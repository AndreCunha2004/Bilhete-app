// Função "notificar": manda notificação no celular do outro quando há atividade nova.
// Secrets necessários (Edge Functions › Secrets): VAPID_PUBLIC, VAPID_PRIVATE, NOTIFY_TOKEN
import webpush from "npm:web-push@3.6.7";
import { createClient } from "npm:@supabase/supabase-js@2";

const URL_ = Deno.env.get("SUPABASE_URL")!;
const KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? (JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS") ?? "{}").default);
const sb = createClient(URL_, KEY, { auth: { persistSession: false } });
webpush.setVapidDetails("mailto:andre@bilhete.app", Deno.env.get("VAPID_PUBLIC")!, Deno.env.get("VAPID_PRIVATE")!);

const SLOT_USER: Record<string, string> = { a: "andre", b: "maju" };
const q = (s?: string) => (s ? `“${s}”` : "");

function texto(a: any, nick: string): { title: string; body: string; tag: string } | null {
  const k = a.kind === "carta" ? "carta" : "desenho";
  switch (a.t) {
    case "nota_nova": return { title: `${nick} te mandou ${k === "carta" ? "uma carta" : "um desenho"} 💌`, body: a.title || a.snip || "Abra para ver", tag: "nota" };
    case "amei": return { title: `${nick} amou seu ${k} ❤️`, body: a.title || "", tag: "amei" };
    case "chat": return { title: `${nick} comentou${a.title ? " em " + q(a.title) : ""}`, body: a.snip || "", tag: "chat" };
    case "item_novo": return { title: `${nick} adicionou ${q(a.title)}`, body: a.list ? `na lista ${q(a.list)}` : "", tag: "lista" };
    case "item_comprado": return { title: `${nick} marcou ${q(a.title)} como comprado`, body: a.list || "", tag: "lista" };
    case "lista_nova": return { title: `${nick} criou a lista ${q(a.title)}`, body: "", tag: "lista" };
    case "humor": return { title: `${nick} está ${a.title || ""}`.trim(), body: "Toque para ver como ela(e) está", tag: "humor" };
    case "pergunta": return { title: `${nick} respondeu a pergunta do dia`, body: "Responda para ver a resposta", tag: "pergunta" };
    default: return null; // edições e exclusões não notificam
  }
}

async function enviar(path: string, a: any) {
  if (!a || !SLOT_USER[a.by] || a.pushed) return 0;
  const alvo = SLOT_USER[a.by === "a" ? "b" : "a"];
  const { data: cfg } = await sb.from("docs").select("data").eq("path", "casal/config").maybeSingle();
  const nick = cfg?.data?.slots?.[a.by]?.nick || (a.by === "a" ? "Déco" : "Juju");
  const msg = texto(a, nick);
  if (msg) {
    const { data: subs } = await sb.from("docs").select("path,data").eq("col", "push").eq("data->>by", alvo);
    for (const s of subs ?? []) {
      try { await webpush.sendNotification(s.data.sub, JSON.stringify({ ...msg, url: "./" }), { TTL: 86400 }); }
      catch (e: any) { if (e?.statusCode === 404 || e?.statusCode === 410) await sb.from("docs").delete().eq("path", s.path); else console.error("push", e?.statusCode, e?.body); }
    }
  }
  await sb.from("docs").update({ data: { ...a, pushed: true } }).eq("path", path);
  return msg ? 1 : 0;
}

Deno.serve(async (req) => {
  if (req.headers.get("x-bilhete-token") !== Deno.env.get("NOTIFY_TOKEN")) return new Response("não autorizado", { status: 401 });
  const body = await req.json().catch(() => ({}));
  let n = 0;
  if (body.path) {
    const { data } = await sb.from("docs").select("path,data").eq("path", body.path).maybeSingle();
    if (data) n += await enviar(data.path, data.data);
  } else if (body.tick) {
    // bilhetes agendados que acabaram de "chegar"
    const agora = Date.now();
    const { data } = await sb.from("docs").select("path,data,updated_at").eq("col", "atividades").eq("data->>t", "nota_nova");
    for (const r of data ?? []) {
      const at = Number(r.data?.at) || 0;
      if (r.data?.pushed || at > agora || at < agora - 2 * 3600e3) continue;
      if (Date.parse(r.updated_at) > at - 60e3) continue; // não era agendado (já foi notificado na hora)
      n += await enviar(r.path, r.data);
    }
  }
  return new Response(JSON.stringify({ ok: true, enviados: n }), { headers: { "Content-Type": "application/json" } });
});
