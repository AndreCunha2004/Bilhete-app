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
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
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
 <label class="ck"><input type="checkbox" data-pref="lembrete20"${on('lembrete20')?' checked':''}>Lembrete às 20h se eu ainda não mandei nada no dia</label></div>`,
 ()=>{const b=$('#pushbtn');if(b)b.addEventListener('click',async()=>{b.disabled=true;const r=await window.bilhetePush().catch(e=>({msg:'Não deu para ativar: '+(e&&e.message||e)}));b.disabled=false;toast(r.msg);if(r.ok){closeSheet();openNotif()}});
  $('#sheet').querySelectorAll('[data-pref]').forEach(c=>c.addEventListener('change',async()=>{const np={...(S.prefs||{}),[c.dataset.pref]:c.checked};S.prefs=np;try{await S.db.doc('prefs/'+S.me).set(np)}catch(err){handleErr(err)}}))},null,{label:'Notificações',reopen:openNotif})}
function openPage(n){if(n==='perfil')openProfile();else if(n==='namoro')openNamoro();else if(n==='notif')openNotif()}
""" + s[j:]
rep("async function afterSend(carta,title){", "async function afterSend(carta,title){return;")
rep("Ligado à sua conta Claude. Fica fixo neste perfil.", "Ligado ao seu login. Fica fixo neste perfil.")
# pergunta do dia gerada pela IA (quando existir)
rep("function perguntaHoje(){", "function perguntaHoje(){if(S.qia&&S.qia.date===today()&&S.qia.q)return S.qia.q;")
rep("  S.respUnsub=S.db.collection('perguntas')", "  if(S.qiaUnsub)S.qiaUnsub();S.qiaUnsub=S.db.doc('sistema/pergunta-'+t).onSnapshot(d=>{const v=d.exists?d.data():null;S.qia=v&&typeof v.q==='string'?{date:t,q:v.q.slice(0,200)}:null;const b=document.querySelector('[data-hsec=pergunta]');if(b&&S.view==='hoje'&&!(document.activeElement&&document.activeElement.id==='pqin')&&!(S.resp&&S.resp[S.me]))b.innerHTML=perguntaHtml()},()=>{});\n  S.respUnsub=S.db.collection('perguntas')")

# service worker (necessário para instalar e, depois, para notificações)
rep('</body>', '''<script>if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>
</body>''')

pathlib.Path('index.html').write_text(s, encoding='utf-8')
print('ok', len(s))
