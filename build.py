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
const TEMAS=['claro','sistema','escuro'];
function temaSwitch(v){const i=Math.max(0,TEMAS.indexOf(v));return `<div class="tsw" role="radiogroup" aria-label="Tema" style="--i:${i}"><span class="tth" aria-hidden="true"></span>${[['claro','Claro',I.tsun],['sistema','Igual ao iPhone',I.tsys],['escuro','Escuro',I.tmoon]].map(([k,l,ic],j)=>`<button type="button" role="radio" aria-checked="${j===i}" aria-label="${l}" data-tv="${k}">${ic}</button>`).join('')}</div>`}
function initTemaSwitch(sw,cb){if(!sw)return;const W=()=>sw.querySelector('button').offsetWidth;let i=Number(getComputedStyle(sw).getPropertyValue('--i'))||0,drag=null;
 const set=(j,fire)=>{j=Math.max(0,Math.min(2,j));sw.style.removeProperty('--x');sw.classList.remove('arr');sw.style.setProperty('--i',j);sw.querySelectorAll('button').forEach((b,k)=>b.setAttribute('aria-checked',String(k===j)));if(fire&&j!==i){i=j;if(navigator.vibrate)try{navigator.vibrate(8)}catch(_){}cb(TEMAS[j])}};
 sw.addEventListener('pointerdown',e=>{drag={x0:e.clientX,moved:false,base:i*W()};try{sw.setPointerCapture(e.pointerId)}catch(_){}});
 sw.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x0;if(Math.abs(dx)>4)drag.moved=true;if(!drag.moved)return;e.preventDefault();sw.classList.add('arr');sw.style.setProperty('--x',Math.max(0,Math.min(2*W(),drag.base+dx))+'px')});
 const up=e=>{if(!drag)return;const d=drag;drag=null;if(d.moved){const x=Math.max(0,Math.min(2*W(),d.base+e.clientX-d.x0));set(Math.round(x/W()),true)}else{const b=document.elementFromPoint(e.clientX,e.clientY);const bt=b&&b.closest&&b.closest('.tsw [data-tv]');if(bt)set(TEMAS.indexOf(bt.dataset.tv),true)}};
 sw.addEventListener('pointerup',up);sw.addEventListener('pointercancel',()=>{drag=null;set(i)});
 sw.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();set(i+(e.key==='ArrowRight'?1:-1),true);sw.querySelectorAll('button')[i].focus()}});
 sw.addEventListener('click',e=>e.stopPropagation())}
function temaAtual(){return (S.prefs&&S.prefs.tema)||window.bilheteTemaLocal()}
function openMais(){const nx=nextData(),ini=inicioNamoro(),tm=temaAtual();
 openSheet(`<div class="sh-head"><h2>Configurações</h2><button type="button" class="tool" data-close aria-label="Fechar">${I.close}</button></div>
 <button type="button" class="card who prof" data-page="perfil" aria-label="Seu perfil: ${esc(nick(S.me))}"><span class="av ${S.me}" aria-hidden="true">${esc(initial(nick(S.me)))}</span><div><b>${esc(nick(S.me))}</b><small>Entrou como ${esc(window.bilheteUser||'')}</small></div>${I.chev}</button>
 <section class="grp" aria-label="Aparência"><h3>Aparência</h3><div class="rows"><div class="rowb trow"><span class="ic" aria-hidden="true">${I.tsun}</span><div><b>Tema</b><small id="ttx">${({claro:'Claro',escuro:'Escuro',sistema:'Igual ao iPhone'})[tm]}</small></div>${temaSwitch(tm)}</div></div></section>
 ${mgrp('Início',[mrow(I.grip,'Organizar o Início','Ou arraste pelo ícone no canto de cada bloco','data-org')])}
 ${mgrp('Nós dois',[mrow(I.heart(false),'Nosso namoro',esc(tempoNamoro(ini))+' · desde '+esc(shortDate(ini)),'data-page="namoro"'),mrow(I.cal,'Datas especiais',nx?esc((diffDays(nx.date)===0?'Hoje: ':'Próxima: ')+nx.title+' · '+shortDate(nx.date)):'Aniversários, viagens e contagens','data-datas')])}
 ${mgrp('Avisos',[mrow(I.bell,'Notificações',esc(pushTxt()),'data-page="notif"')])}
 ${mgrp('Seus dados',[mrow(I.dl,'Exportar backup','Arquivo .json com tudo de vocês','id="backupbtn"'),mrow(I.dl,'Importar backup','Traz um arquivo exportado antes','id="importbtn"')])}
 ${mgrp('Conta',[mrow(I.back,'Sair desta conta','Só neste aparelho','id="sairbtn"')])}<input type="file" id="importin" accept="application/json,.json" hidden>`,
 ()=>{$('#backupbtn').addEventListener('click',exportBackup);$('#sairbtn').addEventListener('click',()=>confirmSheet('Sair da conta neste aparelho?','Sair',()=>window.bilheteSair()));
  $('#importbtn').addEventListener('click',()=>$('#importin').click());$('#importin').addEventListener('change',async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;
   try{const txt=await f.text();toast('Importando…');const n=await window.bilheteImportar(txt,(d,t)=>{if(d===t||d%100===0)toast('Importando… '+d+' de '+t)});toast(n+' itens importados. Recarregando…');setTimeout(()=>location.reload(),1500)}catch(err){toast(err&&err.message?err.message:'Não deu para importar.')}})
  initTemaSwitch($('#sheet .tsw'),async v=>{const tx=$('#ttx');if(tx)tx.textContent=({claro:'Claro',escuro:'Escuro',sistema:'Igual ao iPhone'})[v];window.bilheteTema(v);const np={...(S.prefs||{}),tema:v};S.prefs=np;try{await S.db.doc('prefs/'+S.me).set(np)}catch(err){handleErr(err)}})},null,{label:'Configurações',reopen:openMais})}
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
rep("const I={grip:", "const I={tsun:sv('<circle cx=\"12\" cy=\"12\" r=\"4\"/><path d=\"M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4\"/>'),tmoon:sv('<path d=\"M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z\"/>'),tsys:sv('<rect x=\"3\" y=\"4\" width=\"18\" height=\"12\" rx=\"2\"/><path d=\"M8 20h8M12 16v4\"/>'),menu:sv('<path d=\"M4 7h16M4 12h16M4 17h16\"/>'),gear:sv('<circle cx=\"12\" cy=\"12\" r=\"3\"/><path d=\"M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z\"/>'),grip:")
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


