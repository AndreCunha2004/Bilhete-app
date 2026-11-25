"""Gera a versão web (GitHub Pages + Supabase) a partir do index.html do artefato.
Uso: python3 build.py ../bilhete-app/index.html  -> escreve index.html aqui."""
import sys, re, pathlib
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../bilhete-app/index.html').read_text(encoding='utf-8')
s = src

def rep(a, b, cnt=1):
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:80])
    s = s.replace(a, b)

# cabeçalho: PWA + scripts do Supabase antes do app
rep('<title>Bilhete</title>', '''<title>Bilhete</title>
<meta name="theme-color" content="#F5F0E6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Bilhete">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<script src="vendor/supabase-2.119.2.js"></script>
<script src="config.js"></script>
<script src="supa.js"></script>''')

# link compartilhado aponta para o próprio site
rep("const APP_URL='https://claude.ai/artifact/2fGJYCK44UGiqcTHnqWZzt';",
    "const APP_URL=location.origin+location.pathname.replace(/index\\.html$/,'');")

# ---------- Mais repaginado (versão web) ----------
i = s.index("function openMais(){")
j = s.index("\n", s.index("function openPage(n){")) + 1
s = s[:i] + r"""function inicioNamoro(){const v=S.config&&S.config.inicio;return /^\d{4}-\d{2}-\d{2}$/.test(v||'')?v:'2025-12-05'}
function tempoNamoro(ini){const [y,m,d]=ini.split('-').map(Number),[ty,tm,td]=today().split('-').map(Number);let mo=(ty-y)*12+(tm-m),dd=td-d;if(dd<0){mo--;dd+=new Date(Date.UTC(ty,tm-1,0)).getUTCDate()}
 if(mo<0)return 'Começa em '+shortDate(ini);const a=Math.floor(mo/12),r=mo%12,p=[];if(a)p.push(a+(a===1?' ano':' anos'));if(r)p.push(r+(r===1?' mês':' meses'));if(dd||!p.length)p.push(dd+(dd===1?' dia':' dias'));return p.join(', ').replace(/, ([^,]*)$/,' e $1')}
function pushTxt(){return ({granted:'Ativadas neste aparelho',denied:'Bloqueadas nos Ajustes do iPhone',instalar:'Instale na Tela de Início para ativar','sem-suporte':'Este navegador não aceita'})[window.bilhetePushStatus()]||'Desativadas neste aparelho'}
function openMais(){const nx=nextData(),ini=inicioNamoro();
 openSheet(`<div class="sh-head"><h2>Mais</h2><button type="button" class="tool" data-close aria-label="Fechar">${I.close}</button></div>
 <button type="button" class="card who prof" data-page="perfil" aria-label="Seu perfil: ${esc(nick(S.me))}"><span class="av ${S.me}" aria-hidden="true">${esc(initial(nick(S.me)))}</span><div><b>${esc(nick(S.me))}</b><small>Entrou como ${esc(window.bilheteUser||'')}</small></div>${I.chev}</button>
 ${mgrp('Nós dois',[mrow(I.heart(false),'Nosso namoro',esc(tempoNamoro(ini))+' · desde '+esc(shortDate(ini)),'data-page="namoro"'),mrow(I.cal,'Datas especiais',nx?esc((diffDays(nx.date)===0?'Hoje: ':'Próxima: ')+nx.title+' · '+shortDate(nx.date)):'Aniversários, viagens e contagens','data-datas')])}
 ${mgrp('Avisos',[mrow(I.bell,'Notificações',esc(pushTxt()),'data-page="notif"')])}
 ${mgrp('Seus dados',[mrow(I.dl,'Exportar backup','Arquivo .json com tudo de vocês','id="backupbtn"'),mrow(I.dl,'Importar backup','Traz um arquivo exportado antes','id="importbtn"')])}
 ${mgrp('Conta',[mrow(I.back,'Sair desta conta','Só neste aparelho','id="sairbtn"')])}<input type="file" id="importin" accept="application/json,.json" hidden>`,
 ()=>{$('#backupbtn').addEventListener('click',exportBackup);$('#sairbtn').addEventListener('click',()=>confirmSheet('Sair da conta neste aparelho?','Sair',()=>window.bilheteSair()));
  $('#importbtn').addEventListener('click',()=>$('#importin').click());$('#importin').addEventListener('change',async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;
   try{const txt=await f.text();toast('Importando…');const n=await window.bilheteImportar(txt,(d,t)=>{if(d===t||d%100===0)toast('Importando… '+d+' de '+t)});toast(n+' itens importados. Recarregando…');setTimeout(()=>location.reload(),1500)}catch(err){toast(err&&err.message?err.message:'Não deu para importar.')}})},null,{label:'Mais',reopen:openMais})}
function openNamoro(){const ini=inicioNamoro();
 openSheet(`<div class="sh-head"><h2>Nosso namoro</h2><button type="button" class="tool" data-close aria-label="Fechar">${I.close}</button></div>
 <section class="card col" style="align-items:center;text-align:center;gap:4px"><span class="hand" style="font-size:34px">${esc(tempoNamoro(ini))}</span><small>juntos desde ${esc(longDate(ini))}</small></section>
 <form id="namf" class="stack"><div class="field"><label for="namd">Começo do namoro</label><input id="namd" type="date" value="${ini}" required></div>
 <p class="fine" style="text-align:left;margin:0">Todo mês, no dia ${Number(ini.slice(8))}, vocês recebem o aviso do mesversário. No aniversário de namoro o aviso é especial, com lembretes 13 dias e 1 dia antes.</p>
 <button type="submit" class="btn primary block">Salvar</button></form>`,
 ()=>{$('#namf').addEventListener('submit',async e=>{e.preventDefault();const v=$('#namd').value;if(!/^\d{4}-\d{2}-\d{2}$/.test(v)){toast('Escolha uma data.');return}
  try{await S.db.doc('casal/config').update({inicio:v});toast('Data salva.');backOrClose()}catch(err){handleErr(err)}})},null,{label:'Namoro',reopen:openNamoro})}
function openNotif(){const st=window.bilhetePushStatus(),pr=S.prefs||{},on=k=>pr[k]!==false;
 openSheet(`<div class="sh-head"><h2>Notificações</h2><button type="button" class="tool" data-close aria-label="Fechar">${I.close}</button></div>
 <section class="card col" style="gap:8px"><b>${esc(pushTxt())}</b><small>${st==='granted'?'Você recebe os avisos mesmo com o app fechado.':st==='instalar'?'Abra o Bilhete pelo ícone da Tela de Início e volte aqui.':st==='denied'?'Libere em Ajustes › Notificações › Bilhete.':'Toque para permitir os avisos neste iPhone.'}</small>
 ${st==='granted'||st==='default'?`<button type="button" class="btn ${st==='granted'?'ghost':'primary'} block" id="pushbtn">${st==='granted'?'Reconectar este aparelho':'Ativar notificações'}</button>`:''}</section>
 <div class="field"><span class="lbl">O que avisar</span>
 <label class="ck"><input type="checkbox" checked disabled>Bilhetes, amei, listas, humor e pergunta do dia</label>
 <label class="ck"><input type="checkbox" data-pref="datas"${on('datas')?' checked':''}>Mesversário e aniversário de namoro</label>
 <label class="ck"><input type="checkbox" data-pref="lembrete20"${on('lembrete20')?' checked':''}>Lembrete às 20h se eu ainda não mandei nada no dia</label></div>
 <div class="rows">${mrow(I.info,'Diagnóstico','Conexão, presença e teste de notificação','data-page="diag"')}</div>`,
 ()=>{const b=$('#pushbtn');if(b)b.addEventListener('click',async()=>{b.disabled=true;const r=await window.bilhetePush().catch(e=>({msg:'Não deu para ativar: '+(e&&e.message||e)}));b.disabled=false;toast(r.msg);if(r.ok){closeSheet();openNotif()}});
  $('#sheet').querySelectorAll('[data-pref]').forEach(c=>c.addEventListener('change',async()=>{const np={...(S.prefs||{}),[c.dataset.pref]:c.checked};S.prefs=np;try{await S.db.doc('prefs/'+S.me).set(np)}catch(err){handleErr(err)}}))},null,{label:'Notificações',reopen:openNotif})}
async function openDiag(){openSheet(`<div class="sh-head"><h2>Diagnóstico</h2><button type="button" class="tool" data-close aria-label="Fechar">${I.close}</button></div><div id="dgbox"><p class="fine">Verificando…</p></div>
 <button type="button" class="btn primary block" id="dgtest">Enviar notificação de teste</button><div id="dgres"></div>`,
 ()=>{const ok=(c,t,d)=>`<div class="dgr ${c?'ok':'no'}"><span aria-hidden="true">${c?'✓':'!'}</span><div><b>${t}</b>${d?`<small>${d}</small>`:''}</div></div>`;
  window.bilheteDiag().then(r=>{const P=esc(nick(other())),mine=r.atividades.find(a=>a.by===S.me&&Date.now()-a.at>45000),ent=mine?mine.pushed:null;
   $('#dgbox').innerHTML=ok(r.conectado,'Conexão em tempo real',r.conectado?'Conectado':'Sem conexão. Confira a internet e reabra o app.')
   +ok(r.canal==='joined','Canal de presença',r.canal==='joined'?'Ativo ('+(r.modo==='private'?'privado':'público')+')':'Estado: '+esc(r.canal)+(r.ultimoErro?' · '+esc(r.ultimoErro):''))
   +ok(true,'Quem está online agora',r.online.length?esc(r.online.join(', ')):P+' não está com o app aberto')
   +ok(r.push==='granted','Permissão de notificação',esc(pushTxt()))
   +ok(r.aparelhoInscrito&&r.inscricoesNoBanco>0,'Este aparelho inscrito',r.aparelhoInscrito?(r.inscricoesNoBanco?'Sim, salvo no banco':'Inscrito, mas não salvo no banco. Toque em Reconectar.'):'Não. Toque em Ativar em Notificações.')
   +ok(ent!==false,'Entrega da sua última atividade',ent===null?'Ainda sem atividade sua para conferir':ent?'A função recebeu e processou':'A função não processou. Confira se “Verify JWT” está desligado na função notificar.')}).catch(e=>{$('#dgbox').innerHTML='<p class="fine">Não deu para verificar: '+esc(String(e&&e.message||e))+'</p>'});
  $('#dgtest').addEventListener('click',async()=>{const bt=$('#dgtest');bt.disabled=true;bt.textContent='Enviando…';const r=await window.bilheteTestePush();bt.disabled=false;bt.textContent='Enviar notificação de teste';
   let h='';if(r.status===0)h=ok(false,'Função inacessível',esc(r.erro));else if(r.status===404)h=ok(false,'Função não encontrada','Confira se ela se chama exatamente notificar.');else if(r.status===401&&!r.segredos)h=ok(false,'Função recusou o pedido','Atualize o código da função notificar no Supabase (versão com teste).');else if(r.segredos){const falta=Object.entries(r.segredos).filter(([k,v])=>!v&&k!=='ANTHROPIC_API_KEY').map(([k])=>k);
    h=ok(!falta.length,'Secrets da função',falta.length?'Faltando: '+esc(falta.join(', ')):'Todos configurados')+(r.envios&&r.envios.length?r.envios.map(e=>ok(e.ok,'Envio para '+esc(e.aparelho),e.ok?'Enviado. Deve aparecer em segundos.':'Falhou'+(e.status?' ('+e.status+')':'')+': '+esc(e.erro||''))).join(''):ok(false,'Nenhum aparelho seu inscrito','Ative as notificações neste iPhone primeiro.'))}else h=ok(false,'Resposta inesperada',esc(JSON.stringify(r).slice(0,200)));
   $('#dgres').innerHTML=h})},null,{label:'Diagnóstico',reopen:openDiag})}
function openPage(n){if(n==='perfil')openProfile();else if(n==='namoro')openNamoro();else if(n==='notif')openNotif();else if(n==='diag')openDiag()}
""" + s[j:]
rep("async function afterSend(carta,title){", "async function afterSend(carta,title){return;")
rep("Ligado à sua conta Claude. Fica fixo neste perfil.", "Ligado ao seu login. Fica fixo neste perfil.")
# pergunta do dia gerada pela IA (quando existir)
rep("function perguntaHoje(){", "function perguntaHoje(){if(S.qia&&S.qia.date===today()&&S.qia.q)return S.qia.q;")
rep("  S.respUnsub=S.db.collection('perguntas')", "  if(S.qiaUnsub)S.qiaUnsub();S.qiaUnsub=S.db.doc('sistema/pergunta-'+t).onSnapshot(d=>{const v=d.exists?d.data():null;S.qia=v&&typeof v.q==='string'?{date:t,q:v.q.slice(0,200)}:null;const b=document.querySelector('[data-hsec=pergunta]');if(b&&S.view==='hoje'&&!(document.activeElement&&document.activeElement.id==='pqin')&&!(S.resp&&S.resp[S.me]))b.innerHTML=perguntaHtml()},()=>{});\n  S.respUnsub=S.db.collection('perguntas')")

