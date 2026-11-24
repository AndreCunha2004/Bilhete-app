-- Notificações no celular: chama a função "notificar" quando entra uma atividade nova,
-- e a cada minuto confere bilhetes agendados que acabaram de chegar.
-- Troque TOKEN_AQUI pelo mesmo valor do secret NOTIFY_TOKEN antes de rodar.
create extension if not exists pg_net;
create extension if not exists pg_cron;

create or replace function public.notificar_atividade() returns trigger
language plpgsql security definer set search_path = public as $$
declare agora numeric := extract(epoch from now()) * 1000;
begin
  if new.col = 'atividades'
     and coalesce((new.data->>'at')::numeric, 0) between agora - 600000 and agora + 60000 then
    perform net.http_post(
      url := 'https://iulvegutcmzrazaihjdy.supabase.co/functions/v1/notificar',
      headers := jsonb_build_object('Content-Type', 'application/json', 'x-bilhete-token', 'TOKEN_AQUI'),
      body := jsonb_build_object('path', new.path));
  end if;
  return new;
end $$;

drop trigger if exists docs_notificar on public.docs;
create trigger docs_notificar after insert on public.docs
for each row execute function public.notificar_atividade();

select cron.unschedule(jobid) from cron.job where jobname = 'bilhete-agendados';
select cron.schedule('bilhete-agendados', '* * * * *', $cron$
  select net.http_post(
    url := 'https://iulvegutcmzrazaihjdy.supabase.co/functions/v1/notificar',
    headers := '{"Content-Type": "application/json", "x-bilhete-token": "TOKEN_AQUI"}'::jsonb,
    body := '{"tick": true}'::jsonb);
$cron$);