# ---------- barra: engrenagem de Configurações no lugar de "Mais" ----------
GEAR='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>'
i = s.index('<button type="button" data-mais>'); j = s.index('</button>', i) + 9
MENU='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
s = s[:i] + '<button type="button" data-menu aria-label="Abrir o menu" aria-controls="lateral" aria-expanded="false">' + MENU + 'Menu</button>' + s[j:]
# menu lateral de vidro (igual ao Recanto) logo depois da barra
rep('<div class="sheet" id="sheet" hidden></div>', '<div class="veu" id="veu" hidden></div><aside class="lateral" id="lateral" aria-label="Menu" inert></aside>\n<div class="sheet" id="sheet" hidden></div>')
rep("let lpT=0,lpXY=null;", r'''function drawerHtml(){const it=(ic,t,attr,cur)=>`<button type="button" class="litem" ${attr}${cur?' aria-current="page"':''}>${ic}<span>${t}</span></button>`,v=S.view;
 return `<div class="lhead">${logo(30)}<div><b>Bilhete</b><small>${esc(nick('a'))} & ${esc(nick('b'))}</small></div></div>
 <nav class="lnav" aria-label="Seções">${it(I.home,'Início','data-go="hoje"',v==='hoje')}${it(I.grid,'Mural','data-go="mural"',v==='mural')}${it(I.list,'Listas','data-go="listas"',v==='listas')}
 <div class="lsep"></div>${it(I.flame,'Sequência','data-mural-cal',v==='sequencia')}${it(I.cal,'Datas especiais','data-datas',v==='datasv')}${it(I.bell,'Notificações','data-page="notif"',v==='notifv')}${it(I.grip,'Organizar o Início','data-org')}</nav>
 <div class="lfoot"><button type="button" class="litem lme" data-mais><span class="av ${S.me}" aria-hidden="true">${esc(initial(nick(S.me)))}</span><span>${esc(nick(S.me))}<small>Entrou como ${esc(window.bilheteUser||'')}</small></span></button>${it(I.gear,'Configurações','data-mais')}</div>`}
function drawer(open){const L=$('#lateral'),V=$('#veu'),b=document.querySelector('[data-menu]');if(!L)return;if(open){L.innerHTML=drawerHtml();L.removeAttribute('inert');V.hidden=false;requestAnimationFrame(()=>{L.classList.add('aberta');V.classList.add('on')});document.body.classList.add('menu-aberto')}
 else{L.classList.remove('aberta');V.classList.remove('on');L.setAttribute('inert','');document.body.classList.remove('menu-aberto');setTimeout(()=>{if(!L.classList.contains('aberta'))V.hidden=true},240)}if(b)b.setAttribute('aria-expanded',String(!!open))}
document.addEventListener('click',e=>{const m=e.target.closest&&e.target.closest('[data-menu]');if(m){drawer(!$('#lateral').classList.contains('aberta'));return}
 if(e.target.id==='veu'){drawer(false);return}const li=e.target.closest&&e.target.closest('#lateral .litem');if(li)setTimeout(()=>drawer(false),0)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('#lateral').classList.contains('aberta')){e.stopImmediatePropagation();drawer(false)}},true);
{let sx=null;document.addEventListener('pointerdown',e=>{sx=e.target.closest&&e.target.closest('#lateral')?e.clientX:null});document.addEventListener('pointerup',e=>{if(sx!==null&&sx-e.clientX>60)drawer(false);sx=null})}
let lpT=0,lpXY=null;''')
rep("</head>", pathlib.Path(__file__).with_name('menu.css').read_text(encoding='utf-8')+"</head>")
s = s.replace('(dá pra voltar em Mais)', '(dá pra voltar em Configurações)')

