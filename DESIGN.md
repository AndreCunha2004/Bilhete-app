---
version: alpha
name: Bilhete
description: App de casal para trocar desenhos, cartas e listas compartilhadas, com conversa por item.
colors:
  primary: "#475480"
  secondary: "#7F3B25"
  tertiary: "#B57056"
  success: "#A7993C"
  highlight: "#DCCD8B"
  neutral: "#F5F0E6"
  surface: "#FFFCF6"
  paper: "#F1E8C6"
  ink: "#262C45"
  muted: "#5E6274"
  on-primary: "#FFFFFF"
  on-secondary: "#FFFFFF"
typography:
  h1:
    fontFamily: DM Sans
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  body:
    fontFamily: DM Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: DM Sans
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
  hand:
    fontFamily: Caveat
    fontSize: 30px
    fontWeight: 500
    lineHeight: 1.05
  brand:
    fontFamily: Caveat
    fontSize: 30px
    fontWeight: 700
    lineHeight: 1
rounded:
  sm: 10px
  md: 14px
  lg: 22px
  full: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 14px
  lg: 20px
  xl: 28px
components:
  button-primary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.sm}"
  button-secondary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
  note-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  streak-pill:
    backgroundColor: "{colors.highlight}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
  page:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.ink}"
  chat-mine:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
  check-done:
    backgroundColor: "{colors.success}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  caption:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.muted}"
---

# Bilhete

## Overview

Um bilhete de papel deixado na mesa do café da manhã: louça azul, figos, cobre.
Terno e leve, nunca com cara de sistema. Fundo bege como papel; uma cor fria (Mozart)
segura a marca e a navegação, quatro quentes dão o tom de carinho. Paleta escolhida pelo
André e aprovada pela Maju — não trocar sem pedido.

## Colors

