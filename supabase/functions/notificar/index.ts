// Função "notificar": avisos no celular do Bilhete.
// - atividade nova (bilhete, amei, lista, humor, pergunta) → avisa o outro
// - a cada minuto (tick): bilhetes agendados que chegaram, e as rotinas do dia (horário de Brasília):
//     00:05 pergunta do dia (IA) · 09:00 mesversário / aniversário de namoro · 20:00 lembrete de quem não mandou nada
// Secrets: VAPID_PUBLIC, VAPID_PRIVATE, NOTIFY_TOKEN e (opcional) ANTHROPIC_API_KEY para as frases e perguntas com IA.
import webpush from "npm:web-push@3.6.7";
import { createClient } from "npm:@supabase/supabase-js@2";

const URL_ = Deno.env.get("SUPABASE_URL")!;
const KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? (JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS") ?? "{}").default);
const sb = createClient(URL_, KEY, { auth: { persistSession: false } });
webpush.setVapidDetails("mailto:andre@bilhete.app", Deno.env.get("VAPID_PUBLIC")!, Deno.env.get("VAPID_PRIVATE")!);
const AI_KEY = Deno.env.get("ANTHROPIC_API_KEY");

const SLOT_USER: Record<string, string> = { a: "andre", b: "maju" };
const outro = (s: string) => (s === "a" ? "b" : "a");
const q = (s?: string) => (s ? `“${s}”` : "");
type Msg = { title: string; body: string; tag: string };

/* ---------- utilidades ---------- */
async function getDoc(path: string) { const { data } = await sb.from("docs").select("data").eq("path", path).maybeSingle(); return data?.data ?? null; }
async function setDoc(path: string, data: unknown) { const col = path.split("/").slice(0, -1).join("/"), id = path.split("/").pop()!; await sb.from("docs").upsert({ path, col, id, data, updated_at: new Date().toISOString() }); }
async function umaVez(chave: string) { // true só na primeira chamada do dia/rotina
  const { error } = await sb.from("docs").insert({ path: "sistema/" + chave, col: "sistema", id: chave, data: { at: Date.now() } });
  return !error;
}
async function nicks() { const c = await getDoc("casal/config"); return { a: c?.slots?.a?.nick || "Déco", b: c?.slots?.b?.nick || "Juju", inicio: /^\d{4}-\d{2}-\d{2}$/.test(c?.inicio || "") ? c.inicio : "2025-12-05" }; }
async function pushPara(slot: string, msg: Msg) {
  const { data: subs } = await sb.from("docs").select("path,data").eq("col", "push").eq("data->>by", SLOT_USER[slot]);
  const res: { aparelho: string; ok: boolean; status?: number; erro?: string }[] = [];
  console.log("push para", SLOT_USER[slot], "inscrições:", subs?.length ?? 0, "|", msg.title);
  for (const s of subs ?? []) {
    const ap = String(s.data?.ua || "").replace(/^.*\((iPhone|iPad|Macintosh|Android|Windows)[^)]*\).*$/, "$1") || s.path;
    try { const r: any = await webpush.sendNotification(s.data.sub, JSON.stringify({ ...msg, url: "./" }), { TTL: 86400, urgency: "high" }); console.log("push ok", SLOT_USER[slot], r?.statusCode); res.push({ aparelho: ap, ok: true, status: r?.statusCode }); }
    catch (e: any) {
      res.push({ aparelho: ap, ok: false, status: e?.statusCode, erro: String(e?.body || e?.message || e).slice(0, 160) });
      if (e?.statusCode === 404 || e?.statusCode === 410) await sb.from("docs").delete().eq("path", s.path); else console.error("push falhou", e?.statusCode, e?.body || e?.message);
    }
  }
  return res;
}
function agoraBR() { const d = new Date(Date.now() - 3 * 3600e3); return { data: d.toISOString().slice(0, 10), hm: d.toISOString().slice(11, 16), y: d.getUTCFullYear(), m: d.getUTCMonth() + 1, d: d.getUTCDate() }; }

/* ---------- IA (opcional) ---------- */
async function contexto() {
  const { data } = await sb.from("docs").select("data").eq("col", "bilhetes").order("data->createdAt", { ascending: false }).limit(12);
  return (data ?? []).map((r: any) => [r.data?.title, (r.data?.text || "").slice(0, 140)].filter(Boolean).join(": ")).filter(Boolean).join("\n");
}
async function ia(pedido: string, fallback: string) {
  if (!AI_KEY) return fallback;
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": AI_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({ model: "claude-haiku-5-5", max_tokens: 160, messages: [{ role: "user", content: pedido }] }),
    });
    const j = await r.json();
    const t = String(j?.content?.[0]?.text || "").trim().replace(/^["“]|["”]$/g, "");
    return t && t.length < 220 ? t : fallback;
  } catch (e) { console.error("ia", e); return fallback; }
}
const FRASES = ["Cada mês ao seu lado é o meu lugar favorito no calendário.", "A gente vai somando dias, e eu só quero somar mais.", "Mais um mês de nós dois, e o coração ainda acelera igual.", "Distância nenhuma diminui o que a gente constrói todo dia.", "Obrigado por escolher a gente de novo, todo mês."];
const frase = () => FRASES[Math.floor(Math.random() * FRASES.length)];

