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

# Mais: importar backup antigo + sair
rep("""${mgrp('Seus dados',[mrow(I.dl,'Exportar backup','Baixa um arquivo .json com bilhetes, fotos, listas e conversas','id="backupbtn"')])}""",
    """${mgrp('Seus dados',[mrow(I.dl,'Exportar backup','Baixa um arquivo .json com bilhetes, fotos, listas e conversas','id="backupbtn"'),mrow(I.dl,'Importar backup','Traz os bilhetes do app antigo (arquivo .json)','id="importbtn"'),mrow(I.back,'Sair desta conta','Neste aparelho','id="sairbtn"')])}${mgrp('No celular',[mrow(I.bell,'Notificações no celular',({granted:'Ativadas neste aparelho',denied:'Bloqueadas nos Ajustes do iPhone',instalar:'Instale na Tela de Início primeiro','sem-suporte':'Este navegador não aceita'})[window.bilhetePushStatus()]||'Avisa quando chegar bilhete, mesmo com o app fechado','id="pushbtn"')])}<input type="file" id="importin" accept="application/json,.json" hidden>""")
rep("""()=>{$('#backupbtn').addEventListener('click',exportBackup)}""",
    """()=>{$('#backupbtn').addEventListener('click',exportBackup);$('#pushbtn').addEventListener('click',async()=>{toast('Ativando…');const r=await window.bilhetePush().catch(e=>({msg:'Não deu para ativar: '+(e&&e.message||e)}));toast(r.msg);if(r.ok)backOrClose()});$('#sairbtn').addEventListener('click',()=>confirmSheet('Sair da conta neste aparelho?','Sair',()=>window.bilheteSair()));
  $('#importbtn').addEventListener('click',()=>$('#importin').click());$('#importin').addEventListener('change',async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;
   try{const txt=await f.text();toast('Importando…');const n=await window.bilheteImportar(txt,(d,t)=>{if(d===t||d%100===0)toast('Importando… '+d+' de '+t)});toast(n+' itens importados. Recarregando…');setTimeout(()=>location.reload(),1500)}catch(err){toast(err&&err.message?err.message:'Não deu para importar.')}})}""")

# service worker (necessário para instalar e, depois, para notificações)
rep('</body>', '''<script>if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>
</body>''')

pathlib.Path('index.html').write_text(s, encoding='utf-8')
print('ok', len(s))
