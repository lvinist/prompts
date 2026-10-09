BEGIN;
-- Local-only seed preceding the timestamp migration. Synthetic data only.
INSERT INTO auth.users(id) VALUES ('55550000-0000-4000-8000-000000000011');
INSERT INTO public.users(id,email,name,role) VALUES
 ('55550000-0000-4000-8000-000000000011','timestamp-fixture@example.invalid','Timestamp fixture','supervisor');
INSERT INTO public.inventory_items(id,name,quantity,created_at) VALUES
 ('55550000-0000-4000-8000-000000000012','Timestamp fixture item',10,'2001-01-01T00:00:00Z');
INSERT INTO public.inventory_transactions(id,item_id,delta,reason,actor_id,idempotency_key,created_at) VALUES
 ('55550000-0000-4000-8000-000000000013','55550000-0000-4000-8000-000000000012',1,'legacy fixture','55550000-0000-4000-8000-000000000011','timestamp-legacy','2000-01-01T00:00:00Z');

-- STEP-55 owner decisions (2026-10-06): separate client event time from server
-- audit time. Preserve historical created_at values and label them honestly.
-- Inventory-item created_at intentionally remains client-authored and unchanged.
-- Preparation/local testing only; remote deployment requires separate approval.

ALTER TABLE public.inventory_transactions
    ADD COLUMN occurred_at timestamptz,
    ADD COLUMN created_at_source text NOT NULL DEFAULT 'legacy_client'
        CHECK (created_at_source IN ('legacy_client', 'server'));

-- Existing timestamps cannot be retroactively called server observations.
UPDATE public.inventory_transactions SET occurred_at = created_at;
ALTER TABLE public.inventory_transactions
    ALTER COLUMN occurred_at SET NOT NULL,
    ALTER COLUMN created_at_source SET DEFAULT 'server';

COMMENT ON COLUMN public.inventory_transactions.occurred_at IS
'Client-reported event time, retained across offline replay; not trusted server audit time.';
COMMENT ON COLUMN public.inventory_transactions.created_at IS
'Server-authored insert time for source=server; preserved original client timestamp for source=legacy_client.';
COMMENT ON COLUMN public.inventory_transactions.created_at_source IS
'Provenance of created_at. legacy_client rows predate the audit-time migration; all subsequent inserts are server.';

-- A column default alone can be overridden by a caller. Enforce both the time
-- and its provenance for every new row, including a direct INSERT under RLS.
CREATE FUNCTION public.stamp_inventory_transaction_audit_time()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = ''
AS $$
BEGIN
    NEW.created_at := statement_timestamp();
    NEW.created_at_source := 'server';
    RETURN NEW;
END;
$$;

CREATE TRIGGER stamp_inventory_transaction_audit_time
BEFORE INSERT ON public.inventory_transactions
FOR EACH ROW EXECUTE FUNCTION public.stamp_inventory_transaction_audit_time();

-- Keep the existing RPC signature so queued offline clients can drain safely.
-- p_created_at now names event time only; item LWW ordering remains unchanged.
CREATE OR REPLACE FUNCTION public.adjust_inventory(
    p_item_id uuid,
    p_delta numeric,
    p_reason text,
    p_actor_id uuid,
    p_idempotency_key text,
    p_created_at timestamptz
) RETURNS void
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = ''
AS $$
DECLARE
    v_new_quantity numeric(10,2);
BEGIN
    IF p_idempotency_key IS NOT NULL AND EXISTS (
        SELECT 1 FROM public.inventory_transactions WHERE idempotency_key = p_idempotency_key
    ) THEN
        RETURN;
    END IF;

    UPDATE public.inventory_items
    SET quantity = quantity + p_delta,
        updated_at = GREATEST(updated_at, p_created_at)
    WHERE id = p_item_id
    RETURNING quantity INTO v_new_quantity;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item not found';
    END IF;

    INSERT INTO public.inventory_transactions (
        item_id, delta, reason, actor_id, idempotency_key, occurred_at
    ) VALUES (
        p_item_id, p_delta, p_reason, p_actor_id, p_idempotency_key, p_created_at
    );
END;
$$;

-- LOCAL-only regression, run inside a transaction after the synthetic legacy
-- fixture and (for GREEN) the timestamp migration. Caller rolls everything back.
SET LOCAL ROLE authenticated;
SELECT set_config('request.jwt.claim.role','authenticated',true);
SELECT set_config('request.jwt.claim.sub','55550000-0000-4000-8000-000000000011',true);
SELECT public.adjust_inventory(
 '55550000-0000-4000-8000-000000000012',2,'timestamp fixture',
 '55550000-0000-4000-8000-000000000011','timestamp-new','2002-01-01T00:00:00Z');