/* ---------- textos das atividades ---------- */
function texto(a: any, nick: string): Msg | null {
  const k = a.kind === "carta" ? "carta" : "desenho";
  switch (a.t) {
    case "nota_nova": return { title: `${nick} te mandou ${k === "carta" ? "uma carta" : "um desenho"} 💌`, body: a.title || a.snip || "Abra para ver", tag: "nota" };
    case "amei": return { title: `${nick} amou seu ${k} ❤️`, body: a.title || "", tag: "amei" };
    case "chat": return { title: `${nick} comentou${a.title ? " em " + q(a.title) : ""}`, body: a.snip || "", tag: "chat" };
    case "item_novo": return { title: `${nick} adicionou ${q(a.title)}`, body: a.list ? `na lista ${q(a.list)}` : "", tag: "lista" };
    case "item_comprado": return { title: `${nick} marcou ${q(a.title)} como comprado`, body: a.list || "", tag: "lista" };
    case "lista_nova": return { title: `${nick} criou a lista ${q(a.title)}`, body: "", tag: "lista" };
    case "humor": return { title: `${nick} está ${a.title || ""}`.trim(), body: "Toque para ver", tag: "humor" };
    case "pergunta": return { title: `${nick} respondeu a pergunta do dia`, body: "Responda para ver a resposta", tag: "pergunta" };
    default: return null;
  }
}
async function enviar(path: string, a: any) {
  if (!a || !SLOT_USER[a.by] || a.pushed) return 0;
  const n = await nicks();
  const msg = texto(a, (n as any)[a.by]);
  if (msg) await pushPara(outro(a.by), msg);
  await sb.from("docs").update({ data: { ...a, pushed: true } }).eq("path", path);
  return msg ? 1 : 0;
}

/* ---------- rotinas do dia ---------- */
async function perguntaDoDia(dia: string) {
  if (!AI_KEY || !(await umaVez("job-pergunta-" + dia))) return;
  const n = await nicks();
  const p = await ia(`Você cria a "pergunta do dia" de um app de namoro à distância entre ${n.a} e ${n.b} (ele em Vila Velha-ES, ela em Curitiba). Escreva UMA pergunta curta (até 15 palavras), carinhosa e específica sobre o casal: o que fizeram um pelo outro, memórias, planos, sentimentos. Inspire-se nos bilhetes recentes abaixo, sem citar trechos. Responda só com a pergunta, em português do Brasil.\n\nBilhetes recentes:\n${await contexto()}`, "");
  if (p) await setDoc("sistema/pergunta-" + dia, { q: p.replace(/\s+/g, " "), at: Date.now(), by: "ia" });
}
async function datasNamoro(h: ReturnType<typeof agoraBR>) {
  if (!(await umaVez("job-namoro-" + h.data))) return;
  const n = await nicks();
  const [ys, ms, ds] = n.inicio.split("-").map(Number);
  const meses = (h.y - ys) * 12 + (h.m - ms);
  let msg: Msg | null = null;
  if (h.d === ds && meses > 0) {
    const anos = meses % 12 === 0 ? meses / 12 : 0;
    const titulo = anos ? `Hoje fazemos ${anos} ${anos === 1 ? "ano" : "anos"} de namoro 💍` : `Hoje fazemos ${meses} ${meses === 1 ? "mês" : "meses"} de namoro 💕`;
    const corpo = await ia(`Escreva UMA frase curta (até 25 palavras), romântica e natural, em português do Brasil, para ${n.a} e ${n.b}, que hoje completam ${anos ? anos + " ano(s)" : meses + " meses"} de namoro à distância. Use como inspiração os bilhetes recentes, sem citar trechos. Só a frase.\n\n${await contexto()}`, frase());
    msg = { title: titulo, body: corpo, tag: "namoro" };
  } else {
    // aniversário de namoro (anual): avisos 13 e 1 dia antes
    let ya = h.y; if (h.m > ms || (h.m === ms && h.d > ds)) ya++;
    const alvo = Date.UTC(ya, ms - 1, ds), hoje = Date.UTC(h.y, h.m - 1, h.d), faltam = Math.round((alvo - hoje) / 864e5), anos = ya - ys;
    if (anos > 0 && (faltam === 13 || faltam === 1)) {
      const quando = faltam === 1 ? "Amanhã" : `Faltam 13 dias: dia ${ds}/${String(ms).padStart(2, "0")}`;
      const corpo = await ia(`Escreva UMA frase curta (até 25 palavras), carinhosa e animada, em português do Brasil, para ${n.a} e ${n.b}, que daqui a ${faltam} dia(s) completam ${anos} ano(s) de namoro à distância. Só a frase.\n\n${await contexto()}`, frase());
      msg = { title: `${quando} fazemos ${anos} ${anos === 1 ? "ano" : "anos"} de namoro 💍`, body: corpo, tag: "namoro" };
    }
  }
  if (!msg) return;
  for (const s of ["a", "b"]) { const pr = await getDoc("prefs/" + s); if (pr?.datas !== false) await pushPara(s, msg); }
}
async function lembrete20(dia: string) {
  if (!(await umaVez("job-lembrete-" + dia))) return;
  const n = await nicks();
  const { data } = await sb.from("docs").select("data").eq("col", "bilhetes").eq("data->>date", dia);
  for (const s of ["a", "b"]) {
    const pr = await getDoc("prefs/" + s);
    if (pr?.lembrete20 === false) continue;
    if ((data ?? []).some((r: any) => r.data?.slot === s)) continue;
    await pushPara(s, { title: `Ainda dá tempo de mandar um bilhete pra ${(n as any)[outro(s)]} 💌`, body: "Um rabisco rápido já mantém a sequência de vocês.", tag: "lembrete" });
  }
}