# ---------- tema travado por usuário (Claro / Escuro / Sistema) ----------
rep('<meta name="theme-color" content="#F5F0E6">', """<meta name="theme-color" content="#F5F0E6" id="themecolor">
<script>(function(){var mq=window.matchMedia?matchMedia('(prefers-color-scheme: dark)'):null;
function cor(){var r=document.documentElement,d=r.dataset.theme==='dark'||(!r.dataset.theme&&mq&&mq.matches),m=document.getElementById('themecolor');if(m)m.setAttribute('content',d?'#17181F':'#F5F0E6')}
window.bilheteTemaLocal=function(){try{return localStorage.getItem('bilhete-tema')||'sistema'}catch(e){return 'sistema'}};
window.bilheteTema=function(t){t=t==='claro'||t==='escuro'?t:'sistema';var r=document.documentElement;if(t==='sistema')delete r.dataset.theme;else r.dataset.theme=t==='escuro'?'dark':'light';try{localStorage.setItem('bilhete-tema',t)}catch(e){}cor()};
window.bilheteTema(window.bilheteTemaLocal());if(mq&&mq.addEventListener)mq.addEventListener('change',cor);document.addEventListener('DOMContentLoaded',cor)})();</script>""")
rep("S.prefs=p||{};if(S.view==='hoje'&&$('#sheet').hidden)render()", "S.prefs=p||{};if(S.prefs.tema)window.bilheteTema(S.prefs.tema);if(S.view==='hoje'&&$('#sheet').hidden)render()")

# ---------- Início: arrastar os blocos pelo ícone do canto, em tempo real ----------
rep("""${homeOrder().filter(k=>sec[k]).map(k=>`<div class="hsec" data-hsec="${k}">${sec[k]}</div>`).join('')}""",
    """${homeOrder().filter(k=>sec[k]).map(k=>`<div class="hsec" data-hsec="${k}">${sec[k]}<button type="button" class="hgrab" data-hgrab aria-label="Mover ${esc((HSEC.find(h=>h[0]===k)||[k,k])[1])} (arraste)">${I.grip}</button></div>`).join('')}""")
