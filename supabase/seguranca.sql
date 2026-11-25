-- Rode no SQL Editor. Troque as duas senhas ANTES de clicar em Run (não compartilhe com ninguém).

-- 1) Presença em tempo real em canal privado: só vocês dois
drop policy if exists "casal realtime" on realtime.messages;
create policy "casal realtime" on realtime.messages for all to authenticated
  using (public.e_do_casal()) with check (public.e_do_casal());

-- 2) Senhas novas + sair de todos os aparelhos
update auth.users set encrypted_password = extensions.crypt('NOVA_SENHA_ANDRE', extensions.gen_salt('bf')) where email = 'andre@bilhete.app';
update auth.users set encrypted_password = extensions.crypt('NOVA_SENHA_MAJU',  extensions.gen_salt('bf')) where email = 'maju@bilhete.app';
delete from auth.sessions where user_id in (select id from auth.users where email in ('andre@bilhete.app', 'maju@bilhete.app'));