const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-bilhete-token", "Access-Control-Allow-Methods": "POST, OPTIONS" };
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const body = await req.json().catch(() => ({}));
  // teste pelo app: usa o login de quem pede e manda a notificação para os aparelhos dele mesmo
  if (body.teste_push) {
    const jwt = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
    const { data: u } = await sb.auth.getUser(jwt);
    const nome = String(u?.user?.email || "").split("@")[0];
    const slot = Object.keys(SLOT_USER).find((k) => SLOT_USER[k] === nome);
    if (!slot) return json({ ok: false, erro: "Login não reconhecido." }, 401);
    const segredos = { VAPID_PUBLIC: !!Deno.env.get("VAPID_PUBLIC"), VAPID_PRIVATE: !!Deno.env.get("VAPID_PRIVATE"), NOTIFY_TOKEN: !!Deno.env.get("NOTIFY_TOKEN"), ANTHROPIC_API_KEY: !!AI_KEY };
    const atraso = Math.min(Math.max(Number(body.atraso) || 0, 0), 20);
    const teste = { title: "Teste do Bilhete 💌", body: "Se você está vendo isto, as notificações funcionam.", tag: "teste-" + Date.now() };
    if (atraso) { // envia depois, para testar com o app fechado
      const job = (async () => { await new Promise((ok) => setTimeout(ok, atraso * 1000)); const e = await pushPara(slot, teste); console.log("teste atrasado", nome, JSON.stringify(e)); })();
      // @ts-ignore EdgeRuntime existe no Supabase
      if (typeof EdgeRuntime !== "undefined") EdgeRuntime.waitUntil(job); else await job;
      const { data: subs } = await sb.from("docs").select("path").eq("col", "push").eq("data->>by", nome);
      return json({ ok: (subs?.length ?? 0) > 0, segredos, agendado: atraso, envios: [], inscricoes: subs?.length ?? 0 });
    }
    const envios = await pushPara(slot, teste);
    console.log("teste", nome, JSON.stringify(envios));
    return json({ ok: envios.some((e) => e.ok), segredos, envios });
  }
  if (req.headers.get("x-bilhete-token") !== Deno.env.get("NOTIFY_TOKEN")) { console.warn("chamada sem token válido"); return new Response("não autorizado", { status: 401 }); }
  console.log("chamada", body.path ? "atividade " + body.path : body.tick ? "tick" : "?");
  let n = 0;
  if (body.path) {
    const { data } = await sb.from("docs").select("path,data").eq("path", body.path).maybeSingle();
    if (data) n += await enviar(data.path, data.data);
  } else if (body.tick) {
    const agora = Date.now();
    const { data } = await sb.from("docs").select("path,data,updated_at").eq("col", "atividades").eq("data->>t", "nota_nova");
    for (const r of data ?? []) {
      const at = Number(r.data?.at) || 0;
      if (r.data?.pushed || at > agora || at < agora - 2 * 3600e3) continue;
      if (Date.parse(r.updated_at) > at - 60e3) continue;
      n += await enviar(r.path, r.data);
    }
    const h = agoraBR();
    if (h.hm >= "00:05" && h.hm < "00:15") await perguntaDoDia(h.data);
    if (h.hm >= "09:00" && h.hm < "09:10") await datasNamoro(h);
    if (h.hm >= "20:00" && h.hm < "20:10") await lembrete20(h.data);
    if (body.teste === "namoro") await datasNamoro({ ...h, data: "teste-" + agora });
  }
  return json({ ok: true, enviados: n });
});
