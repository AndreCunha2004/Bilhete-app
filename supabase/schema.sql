-- Bilhete: banco no Supabase
-- Cole tudo no SQL Editor do projeto e clique em "Run". Pode rodar mais de uma vez sem problema.

-- 1) Tabela única: cada linha é um "documento" do app (mesmo modelo das pastas de antes)
create table if not exists public.docs (
  path        text primary key,          -- ex.: bilhetes/2026-11-24_a_xyz
  col         text not null,             -- pasta: bilhetes, listas/abc/itens…
  id          text not null,
  data        jsonb not null,
  updated_at  timestamptz not null default now()
);
create index if not exists docs_col_idx on public.docs (col);
create index if not exists docs_col_date_idx on public.docs (col, (data->>'date'));

-- 2) Só vocês dois: login com andre@bilhete.app ou maju@bilhete.app
create or replace function public.e_do_casal() returns boolean
language sql stable as $$
  select coalesce(auth.jwt() ->> 'email', '') in ('andre@bilhete.app', 'maju@bilhete.app')
$$;

alter table public.docs enable row level security;
drop policy if exists "casal le"      on public.docs;
drop policy if exists "casal cria"    on public.docs;
drop policy if exists "casal altera"  on public.docs;
drop policy if exists "casal apaga"   on public.docs;
create policy "casal le"     on public.docs for select to authenticated using (public.e_do_casal());
create policy "casal cria"   on public.docs for insert to authenticated with check (public.e_do_casal());
create policy "casal altera" on public.docs for update to authenticated using (public.e_do_casal()) with check (public.e_do_casal());
create policy "casal apaga"  on public.docs for delete to authenticated using (public.e_do_casal());

-- 3) Tempo real (bilhete chega na hora, sem atualizar a página)
alter table public.docs replica identity full;
do $$ begin
  alter publication supabase_realtime add table public.docs;
exception when duplicate_object then null; end $$;

-- 4) Presença ("online", "desenhando agora") só para quem está logado
-- (feito pelo canal de Realtime; não precisa de tabela)