rep("function render(){const v=$('#view');", "function render(){if(S.hdrag){S.hdragPend=1;return}const v=$('#view');")
rep("document.addEventListener('pointerdown',e=>{const h=e.target.closest('[data-hsec]');if(!h||", "document.addEventListener('pointerdown',e=>{const h=e.target.closest('[data-hsec]');if(!h||e.target.closest('[data-hgrab]')||")
rep(".hsec{display:contents}", ".hsec{display:flex;flex-direction:column;gap:14px;position:relative}.hsec:has(>#cdbox:empty){display:none}")
rep("</head>", """<style>.hgrab{position:absolute;top:-9px;right:-7px;z-index:3;width:30px;height:30px;padding:0;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--muted);display:grid;place-items:center;cursor:grab;touch-action:none;box-shadow:0 1px 4px rgba(0,0,0,.12);opacity:.9}
.hgrab svg{width:16px;height:16px}.hgrab:active{cursor:grabbing}
.hsec.hlift{z-index:20;transition:none!important;filter:drop-shadow(0 14px 22px rgba(0,0,0,.22));cursor:grabbing}.hsec.hlift>*:not(.hgrab){transform:scale(1.02)}.hsec.hlift .hgrab{background:var(--brand);color:var(--surface);border-color:var(--brand)}
.hsec.hshift{transition:transform .2s cubic-bezier(.2,.8,.2,1)}body.hdragging{user-select:none;-webkit-user-select:none;overscroll-behavior:none}
.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px;border-radius:14px;background:var(--chip)}.seg button{border:0;border-radius:10px;min-height:40px;background:none;font:600 14px 'DM Sans',sans-serif;color:var(--muted);cursor:pointer}.seg button[aria-checked=true]{background:var(--surface);color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.14)}</style>
</head>""")
rep("let lpT=0,lpXY=null;", "(function(){let d=null;\nconst gap=()=>14,secs=()=>[...document.querySelectorAll('#view .hsec')];\nfunction down(e){const g=e.target.closest&&e.target.closest('[data-hgrab]');if(!g||e.button>0)return;e.preventDefault();const el=g.closest('.hsec'),all=secs(),i=all.indexOf(el);if(i<0)return;\n try{g.setPointerCapture(e.pointerId)}catch(_){}\n const rs=all.map(x=>x.getBoundingClientRect());\n d={g,el,all,i,to:i,rs,h:rs[i].height+gap(),y0:e.clientY+scrollY,y:e.clientY,raf:0};S.hdrag=1;el.classList.add('hlift');document.body.classList.add('hdragging');\n all.forEach(x=>{if(x!==el)x.classList.add('hshift')});if(navigator.vibrate)try{navigator.vibrate(10)}catch(_){}\n loop()}\nfunction place(){if(!d)return;const dy=d.y+scrollY-d.y0;d.el.style.transform=`translateY(${dy}px)`;\n const c=d.rs[d.i].top+d.rs[d.i].height/2+dy;let to=d.i;\n d.rs.forEach((r,k)=>{const m=r.top+r.height/2;if(k<d.i&&c<m&&k<to)to=k;if(k>d.i&&c>m)to=Math.max(to,k)});\n if(to!==d.to){d.to=to;if(navigator.vibrate)try{navigator.vibrate(5)}catch(_){}}\n d.all.forEach((x,k)=>{if(x===d.el)return;let t=0;if(d.i<k&&k<=d.to)t=-d.h;else if(d.to<=k&&k<d.i)t=d.h;x.style.transform=t?`translateY(${t}px)`:''})}\nfunction loop(){if(!d)return;const edge=70,vh=innerHeight;let v=0;if(d.y<edge)v=-Math.ceil((edge-d.y)/6);else if(d.y>vh-edge-80)v=Math.ceil((d.y-(vh-edge-80))/6);if(v)scrollBy(0,v);place();d.raf=requestAnimationFrame(loop)}\nfunction move(e){if(!d)return;e.preventDefault();d.y=e.clientY}\nasync function up(){if(!d)return;const D=d;d=null;cancelAnimationFrame(D.raf);\n const keys=D.all.map(x=>x.dataset.hsec),mv=keys.splice(D.i,1)[0];keys.splice(D.to,0,mv);\n const par=D.el.parentNode,ref=D.all[D.to<D.i?D.to:D.to+1]||null,r0=D.el.getBoundingClientRect();\n D.all.forEach(x=>{x.classList.remove('hshift');x.style.transform=''});\n if(D.to!==D.i)par.insertBefore(D.el,D.to<D.i?D.all[D.to]:(D.all[D.to].nextSibling));\n const r1=D.el.getBoundingClientRect();D.el.style.transform=`translateY(${r0.top-r1.top}px)`;D.el.getBoundingClientRect();\n D.el.classList.remove('hlift');D.el.classList.add('hshift');D.el.style.transform='';setTimeout(()=>D.el.classList.remove('hshift'),220);\n document.body.classList.remove('hdragging');\n S.hdrag=0;\n if(D.to!==D.i&&S.db&&S.me){const full=homeOrder(),vis=new Set(keys);let q=0;const ord=full.map(k=>vis.has(k)?keys[q++]:k);\n  S.prefs={...(S.prefs||{}),homeOrder:ord};try{await S.db.doc('prefs/'+S.me).set({...S.prefs,at:Date.now()})}catch(err){handleErr(err)}}\n if(S.hdragPend){S.hdragPend=0;setTimeout(render,240)}}\ndocument.addEventListener('pointerdown',down,true);document.addEventListener('pointermove',move,{passive:false});['pointerup','pointercancel'].forEach(t=>document.addEventListener(t,up));\ndocument.addEventListener('touchmove',e=>{if(d)e.preventDefault()},{passive:false});\ndocument.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-hgrab]')){e.preventDefault();e.stopPropagation()}},true)})();\nlet lpT=0,lpXY=null;")

import time as _t
BUILD_V = str(int(_t.time()))
s = s.replace('src="config.js"', 'src="config.js?v=' + BUILD_V + '"').replace('src="supa.js"', 'src="supa.js?v=' + BUILD_V + '"')
pathlib.Path('index.html').write_text(s, encoding='utf-8')
print('ok', len(s))
