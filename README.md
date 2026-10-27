# Agente de estudos DevEstavel

Um modelo de projeto para estudar para concurso com um agente de IA (Claude Code ou Codex). Você conversa; o agente organiza o edital do seu cargo, ajuda a escolher as fontes, busca questões da sua banca no TEC Concursos, cria questões para você treinar e corrige sem inventar.

## Do que você precisa

- Claude Code (plano Pro ou superior) ou Codex.
- Conta no TEC Concursos. Para buscar questões, o agente precisa controlar um navegador; no Claude, serve o navegador do app desktop ou a extensão Claude in Chrome.
- O PDF do edital.

O agente instala sozinho o que os scripts precisam e pede sua permissão antes.

## Como começar

1. Clone este repositório e abra o terminal na pasta dele.
2. Rode `claude` (ou `codex`).
3. Diga "monta o meu edital" e conte onde está o PDF.

Depois é conversa:

- "quero material de Ética"
- "traz questões de conflito de interesses"
- "me treina em conflito de interesses"

## Seus dados

Tudo o que é seu fica na pasta `estudo/`, só no seu computador. O git ignora essa pasta: nada do seu estudo, das questões do TEC ou dos seus livros vai para o GitHub.

Para atualizar o modelo, `git pull`. Seus dados não são afetados.
