BEGIN;
-- Local-only seed preceding the timestamp migration. Synthetic data only.
INSERT INTO auth.users(id) VALUES ('55550000-0000-4000-8000-000000000011');
INSERT INTO public.users(id,email,name,role) VALUES
 ('55550000-0000-4000-8000-000000000011','timestamp-fixture@example.invalid','Timestamp fixture','supervisor');
INSERT INTO public.inventory_items(id,name,quantity,created_at) VALUES
 ('55550000-0000-4000-8000-000000000012','Timestamp fixture item',10,'2001-01-01T00:00:00Z');
INSERT INTO public.inventory_transactions(id,item_id,delta,reason,actor_id,idempotency_key,created_at) VALUES
 ('55550000-0000-4000-8000-000000000013','55550000-0000-4000-8000-000000000012',1,'legacy fixture','55550000-0000-4000-8000-000000000011','timestamp-legacy','2000-01-01T00:00:00Z');

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

ROLLBACK;