DO $$
DECLARE actual timestamptz;
BEGIN
 SELECT created_at INTO actual FROM public.inventory_transactions WHERE idempotency_key='timestamp-new';
 IF actual IS NULL OR actual < transaction_timestamp() OR actual > clock_timestamp() THEN
   RAISE EXCEPTION 'REGRESSION: ledger audit timestamp trusts the client clock';
 END IF;
 RAISE NOTICE 'PASS: new ledger created_at is server-authored';
END;
$$;

DO $$
DECLARE before_quantity numeric; before_audit timestamptz; rows_before integer;
BEGIN
 IF NOT EXISTS (SELECT 1 FROM public.inventory_transactions
   WHERE idempotency_key='timestamp-legacy' AND created_at='2000-01-01T00:00:00Z'
     AND occurred_at=created_at AND created_at_source='legacy_client') THEN
   RAISE EXCEPTION 'Legacy timestamp was rewritten or falsely labelled server';
 END IF;
 IF NOT EXISTS (SELECT 1 FROM public.inventory_transactions
   WHERE idempotency_key='timestamp-new' AND occurred_at='2002-01-01T00:00:00Z'
     AND created_at_source='server') THEN
   RAISE EXCEPTION 'Client event time or new audit provenance lost';
 END IF;
 SELECT quantity INTO before_quantity FROM public.inventory_items
   WHERE id='55550000-0000-4000-8000-000000000012';
 SELECT created_at INTO before_audit FROM public.inventory_transactions WHERE idempotency_key='timestamp-new';
 SELECT count(*) INTO rows_before FROM public.inventory_transactions;
 PERFORM public.adjust_inventory('55550000-0000-4000-8000-000000000012',2,'retry',
   '55550000-0000-4000-8000-000000000011','timestamp-new','2002-01-01T00:00:00Z');
 IF (SELECT quantity FROM public.inventory_items WHERE id='55550000-0000-4000-8000-000000000012') <> before_quantity
   OR (SELECT count(*) FROM public.inventory_transactions) <> rows_before
   OR (SELECT created_at FROM public.inventory_transactions WHERE idempotency_key='timestamp-new') <> before_audit THEN
   RAISE EXCEPTION 'Replay changed stock, ledger count or audit timestamp';
 END IF;
 BEGIN
   PERFORM public.adjust_inventory('55550000-0000-4000-8000-000000000012',2,'invalid event',
     '55550000-0000-4000-8000-000000000011','timestamp-null',NULL);
   RAISE EXCEPTION 'Null event time unexpectedly accepted';
 EXCEPTION WHEN not_null_violation THEN NULL;
 END;
 IF (SELECT quantity FROM public.inventory_items WHERE id='55550000-0000-4000-8000-000000000012') <> before_quantity
   OR EXISTS (SELECT 1 FROM public.inventory_transactions WHERE idempotency_key='timestamp-null') THEN
   RAISE EXCEPTION 'Failed transaction did not roll back quantity and ledger';
 END IF;
 IF (SELECT created_at FROM public.inventory_items WHERE id='55550000-0000-4000-8000-000000000012') <> '2001-01-01T00:00:00Z' THEN
   RAISE EXCEPTION 'Item creation time must remain client-authored and unchanged';
 END IF;
 RAISE NOTICE 'PASS: legacy provenance, event time, replay, rollback and item timestamp preserved';
END;
$$;

INSERT INTO public.inventory_transactions(item_id,delta,reason,actor_id,idempotency_key,
 occurred_at,created_at,created_at_source) VALUES
 ('55550000-0000-4000-8000-000000000012',1,'spoof attempt',
 '55550000-0000-4000-8000-000000000011','timestamp-spoof',
 '2003-01-01T00:00:00Z','1900-01-01T00:00:00Z','legacy_client');
DO $$
BEGIN
 IF NOT EXISTS (SELECT 1 FROM public.inventory_transactions WHERE idempotency_key='timestamp-spoof'
   AND created_at >= transaction_timestamp() AND created_at <= clock_timestamp()
   AND created_at_source='server' AND occurred_at='2003-01-01T00:00:00Z') THEN
   RAISE EXCEPTION 'Direct insert can forge server audit time or legacy provenance';
 END IF;
 RAISE NOTICE 'PASS: direct INSERT cannot spoof audit timestamp or provenance';
END;
$$;

ROLLBACK;
