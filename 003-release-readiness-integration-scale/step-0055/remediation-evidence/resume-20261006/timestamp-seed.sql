-- Local-only seed preceding the timestamp migration. Synthetic data only.
INSERT INTO auth.users(id) VALUES ('55550000-0000-4000-8000-000000000011');
INSERT INTO public.users(id,email,name,role) VALUES
 ('55550000-0000-4000-8000-000000000011','timestamp-fixture@example.invalid','Timestamp fixture','supervisor');
INSERT INTO public.inventory_items(id,name,quantity,created_at) VALUES
 ('55550000-0000-4000-8000-000000000012','Timestamp fixture item',10,'2001-01-01T00:00:00Z');
INSERT INTO public.inventory_transactions(id,item_id,delta,reason,actor_id,idempotency_key,created_at) VALUES
 ('55550000-0000-4000-8000-000000000013','55550000-0000-4000-8000-000000000012',1,'legacy fixture','55550000-0000-4000-8000-000000000011','timestamp-legacy','2000-01-01T00:00:00Z');