- **Mozart (primary #475480):** marca (logo, "Bilhete"), aba ativa, botão "Responder", minhas mensagens no chat, avatar de quem criou o par.
- **Roycroft Copper (secondary #7F3B25):** ação principal (Enviar, Criar, Adicionar, "+" central), links, aviso de mensagem nova, avatar do par.
- **Sunburn (tertiary #B57056):** afeto e tempo real: coração, chama da sequência, ponto "ao vivo", dias com troca.
- **Prickly Pear (success #A7993C):** "comprado". Nunca em texto.
- **Status do par:** bolinha verde padrão #2E9E5B (online) e vermelha padrão #D93025 (offline), fora da paleta de propósito, para não se confundir com os outros elementos.
- **Master Key (highlight #DCCD8B):** papel (versão clara #F1E8C6), sequência, resumo da lista, aba selecionada.
- Texto só em ink, muted, Mozart ou Copper. Sunburn, Prickly Pear e Master Key só como preenchimento.
- Pincel: as 5 cores + tinta, mais "Mais cores" (10 cores padrão, gradiente de matiz + claro/escuro, seletor nativo e recentes).

## Typography

DM Sans para interface; Caveat (letra de mão) para o conteúdo dos bilhetes, cartas e o nome "Bilhete".
Fontes hospedadas no próprio app (pasta fonts/, licença OFL), sem depender do Google Fonts.

## Layout

Coluna única de celular (máx. 520px). Barra superior fixa e quase opaca com logo + presença do par.
Sininho no topo com contador (Copper) das atualizações do outro; painel em folha inferior.
Barra inferior (64 px de altura, ícones 26 px): Início · Mural · (+ Novo central) · Listas · Mais. Detalhes e conversas abrem em folha inferior.

## Components

- Bilhete: cartão papel com título, desenho (máx. 440px de largura) e frase em Caveat.
- Item da lista: caixinha "comprado", nome, descrição, preço, autor e balão de conversa com contador (Copper quando há mensagem nova).
- Conversa: minhas mensagens em Mozart à direita, do par em papel à esquerda, "digitando…" abaixo.
- Desenho: no formulário a área ocupa ~84% da largura (laterais livres para rolar); botão ⤢ abre tela cheia com a barra completa e "Concluir".
- Calendário (página Nossa sequência): mapa de 4 semanas, dias com bilhete tocáveis (abrem os bilhetes do dia); intensidade por bilhetes no dia: 0 contorno, 1 Master Key, 2 Sunburn, 3+ Copper, número no dia, hoje com contorno Mozart.
- Sequência: "N dias seguidos" (dias em que os dois mandaram pelo menos um bilhete) + recorde.
- Foto no desenho: fundo recortado 10:11 e comprimido; o rabisco fica numa camada por cima (a borracha não apaga a foto). Botões "Usar foto da galeria" / "Remover foto".
- Tela Hoje: contagem regressiva (próxima data especial) no topo; cartão "Tema de hoje" em papel, com "Desenhar" e "Escrever".
- Lista dinâmica: etiquetas de prioridade (Alta em Copper, Média em Master Key), etapa (Decidido em Mozart, Comprado/Embrulhado em Prickly Pear), filtros em pílulas (selecionada em Master Key) e barra de orçamento (Mozart; Copper quando passa).
- Folhas (sheets) em pilha: tópico aberto a partir de outro mostra "‹ Anterior" no topo; X ou tocar fora fecha tudo. "Mais" no estilo Ajustes do iPhone: cartão de perfil + grupos (Nós dois, No iPhone, Seus dados, Ajuda) com linhas de 62 px (ícone, título, resumo, seta).
- Lista: etiqueta do tipo abaixo do título ("Lista simples" neutra / "Lista dinâmica" em Mozart) e botão "Configurações" (tipo com opções de rádio + "Aplicar" com confirmação, orçamento, renomear, apagar em Copper).
- Início (tela de entrada leve): saudação + sequência; prévia do último bilhete do outro (miniatura 72 px, etiqueta "Novo" em Copper até abrir); um único cartão "Mandar algo" em papel com a ideia do dia e Desenhar/Escrever; cartão da próxima data; atalhos Mural/Listas.
- Contagem regressiva: foto, ícone (traço) ou emoji, nessa prioridade, sobre a cor escolhida da paleta (Master Key por padrão), "Faltam N dias" em Copper, barra de progresso Sunburn, contorno Sunburn no dia.
- Contagem em tela cheia: "‹ Voltar" + "Editar"; com foto, capa 4:3 de largura total (cantos 16 px); sem foto, ícone grande (96 px), título em Caveat, relógio em três blocos (dias/horas/min) atualizado a cada 20 s, "É hoje!" no dia; botão "Mandar bilhete" e grade dos bilhetes ligados à data.
- Editar data: prévia ao vivo; foto da galeria (recorte 4:3, ≤150 KB) com "Trocar"/"Remover"; grade de 12 ícones (selecionado em Master Key), campo de emoji (prevalece sobre o ícone), 5 cores da paleta em círculos, hora opcional.
- Imagem da contagem: prévia + botão "Editar imagem" abre painel com abas Foto · Ícone · Emoji (uma de cada vez) e cor; com foto a cor vira fundo da contagem (24% sobre Surface, opção "Padrão" sem cor).
- Quando entregar / Reagendar: pílulas de escolha única (Agora · Amanhã 7h · Escolher; ao editar agendado, "Manter" primeiro); o campo de dia e hora só aparece em "Escolher". Nunca dois controles para a mesma decisão.
- Nossa sequência: abre ao tocar no 🔥 do Início; número grande em Copper, recorde em selo Master Key, 4 blocos (total, de cada um, dias juntos no mês) e o calendário. Mural só tem bilhetes: botão "Álbum de <mês>" + link "Meses anteriores"; aba "Agendados" só quando existir.
- Listas: botão "Nova lista" no cabeçalho abre folha (nome, tipo, orçamento, contagem ligada); cartão com etiqueta do tipo, barra Sunburn "x de y itens feitos", orçamento usado e data ligada.
- Avisos fora do app: depois de enviar, folha "Enviado" com "Avisar no WhatsApp" (primário) e "Outro app"; e-mail automático opcional pelo Gmail do dono (Mais › Avisos).
- Início, novos: com 2+ bilhetes não vistos, cartão "N novos de <nome>" lista até 6 (miniatura, título, tipo · hora, selo Novo) + "Marcar como vistos"; com 1, o cartão grande de sempre.
- Início, "Nas listas": até 3 novidades (item novo/editado/comprado, comentário com o texto entre aspas) das últimas 72 h, cada uma leva ao item ou chat; "Dispensar".
- Conversa da lista: mostra as mensagens de todos os itens em ordem, cada uma com etiqueta do item (toque escolhe o item); campo "Sobre" antes de escrever.
- Resposta: título automático "RE: <título original>", sem repetir RE.
- Desenho: Lápis e Borracha num segmento (ativo em Ink); "Apagando…" em Copper enquanto a borracha está ativa. Lupa circular de 116 px (2×) no canto oposto ao dedo, com anel do tamanho do traço.
- Início em seções reordenáveis (ordem por pessoa, salva em prefs/<slot>): padrão Bilhetes novos → Contagem → Mandar → Humor → Pergunta → Listas → Hoje há 1 mês → Mural e Listas. Segurar uma seção por 0,6 s ou tocar "Organizar o Início" abre a folha com alça de arrastar e setas.
- Contagem no Início: cartão da próxima data + fileira rolável de chips das seguintes (ícone, título, dias).
- Humor do dia: 6 emojis em grade (selecionado com borda Ink sobre Master Key); humor do outro no cabeçalho do cartão.
- Pergunta do dia: pergunta em Caveat; a resposta do outro só aparece depois da sua ("<nome> já respondeu. Responda para ver.").
- Lembrete suave: a partir das 20 h sem envio no dia, o cartão Mandar ganha contorno Sunburn e a frase "Ainda dá tempo de manter os N dias seguidos".
- Notificações: últimas 24 h (mais antigas recolhidas); contador Copper = há não vistas, neutro = tudo visto.

## Do's and Don'ts

- Do: uma frase em telas vazias; ícone do Bilhete em PNG (1024 px, envelope com coração sobre Background) para o atalho do iPhone; confirmação antes de apagar; mostrar presença só quando leva a uma ação.
- Don't: repetir "online" em vários lugares; usar Sunburn/Prickly Pear/Master Key em texto.
- Descartado: coral #C2412D + amarelo #FFF4D6 (v1–v5); fundo branco (avaliado e cancelado em 21/11/2026).
