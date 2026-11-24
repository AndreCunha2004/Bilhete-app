# 💌 Bilhete

Um cantinho só nosso para trocar bilhetes, rabiscos e listas — em tempo real, direto do celular.

## O que dá pra fazer
- **Bilhetes do dia:** desenhos (com foto de fundo) e cartas, com envio agendado
- **Mural e álbum:** todos os bilhetes, organizados por dia e por mês
- **Contagens regressivas:** próximas datas especiais, com foto de capa
- **Listas compartilhadas:** presentes de Natal, viagens… com conversa por item
- **Início personalizável:** humor do dia, pergunta do dia, "hoje há 1 mês" e sequência de dias
- **Ao vivo:** veja quando o outro está online ou desenhando

## Como funciona
- Site estático no **GitHub Pages**
- Dados, login e tempo real no **Supabase** (só duas contas têm acesso)
- Instalável no iPhone: Safari › Compartilhar › **Adicionar à Tela de Início**

## Estrutura
| Arquivo | Para quê |
|---|---|
| `index.html` | O app |
| `supa.js` | Ligação com o Supabase (dados, login, presença) |
| `config.js` | URL e chave pública do projeto |
| `supabase/schema.sql` | Banco e regras de acesso |
| `manifest.webmanifest`, `sw.js`, `icons/` | Instalação como app |
| `DESIGN.md` | Cores, fontes e componentes |

---
Feito com carinho por Déco, para a Maju. 🌊
