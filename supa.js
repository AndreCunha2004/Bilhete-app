/* Bilhete fora do Claude: substitui claude.use(db|user|room|downloads) por Supabase.
   Modelo de dados: uma tabela "docs" (path, col, id, data jsonb), igual às "pastas" do app. */
(function () {
  'use strict';
  const CFG = window.BILHETE_CFG || {};
  const DOMAIN = 'bilhete.app';
  const USERS = ['andre', 'maju']; // só essas duas contas existem
  window.BILHETE_WEB = true;

  let ready, resolveReady;
  ready = new Promise(r => (resolveReady = r));
  let sb = null, uname = null;

  /* ---------------- tela de login ---------------- */
  const css = `.bw-ov{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:24px;background:#F5F0E6;font-family:'DM Sans',system-ui,sans-serif;color:#262C45}
  .bw-card{width:100%;max-width:360px;display:flex;flex-direction:column;gap:14px}
  .bw-logo{font-family:'Caveat',cursive;font-size:56px;font-weight:700;color:#475480;text-align:center;margin:0 0 4px}
  .bw-sub{text-align:center;color:#5E6274;margin:-10px 0 8px;font-size:15px}
  .bw-card label{font-size:14px;color:#5E6274;display:flex;flex-direction:column;gap:6px}
  .bw-card input{font:inherit;font-size:17px;padding:14px 16px;border-radius:14px;border:1px solid #E2D9C6;background:#FFFCF6;color:#262C45}
  .bw-card button{font:inherit;font-weight:700;font-size:17px;min-height:52px;border:0;border-radius:16px;background:#7F3B25;color:#fff;cursor:pointer}
  .bw-card button[disabled]{opacity:.6}
  .bw-err{color:#7F3B25;font-size:14px;min-height:20px;margin:0;text-align:center}
  .bw-pw{position:relative;display:block}.bw-pw input{width:100%;box-sizing:border-box;padding-right:96px}
  .bw-card .bw-pw button{position:absolute;right:6px;top:50%;transform:translateY(-50%);min-height:40px;padding:0 12px;font-size:14px;background:#EFE7D6;color:#262C45;border-radius:10px}
  .bw-note{font-size:13px;color:#5E6274;text-align:center;margin:0}`;
  function overlay(html) {
    let st = document.getElementById('bw-style');
    if (!st) { st = document.createElement('style'); st.id = 'bw-style'; st.textContent = css; document.head.appendChild(st); }
    let ov = document.getElementById('bw-ov');
    if (!ov) { ov = document.createElement('div'); ov.id = 'bw-ov'; ov.className = 'bw-ov'; document.body.appendChild(ov); }
    ov.innerHTML = html; return ov;
  }
  function closeOverlay() { const ov = document.getElementById('bw-ov'); if (ov) ov.remove(); }
  function showLogin(msg) {
    const ov = overlay(`<form class="bw-card" id="bw-f" autocomplete="on">
      <p class="bw-logo">Bilhete</p><p class="bw-sub">Entre para ver os bilhetes de vocês</p>
      <label>Usuário<input id="bw-u" name="username" autocomplete="username" autocapitalize="none" spellcheck="false" required></label>
      <label>Senha<span class="bw-pw"><input id="bw-p" name="password" type="password" autocomplete="current-password" required><button type="button" id="bw-eye" aria-label="Mostrar senha" aria-pressed="false">Mostrar</button></span></label>
      <p class="bw-err" id="bw-e" role="alert">${msg || ''}</p>
      <button type="submit" id="bw-b">Entrar</button>
      <p class="bw-note">Você só precisa entrar uma vez neste aparelho.</p></form>`);
    const eye = ov.querySelector('#bw-eye'), pw = ov.querySelector('#bw-p');
    eye.addEventListener('click', () => { const show = pw.type === 'password'; pw.type = show ? 'text' : 'password'; eye.textContent = show ? 'Ocultar' : 'Mostrar'; eye.setAttribute('aria-pressed', String(show)); eye.setAttribute('aria-label', show ? 'Ocultar senha' : 'Mostrar senha'); pw.focus(); });
    ov.querySelector('#bw-f').addEventListener('submit', async e => {
      e.preventDefault();
      const u = ov.querySelector('#bw-u').value.trim().toLowerCase().replace(/@.*$/, ''), p = ov.querySelector('#bw-p').value;
      const b = ov.querySelector('#bw-b'), er = ov.querySelector('#bw-e');
      if (!USERS.includes(u)) { er.textContent = 'Esse usuário não existe. Use ' + USERS.join(' ou ') + '.'; return; }
      b.disabled = true; b.textContent = 'Entrando…'; er.textContent = '';
      const { data, error } = await sb.auth.signInWithPassword({ email: u + '@' + DOMAIN, password: p });
      b.disabled = false; b.textContent = 'Entrar';
      if (error || !data.session) { const m = String((error && (error.message || error.code)) || ''); console.warn('login', error);
        er.textContent = /confirm/i.test(m) ? 'Essa conta ainda não foi confirmada no Supabase (Auto Confirm).' : /disabled|not enabled|provider/i.test(m) ? 'O login por e-mail está desligado no Supabase.' : /invalid.*credential|invalid login/i.test(m) ? 'Senha incorreta para ' + u + '. Toque em Mostrar para conferir.' : /fetch|network/i.test(m) ? 'Sem conexão com o banco. Confira a internet.' : 'Não deu para entrar agora. Tente de novo em instantes.'; return; }
      start(data.session);
    });
    setTimeout(() => { const i = document.getElementById('bw-u'); if (i) i.focus(); }, 50);
  }
  function start(session) {
    uname = String(session.user.email || '').split('@')[0]; window.bilheteUser = uname;
    try { sb.realtime.setAuth(session.access_token); } catch (_) {}
    closeOverlay(); resolveReady(true);
  }
  window.bilheteSair = async () => { try { await sb.auth.signOut(); } catch (e) {} location.reload(); };

  async function boot() {
    if (!window.supabase || !CFG.url || !CFG.anon || /COLE_/.test(CFG.url + CFG.anon)) {
      overlay(`<div class="bw-card"><p class="bw-logo">Bilhete</p><p class="bw-sub">Estamos configurando o banco de dados. Volte daqui a pouco 💌</p></div>`);
      return;
    }
    sb = window.supabase.createClient(CFG.url, CFG.anon, { auth: { persistSession: true, autoRefreshToken: true, storageKey: 'bilhete-auth' } });
    window.__sb = sb;
    const { data } = await sb.auth.getSession();
    if (data && data.session) start(data.session); else showLogin();
    sb.auth.onAuthStateChange((ev, ses) => { if (ev === 'SIGNED_OUT') location.reload(); else if (ses && ses.access_token) { try { sb.realtime.setAuth(ses.access_token); } catch (_) {} } });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();

  /* ---------------- db ---------------- */
  const colOf = p => p.split('/').slice(0, -1).join('/');
  const idOf = p => p.split('/').pop();
  const rid = () => Array.from(crypto.getRandomValues(new Uint8Array(15)), b => 'abcdefghijklmnopqrstuvwxyz0123456789'[b % 36]).join('');
  const err = e => { const m = String((e && (e.message || e.code)) || e); const o = new Error(m); o.code = /permission|policy|JWT|401|403/i.test(m) ? 'permission_denied' : 'unavailable'; return o; };
  const isObj = v => v && typeof v === 'object' && !Array.isArray(v);
  const merge = (a, b) => { const o = { ...(a || {}) }; for (const k in b) o[k] = isObj(b[k]) && isObj(o[k]) ? merge(o[k], b[k]) : b[k]; return o; };
  const snapDoc = (path, data) => ({ id: idOf(path), exists: data != null, data: () => data, ref: docRef(path), metadata: { fromCache: false } });

  /* realtime: um canal por pasta, vários ouvintes */
  const chans = new Map();
  const locals = new Map(); // col -> Set(refresh) : atualização local imediata após escrever (como o app espera)
  function local(col, f) { let z = locals.get(col); if (!z) { z = new Set(); locals.set(col, z); } z.add(f); return () => z.delete(f); }
  async function bump(col) { const z = locals.get(col); if (z) await Promise.all([...z].map(f => f().catch(() => {}))); }
  function listen(col, fn) {
    let c = chans.get(col);
    if (!c) {
      c = { fns: new Set(), ch: null };
      c.ch = sb.channel('docs:' + col).on('postgres_changes', { event: '*', schema: 'public', table: 'docs', filter: 'col=eq.' + col }, pl => c.fns.forEach(f => { try { f(pl); } catch (e) { console.warn(e); } })).subscribe();
      chans.set(col, c);
    }
    c.fns.add(fn);
    return () => { c.fns.delete(fn); if (!c.fns.size) { sb.removeChannel(c.ch); chans.delete(col); } };
  }
  // reconecta e recarrega quando o app volta do segundo plano
  const wakers = new Set();
  document.addEventListener('visibilitychange', () => { if (!document.hidden) wakers.forEach(f => f()); });
  window.addEventListener('online', () => wakers.forEach(f => f()));

  async function getData(path) {
    const { data, error } = await sb.from('docs').select('data').eq('path', path).maybeSingle();
    if (error) throw err(error); return data ? data.data : null;
  }
  async function put(path, data) {
    const { error } = await sb.from('docs').upsert({ path, col: colOf(path), id: idOf(path), data, updated_at: new Date().toISOString() });
    if (error) throw err(error);
    await bump(colOf(path));
  }
  function docRef(path) {
    return {
      id: idOf(path), path,
      get: async () => { await ready; return snapDoc(path, await getData(path)); },
      set: async d => { await ready; await put(path, JSON.parse(JSON.stringify(d))); },
      update: async d => { await ready; const cur = await getData(path); if (cur == null) { const e = new Error('not found'); e.code = 'not_found'; throw e; } await put(path, merge(cur, JSON.parse(JSON.stringify(d)))); },
      delete: async () => { await ready; const { error } = await sb.from('docs').delete().eq('path', path); if (error) throw err(error); await bump(colOf(path)); },
      onSnapshot(next, onErr) {
        let off = null, dead = false, offL = null;
        const load = () => getData(path).then(d => { if (!dead) next(snapDoc(path, d)); }, e => onErr && onErr(err(e)));
        ready.then(() => { if (dead) return; load(); offL = local(colOf(path), load); off = listen(colOf(path), pl => { const p = (pl.new && pl.new.path) || (pl.old && pl.old.path); if (p === path) { if (pl.eventType === 'DELETE') next(snapDoc(path, null)); else if (pl.new && pl.new.data !== undefined) next(snapDoc(path, pl.new.data)); else load(); } }); wakers.add(load); });
        return () => { dead = true; if (off) off(); if (offL) offL(); wakers.delete(load); };
      }
    };
  }
  const OPS = { '==': (a, b) => a === b, '!=': (a, b) => a !== b, '<': (a, b) => a < b, '<=': (a, b) => a <= b, '>': (a, b) => a > b, '>=': (a, b) => a >= b, 'in': (a, b) => Array.isArray(b) && b.includes(a) };
  function query(col, st) {
    st = st || { w: [], o: null, l: 0 };
    const run = async () => {
      let q = sb.from('docs').select('path,data').eq('col', col);
      const eqs = st.w.filter(w => w[1] === '==' && (typeof w[2] === 'string' || typeof w[2] === 'number'));
      eqs.forEach(([f, , v]) => { q = q.eq('data->>' + f, String(v)); });
      const rest = st.w.filter(w => !eqs.includes(w));
      if (st.o) q = q.order('data->' + st.o[0], { ascending: st.o[1] !== 'desc', nullsFirst: false });
      if (st.l && !rest.length) q = q.limit(st.l); else q = q.limit(5000);
      const { data, error } = await q;
      if (error) throw err(error);
      let rows = (data || []).filter(r => rest.every(([f, op, v]) => (OPS[op] || (() => true))(r.data && r.data[f], v)));
      if (st.l) rows = rows.slice(0, st.l);
      const docs = rows.map(r => snapDoc(r.path, r.data));
      return { docs, size: docs.length, empty: !docs.length, metadata: { fromCache: false }, forEach: f => docs.forEach(f) };
    };
    return {
      where: (f, op, v) => query(col, { ...st, w: st.w.concat([[f, op, v]]) }),
      orderBy: (f, d) => query(col, { ...st, o: [f, d || 'asc'] }),
      limit: n => query(col, { ...st, l: n }),
      doc: id => docRef(col + '/' + (id || rid())),
      add: async d => { const r = docRef(col + '/' + rid()); await r.set(d); return r; },
      get: async () => { await ready; return run(); },
      onSnapshot(next, onErr) {
        let off = null, dead = false, t = 0, offL = null, seq = 0;
        const load = () => { const my = ++seq; return run().then(s => { if (!dead && my === seq) next(s); }, e => onErr && onErr(err(e))); };
        const soon = () => { clearTimeout(t); t = setTimeout(load, 120); };
        ready.then(() => { if (dead) return; load(); offL = local(col, load); off = listen(col, soon); wakers.add(load); });
        return () => { dead = true; clearTimeout(t); if (off) off(); if (offL) offL(); wakers.delete(load); };
      }
    };
  }
  const db = { doc: docRef, collection: c => query(c) };

  /* ---------------- user ---------------- */
  const user = { id: async () => { await ready; return uname; }, can: async () => { await ready; return true; } };

  /* ---------------- room (presença em tempo real) ---------------- */
  // Online/offline confiável no iPhone: sai na hora ao ir para segundo plano, renova a cada 20 s
  // e ignora "fantasmas" (aparelho que dormiu sem avisar) com mais de 60 s sem renovar.
  const tab = rid().slice(0, 8), STALE = 60e3, BEAT = 20e3;
  let rch = null, mine = {}, peerFns = new Set(), lastPeers = [], tT = 0, rjT = 0;
  const myKey = () => uname + ':' + tab;
  function peersNow() {
    if (!rch) return [];
    const st = rch.presenceState(), out = [], now = Date.now();
    for (const k in st) {
      const metas = st[k] || []; const m = metas[metas.length - 1]; if (!m) continue;
      const me = k === myKey();
      if (!me && (m.hidden || now - (m.at || 0) > STALE)) continue;
      out.push({ peer: k, by: m.by, isMe: me, sameTab: me, kind: 'viewer', presence: m.p || {}, updatedAt: m.at || 0 });
    }
    return out;
  }
  function emit() {
    const peers = peersNow(), prev = lastPeers; lastPeers = peers;
    const sig = p => p.map(x => x.peer + JSON.stringify(x.presence)).sort().join('|');
    if (sig(peers) === sig(prev) && prev.length === peers.length && peerFns.size && emit.done) return;
    emit.done = true;
    peerFns.forEach(f => { try { f({ peers, joined: peers.filter(p => !prev.some(q => q.peer === p.peer)), left: prev.filter(p => !peers.some(q => q.peer === p.peer)), updated: peers }); } catch (e) { console.warn(e); } });
  }
  let modo = 'private', ultimoErro = '', rejoining = false, ultimoSync = 0;
  function rejoin(delay) {
    clearTimeout(rjT);
    rjT = setTimeout(async () => {
      if (rejoining) return; rejoining = true;
      try { if (rch) { const old = rch; rch = null; await sb.removeChannel(old); } } catch (_) {}
      rejoining = false; ensureRoom();
    }, delay || 0);
  }
  async function ensureRoom() {
    await ready; if (rch || rejoining) return;
    const ch = sb.channel('sala', { config: { private: modo === 'private', presence: { key: myKey() } } });
    rch = ch;
    const sync = () => { ultimoSync = Date.now(); emit(); };
    ch.on('presence', { event: 'sync' }, sync).on('presence', { event: 'join' }, sync).on('presence', { event: 'leave' }, sync)
      .subscribe((st, e) => {
        if (st === 'SUBSCRIBED') { ultimoErro = ''; track(true); return; }
        if (rch !== ch) return;
        ultimoErro = st + (e && e.message ? ': ' + e.message : '');
        if (st === 'CHANNEL_ERROR' && modo === 'private') { modo = 'public'; rejoin(0); return; } // sem a regra de tempo real privado no banco: usa canal público
        if (!document.hidden) rejoin(3000);
      });
  }
  function track(now) {
    clearTimeout(tT);
    const go = () => { if (rch && !document.hidden) rch.track({ by: uname, p: mine, at: Date.now() }).catch(() => {}); };
    if (now) go(); else tT = setTimeout(go, 60);
  }
  function sair() { clearTimeout(tT); if (rch) { try { rch.untrack(); } catch (_) {} } }
  function voltar() {
    if (!sb || !uname) return;
    try { if (sb.realtime && !sb.realtime.isConnected()) sb.realtime.connect(); } catch (_) {}
    if (!rch || rch.state === 'closed' || rch.state === 'errored') rejoin(0); else { track(true); emit(); }
  }
  document.addEventListener('visibilitychange', () => { if (document.hidden) sair(); else voltar(); });
  window.addEventListener('pagehide', sair);
  window.addEventListener('pageshow', () => { if (!document.hidden) voltar(); });
  window.addEventListener('online', () => voltar());
  setInterval(() => { if (document.hidden || !rch) return; if (rch.state === 'closed' || rch.state === 'errored') rejoin(0); else if (rch.state === 'joined') track(true); emit(); }, BEAT);
  const room = {
    presence: async o => { mine = { ...mine, ...(o || {}) }; Object.keys(mine).forEach(k => { if (mine[k] == null) delete mine[k]; }); await ensureRoom(); track(); },
    onPeers: (fn) => { peerFns.add(fn); ensureRoom().then(() => setTimeout(() => { emit.done = false; emit(); }, 0)); return () => peerFns.delete(fn); }
  };

  /* ---------------- diagnóstico ---------------- */
  window.bilheteDiag = async () => {
    await ready;
    const r = { usuario: uname, conectado: false, canal: rch ? rch.state : 'sem canal', modo, ultimoErro, ultimoSync, online: [], aparelhoInscrito: false, inscricoesNoBanco: 0, atividades: [] };
    try { r.conectado = sb.realtime.isConnected(); } catch (_) {}
    r.online = peersNow().filter(p => !p.isMe).map(p => p.by + (p.presence && p.presence.mode ? ' (' + p.presence.mode + ')' : ''));
    r.push = window.bilhetePushStatus ? window.bilhetePushStatus() : '?';
    try { const reg = await Promise.race([navigator.serviceWorker.ready, new Promise((_, no) => setTimeout(() => no(new Error('sw')), 3000))]); r.aparelhoInscrito = !!(await reg.pushManager.getSubscription()); } catch (_) {}
    try { const { data } = await sb.from('docs').select('path').eq('col', 'push').eq('data->>by', uname); r.inscricoesNoBanco = (data || []).length; } catch (_) {}
    try { const { data } = await sb.from('docs').select('data').eq('col', 'atividades').order('data->at', { ascending: false }).limit(8); r.atividades = (data || []).map(x => ({ t: x.data.t, by: x.data.by, at: x.data.at, pushed: !!x.data.pushed })); } catch (_) {}
    return r;
  };
  window.bilheteTestePush = async () => {
    await ready;
    const { data } = await sb.auth.getSession(); const tok = data && data.session && data.session.access_token;
    try {
      const res = await fetch(CFG.url.replace(/\/$/, '') + '/functions/v1/Notificar', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + tok, apikey: CFG.anon }, body: JSON.stringify({ teste_push: true }) });
      const txt = await res.text(); let j = null; try { j = JSON.parse(txt); } catch (_) {}
      return { status: res.status, ...(j || { texto: txt.slice(0, 200) }) };
    } catch (e) { return { status: 0, erro: 'Não alcançou a função (rede ou CORS). Confira se ela se chama notificar e está publicada.' }; }
  };

  /* ---------------- downloads ---------------- */
  const downloads = {
    save: async ({ filename, data }) => {
      const blob = data instanceof Blob ? data : new Blob([data], { type: /\.json$/.test(filename) ? 'application/json' : /\.png$/.test(filename) ? 'image/png' : 'application/octet-stream' });
      const f = new File([blob], filename, { type: blob.type });
      if (navigator.canShare && navigator.canShare({ files: [f] })) { try { await navigator.share({ files: [f] }); return { status: 'saved' }; } catch (e) { if (e && e.name === 'AbortError') return { status: 'cancelled' }; } }
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
      return { status: 'saved' };
    }
  };

  /* ---------------- importar backup do app antigo ---------------- */
  window.bilheteImportar = async (json, onProg) => {
    await ready;
    const B = typeof json === 'string' ? JSON.parse(json) : json;
    if (!B || B.app !== 'Bilhete') throw new Error('Esse arquivo não é um backup do Bilhete.');
    const rows = [], add = (path, data) => { if (data != null) rows.push({ path, col: colOf(path), id: idOf(path), data, updated_at: new Date().toISOString() }); };
    const strip = o => { const c = { ...o }; delete c.id; return c; };
    if (B.casal) { const c = JSON.parse(JSON.stringify(B.casal)); if (c.slots) { if (c.slots.a) c.slots.a.uid = 'andre'; if (c.slots.b) c.slots.b.uid = 'maju'; } add('casal/config', c); }
    if (B.datas) add('casal/datas', B.datas);
    (B.bilhetes || []).forEach(n => n && n.id && add('bilhetes/' + n.id, strip(n)));
    Object.entries(B.imagens || {}).forEach(([id, d]) => d && add('imagens/' + id, { data: d, by: 'import', at: Date.now() }));
    (B.listas || []).forEach(l => { if (!l || !l.id) return; const { itens, conversa, ...meta } = l; add('listas/' + l.id, strip(meta)); (itens || []).forEach(i => i && i.id && add('listas/' + l.id + '/itens/' + i.id, strip(i))); (conversa || []).forEach(m => m && m.id && add('listas/' + l.id + '/chat/' + m.id, strip(m))); });
    (B.atividades || []).forEach(a => a && a.id && add('atividades/' + a.id, strip(a)));
    let done = 0;
    for (let i = 0; i < rows.length; i += 20) {
      const chunk = rows.slice(i, i + 20);
      const { error } = await sb.from('docs').upsert(chunk);
      if (error) throw err(error);
      done += chunk.length; if (onProg) onProg(done, rows.length);
    }
    return rows.length;
  };

  /* ---------------- notificações no celular ---------------- */
  const b64 = s => { const p = '='.repeat((4 - s.length % 4) % 4), r = atob((s + p).replace(/-/g, '+').replace(/_/g, '/')); return Uint8Array.from(r, c => c.charCodeAt(0)); };
  const hashOf = async t => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t))).slice(0, 8), b => b.toString(16).padStart(2, '0')).join('');
  const standalone = () => (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  window.bilhetePushStatus = () => {
    if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) return /iPhone|iPad/.test(navigator.userAgent) && !standalone() ? 'instalar' : 'sem-suporte';
    return Notification.permission; // default | granted | denied
  };
  async function salvarSub(sub) {
    const j = sub.toJSON(), id = uname + '_' + await hashOf(j.endpoint);
    await put('push/' + id, { by: uname, sub: j, ua: navigator.userAgent.slice(0, 120), at: Date.now() });
  }
  window.bilhetePush = async () => {
    await ready;
    const st = window.bilhetePushStatus();
    if (st === 'instalar') return { ok: false, msg: 'Primeiro adicione o Bilhete à Tela de Início (Safari › Compartilhar) e abra por lá.' };
    if (st === 'sem-suporte') return { ok: false, msg: 'Este navegador não aceita notificações.' };
    if (!CFG.vapid) return { ok: false, msg: 'Notificações ainda não configuradas.' };
    const perm = await Notification.requestPermission();
    if (perm !== 'granted') return { ok: false, msg: 'Permissão negada. Ative em Ajustes › Notificações › Bilhete.' };
    const reg = await navigator.serviceWorker.ready;
    let sub = await reg.pushManager.getSubscription();
    if (!sub) sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64(CFG.vapid) });
    await salvarSub(sub);
    return { ok: true, msg: 'Notificações ativadas neste aparelho.' };
  };
  // mantém a inscrição atualizada e limpa o selo do ícone ao abrir
  ready.then(async () => {
    try { if (navigator.clearAppBadge) navigator.clearAppBadge(); } catch (_) {}
    try { if (window.bilhetePushStatus() === 'granted' && CFG.vapid) { const reg = await navigator.serviceWorker.ready; const sub = await reg.pushManager.getSubscription(); if (sub) await salvarSub(sub); } } catch (e) { console.warn('push', e); }
  });
  document.addEventListener('visibilitychange', () => { if (!document.hidden && navigator.clearAppBadge) navigator.clearAppBadge().catch(() => {}); });

  /* ---------------- ponte claude.use ---------------- */
  const caps = { db, user, room, downloads };
  window.claude = { use: async n => { if (!(n in caps)) return null; await ready; return caps[n]; } };
})();