# ---------- telas inteiras: Datas especiais e Notificações ----------
rep("""data-dedit="${esc(x.id)}"`)}).join('')}</div>`}""", """data-dview="${esc(x.id)}"`)}).join('')}</div>`}""")
rep("S.view==='sequencia'?viewSeq():viewHoje()", "S.view==='sequencia'?viewSeq():S.view==='datasv'?viewDatasV():S.view==='notifv'?viewNotifV():viewHoje()")
rep("if('datas' in t.dataset){openDatas();return}", "if('datas' in t.dataset){openView('datasv');return}\n if('vback' in t.dataset){go(S.viewBack||'hoje');return}")
rep("[data-hday],", "[data-hday],[data-vback],")
rep("function openPage(n){if(n==='perfil')openProfile();else if(n==='namoro')openNamoro();else if(n==='notif')openNotif();else if(n==='diag')openDiag()}",
r"""function openPage(n){if(n==='perfil')openProfile();else if(n==='namoro'||n==='datas')openView('datasv');else if(n==='notif'||n==='diag')openView('notifv')}
const VIEWS_X=['contagem','sequencia','datasv','notifv'];
function openView(v){closeSheet();if(S.view==='desenhar')leaveDraw();if(!VIEWS_X.includes(S.view))S.viewBack=S.view;S.view=v;render();pushPresence();window.scrollTo(0,0)}
function viewDatasV(){const ini=inicioNamoro();
 return `<header class="dtop"><button type="button" class="btn back" data-vback>${I.back}Voltar</button><h1>Datas especiais</h1><span></span></header>
 <section class="card col namv" aria-label="Nosso namoro"><small>Nosso namoro</small><span class="hand namt">${esc(tempoNamoro(ini))}</span><small>juntos desde ${esc(longDate(ini))}</small>
 <form id="namf2" class="namf" autocomplete="off"><div class="field"><label for="namd2">Começo do namoro</label><input id="namd2" type="date" value="${ini}" required></div><button type="submit" class="btn ghost">Salvar</button></form>
 <p class="fine" style="text-align:left;margin:0">Aviso todo dia ${Number(ini.slice(8))} às 9h. No aniversário de namoro, aviso especial com lembretes 13 dias e 1 dia antes.</p></section>
 <button type="button" class="btn primary block" data-dedit="">${I.cal}Nova data</button>
 <section aria-label="Datas criadas"><h2 class="vsec">Próximas datas</h2><div id="dlist">${datasListHtml()}</div><p class="fine">Toque numa data para ver a contagem em tela cheia e editar.</p></section>`}
function dgRow(c,t,d){return `<div class="dgr ${c?'ok':'no'}"><span aria-hidden="true">${c?'✓':'!'}</span><div><b>${t}</b>${d?`<small>${d}</small>`:''}</div></div>`}
function viewNotifV(){const pr=S.prefs||{},on=k=>pr[k]!==false;setTimeout(initNotifV,0);
 return `<header class="dtop"><button type="button" class="btn back" data-vback>${I.back}Voltar</button><h1>Notificações</h1><span></span></header>
 <section class="card nst"><div><b>Neste iPhone</b><small id="nstx">Verificando…</small></div><button type="button" class="sw2" id="pushsw" role="switch" aria-checked="false" aria-label="Notificações neste aparelho" disabled><span></span></button></section>
 <section class="card col" aria-label="O que avisar"><b>O que avisar</b>
 <label class="ck"><input type="checkbox" checked disabled>Bilhetes, amei, listas, humor e pergunta do dia</label>
 <label class="ck"><input type="checkbox" data-pref="datas"${on('datas')?' checked':''}>Mesversário e aniversário de namoro (9h)</label>
 <label class="ck"><input type="checkbox" data-pref="lembrete20"${on('lembrete20')?' checked':''}>Lembrete às 20h se eu ainda não mandei nada no dia</label></section>
 <section class="card col" aria-label="Testar"><b>Testar</b><small>Manda uma notificação para este iPhone e mostra o resultado.</small><button type="button" class="btn ghost block" id="dgtest">Enviar notificação de teste</button><div id="dgres"></div></section>
 <details class="card col dgdet"><summary>Diagnóstico da conexão</summary><div id="dgbox"><p class="fine">Verificando…</p></div></details>`}
async function nstUpdate(){const st=window.bilhetePushStatus(),at=await window.bilhetePushAtivo(),sw=$('#pushsw'),tx=$('#nstx');if(!sw||!tx)return;
 sw.setAttribute('aria-checked',String(at));sw.disabled=st==='denied'||st==='instalar'||st==='sem-suporte';
 tx.textContent=at?'Ativadas: você recebe avisos mesmo com o app fechado.':st==='denied'?'Bloqueadas. Libere em Ajustes › Notificações › Bilhete.':st==='instalar'?'Abra o Bilhete pelo ícone da Tela de Início para ativar.':st==='sem-suporte'?'Este navegador não aceita notificações.':'Desativadas neste aparelho.'}
function initNotifV(){if(S.view!=='notifv')return;nstUpdate();
 const sw=$('#pushsw');if(sw)sw.onclick=async()=>{sw.disabled=true;const on=sw.getAttribute('aria-checked')==='true';const r=on?await window.bilhetePushOff():await window.bilhetePush().catch(e=>({msg:'Não deu para ativar: '+(e&&e.message||e)}));toast(r.msg);await nstUpdate();sw.disabled=false};
 const bt=$('#dgtest');if(bt)bt.onclick=async()=>{bt.disabled=true;bt.textContent='Enviando…';const r=await window.bilheteTestePush();bt.disabled=false;bt.textContent='Enviar notificação de teste';let h='';
  if(r.status===0)h=dgRow(false,'Função inacessível',esc(r.erro));else if(r.status===404)h=dgRow(false,'Função não encontrada','Confira o nome da função no Supabase.');else if(r.segredos){const falta=Object.entries(r.segredos).filter(([k,v])=>!v&&k!=='ANTHROPIC_API_KEY').map(([k])=>k);
   h=(falta.length?dgRow(false,'Secrets da função','Faltando: '+esc(falta.join(', '))):'')+(r.envios&&r.envios.length?r.envios.map(e=>dgRow(e.ok,'Envio para '+esc(e.aparelho),e.ok?'Enviado. Deve aparecer em segundos.':'Falhou'+(e.status?' ('+e.status+')':'')+': '+esc(e.erro||''))).join(''):dgRow(false,'Nenhum aparelho seu inscrito','Ative as notificações acima.'))}else h=dgRow(false,'Resposta inesperada',esc(JSON.stringify(r).slice(0,200)));
  const el=$('#dgres');if(el)el.innerHTML=h};
 const det=$('.dgdet');if(det)det.addEventListener('toggle',()=>{if(!det.open)return;window.bilheteDiag().then(r=>{const P=esc(nick(other())),mine=r.atividades.find(a=>a.by===S.me&&Date.now()-a.at>45000),ent=mine?mine.pushed:null;const box=$('#dgbox');if(!box)return;
  box.innerHTML=dgRow(r.conectado,'Conexão em tempo real',r.conectado?'Conectado':'Sem conexão')+dgRow(r.canal==='joined','Canal de presença',r.canal==='joined'?'Ativo ('+(r.modo==='private'?'privado':'público')+')':'Estado: '+esc(r.canal))+dgRow(true,'Online agora',r.online.length?esc(r.online.join(', ')):P+' não está com o app aberto')+dgRow(r.aparelhoInscrito&&r.inscricoesNoBanco>0,'Este aparelho inscrito',r.aparelhoInscrito?(r.inscricoesNoBanco?'Sim, salvo no banco':'Inscrito, mas não salvo no banco'):'Não')+dgRow(ent!==false,'Entrega da sua última atividade',ent===null?'Sem atividade recente para conferir':ent?'Processada pela função':'Ainda não processada')})})}
document.addEventListener('change',async e=>{const c=e.target.closest&&e.target.closest('[data-pref]');if(!c||!S.db)return;const np={...(S.prefs||{}),[c.dataset.pref]:c.checked};S.prefs=np;try{await S.db.doc('prefs/'+S.me).set(np);toast('Preferência salva.')}catch(err){handleErr(err)}});
document.addEventListener('submit',async e=>{if(e.target.id!=='namf2')return;e.preventDefault();const v=$('#namd2').value;if(!/^\d{4}-\d{2}-\d{2}$/.test(v)){toast('Escolha uma data.');return}try{await S.db.doc('casal/config').update({inicio:v});S.config={...(S.config||{}),inicio:v};toast('Data salva.');if(S.view==='datasv')render()}catch(err){handleErr(err)}});
""")
rep("""${mgrp('Nós dois',[mrow(I.heart(false),'Nosso namoro',esc(tempoNamoro(ini))+' · desde '+esc(shortDate(ini)),'data-page="namoro"'),mrow(I.cal,'Datas especiais',nx?esc((diffDays(nx.date)===0?'Hoje: ':'Próxima: ')+nx.title+' · '+shortDate(nx.date)):'Aniversários, viagens e contagens','data-datas')])}""",
"""${mgrp('Nós dois',[mrow(I.cal,'Datas especiais',esc(tempoNamoro(ini))+' de namoro'+(nx?' · próxima: '+esc(nx.title):''),'data-datas')])}""")
rep("</head>", "<style>.namv{align-items:center;text-align:center;gap:4px}.namt{font-size:38px;line-height:1.1}.namf{display:flex;gap:8px;align-items:flex-end;width:100%;margin-top:10px;text-align:left}.namf .field{flex:1;margin:0}.vsec{font-size:18px;margin:18px 0 8px}.nst{display:flex;align-items:center;gap:12px;justify-content:space-between}.nst small{display:block;color:var(--muted)}.sw2{flex:none;width:56px;height:34px;border-radius:999px;border:0;background:#D9D0BE;position:relative;cursor:pointer;padding:0}.sw2 span{position:absolute;top:3px;left:3px;width:28px;height:28px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);transition:left .2s}.sw2[aria-checked=true]{background:#4C7A4C}.sw2[aria-checked=true] span{left:25px}.sw2:disabled{opacity:.5}.dgdet summary{cursor:pointer;font-weight:700}.dgdet[open] summary{margin-bottom:10px}.updbar{position:fixed;left:12px;right:12px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:60;display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:16px;background:#262C45;color:#fff;box-shadow:0 8px 24px rgba(0,0,0,.25)}.updbar b{flex:1;font-size:15px}.updbar button{border:0;border-radius:12px;padding:10px 14px;font:inherit;font-weight:700;background:#DCCD8B;color:#262C45}</style></head>")
# service worker (necessário para instalar e, depois, para notificações)
rep('</head>','<style>.dgr{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-radius:12px;background:var(--surface);margin-bottom:6px}.dgr>span{flex:none;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:13px;color:#fff;background:#4C7A4C}.dgr.no>span{background:#B57056}.dgr small{display:block;color:var(--muted)}#dgres{margin-top:10px}</style></head>')
rep('</body>', '''<script>if('serviceWorker' in navigator)window.addEventListener('load',()=>{const had=!!navigator.serviceWorker.controller;
navigator.serviceWorker.register('sw.js').then(reg=>{const chk=()=>reg.update().catch(()=>{});document.addEventListener('visibilitychange',()=>{if(!document.hidden)chk()});setInterval(chk,30*60e3);
 reg.addEventListener('updatefound',()=>{const w=reg.installing;if(w)w.addEventListener('statechange',()=>{if(w.state==='activated'&&had&&!document.getElementById('updbar')){const d=document.createElement('div');d.id='updbar';d.className='updbar';d.setAttribute('role','status');d.innerHTML='<b>Nova versão do Bilhete pronta</b><button type="button">Atualizar</button>';d.querySelector('button').onclick=()=>location.reload();document.body.appendChild(d)}})})}).catch(()=>{})});</script>
</body>''')

import time as _t
BUILD_V = str(int(_t.time()))
s = s.replace('src="config.js"', 'src="config.js?v=' + BUILD_V + '"').replace('src="supa.js"', 'src="supa.js?v=' + BUILD_V + '"')
pathlib.Path('index.html').write_text(s, encoding='utf-8')
print('ok', len(s))
