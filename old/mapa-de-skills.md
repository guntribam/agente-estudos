# Mapa de skills

Decidido em 27/10/2026. Complementa o `docs/contexto-inicial.md` e, onde os dois divergem, vale este.

Para o aluno, tudo é conversa. Ele nunca digita um id nem abre um arquivo. Ids, registro de respostas e contas ficam com o agente.

## A tríade

O treino se apoia em três coisas, cada uma com um papel:

- **Fontes**, conversadas e negociadas com o aluno. Decidem o que é verdade.
- **Questões reais**, obtidas no TEC. São matéria-prima: mostram como a banca pergunta, que pegadinhas usa e o que ela deu como certo. Servem para enriquecer e variar o treino.
- **Conhecimento do modelo.** Um modelo como o Opus 5.5 sabe muito e explica, conecta e cria bem. Mas não pode inventar: gabarito precisa estar apoiado numa fonte ou numa questão real.

Por isso obter questões e treinar são coisas separadas. A skill `questoes` junta material, e a skill `treino` usa a tríade para montar as questões do aluno.

## As cinco skills

**edital.** O aluno traz o PDF do edital e diz o cargo. O agente monta o conteúdo programático do cargo seguindo a hierarquia do edital, com o texto literal de cada item. Cada item ganha um id com a sigla da matéria e a numeração do próprio edital (`ETICA-3.1`), sem subdividir.

Detalhe: o aluno diz "monta o meu edital", e o agente lista os cargos encontrados e pergunta qual é o dele. Sai um único `edital.md` (bloco > matéria > tópico > item). A sigla aparece só no título da matéria (`### Ética Pública e Responsabilidade Profissional [ETICA]`), e o id é a sigla mais o número do item. Um script confere que cada item existe no texto do PDF e que a numeração não pula. PDF escaneado: o agente avisa e para. Ficam para depois as regras do edital que afetam o estudo (14.32, 14.33.1, penalidade) e o tratamento de retificação.

**fontes.** O aluno pede material para uma matéria ou para alguns assuntos. O agente junta os assuntos afins, pergunta como o aluno quer pesquisar, busca na web e sugere só o que encontrou, com link. Dá preferência a documentação oficial, texto de lei e livros consagrados. O que o aluno escolhe vai para o catálogo de fontes dele.

Detalhe: a skill tem três momentos. Conversar: o agente agrupa os itens do `edital.md` por afinidade; onde o edital já cita a fonte, não há escolha. Negociar: para cada grupo com escolha, duas ou três opções achadas na web, com link; se o aluno traz um livro, o agente diz pelo sumário o que ele cobre. O combinado vai para um `fontes.md`. Obter: lei e documento oficial o agente baixa sozinho; livro o aluno coloca na pasta.

Tudo é convertido para `.md`, um arquivo por capítulo, com o pymupdf4llm, rodando por `uv run` para o aluno não lidar com instalação. Se a conversão falhar ou vier ruim (PDF escaneado, por exemplo), o agente lê o próprio PDF, mesmo gastando mais limite. Sem OCR e sem Docling. Para o aluno, isso é invisível: ele só ouve algo como "preparei o livro, os capítulos 3 e 5 cobrem conflito de interesses". O material fica na pasta ignorada pelo git.

**questoes.** O aluno pede questões de um assunto. O agente busca no TEC pelo navegador, usando a sessão que o aluno já abriu, e guarda as questões com os ids do edital. Essas questões são material de referência para o treino, como as fontes. A busca acontece uma vez por assunto, e o agente só volta ao TEC quando quiser mais material.

**treino.** O agente monta as questões a partir da tríade. As fontes dão o conteúdo e o gabarito, as questões reais dão o jeito de perguntar e as pegadinhas da banca, e o conhecimento do modelo dá variedade e situações-problema. O treino sempre cria as questões, mesmo quando a criada fica bem parecida com uma real. A questão real nunca é aplicada como está: ela é fonte de conhecimento sobre como a banca cobra, o estilo e o desafio colocado. O gabarito da questão criada precisa se apoiar num trecho da fonte ou numa questão real que cobre o mesmo ponto. Cada rodada tem 3, 5 ou 10 questões, à escolha do aluno. O feedback segue `docs/prompt-feedback-treino.md`, que protege contra a IA inventar ou ensinar errado; a frase com as palavras do aluno é pedida só no erro sem dúvida.

Registro: a questão criada vai para o `estudo/questoes.jsonl` com código próprio (`g-0001`), `origem: "gerada"`, gabarito e apoio. Cada resposta vira uma linha em `estudo/respostas.csv` (`data;item;questao;resposta;gabarito;resultado;duvida;ponto`), gravada por script, que é quem decide acerto, erro ou branco comparando com o gabarito. O erro é a própria linha: a coluna `ponto` traz, só nos erros, uma frase com o que o aluno errou e onde a fonte diz o contrário. Não há caderno de erros separado. É o treino que descarta questões de cargos muito acima do concurso do aluno (para a CGU, juiz, promotor e delegado); a skill `questoes` não filtra isso no TEC. O aluno responde no formato `1C 2E? 3B`, em que o `?` marca resposta dada na dúvida. A correção cita a origem de cada afirmação. Quando o aluno erra, o agente explica o ponto e anota o erro. Quando ele diz "discordo", o agente confere na fonte ali mesmo.

**material.** (Substitui o `balanco`, descartado pelo Gunter.) Depois de uma rodada de treino, o agente julga se vale a pena montar um material enxuto de estudo do tópico e, se valer, escreve no próprio chat. Nada de PDF ou arquivo, a não ser que o aluno peça. O material se apoia nas fontes e nas questões reais, com o mesmo rigor do feedback: nada inventado, origem marcada e trecho literal da fonte. O aluno também pode pedir o material a qualquer momento.

Detalhe: vale a pena quando houve erro sem dúvida, vários erros no mesmo ponto ou muitos acertos na dúvida; rodada limpa ou erro isolado já resolvido no feedback não pedem material. Quando vale, o agente oferece em uma linha e só escreve se o aluno quiser. O material é organizado pelos conceitos que falharam, cabe numa tela, e cada conceito tem: o que a fonte diz (trecho literal, `[FONTE]`), como a banca cobra (pegadinha com o número das questões reais, `[QUESTÃO]`) e como não cair (uma ou duas linhas do modelo, `[MODELO]`, sem fato novo). Mesmas regras de rigor do feedback.

## Decisões que valem para todas

- O edital é a fonte da verdade sobre o que estudar. O agente não questiona o escopo.
- Contas e checagens são feitas por script. A IA explica e conversa.
- As questões ficam só no computador do aluno, numa pasta que o git ignora, porque o repositório é público.
- Dados em texto (JSONL e CSV), sem SQLite.
- Não há exportação para a aplicação de ciclo de estudos.

## Formato dos arquivos

- `AGENTS.md` com as regras comuns e uma linha por skill. Um `CLAUDE.md` com só `@AGENTS.md`, para o Claude Code ler o mesmo arquivo.
- Cada skill num `SKILL.md` do padrão Agent Skills, só com os campos do padrão, escrito com rigor para que nada seja inventado: as fontes e as questões obtidas servem de inspiração, e nunca a memória do modelo sozinha. A versão oficial fica em `.agents/skills/` (onde o Codex procura), e um script copia para `.claude/skills/` (onde o Claude Code procura). A cópia não se edita à mão.
- Os arquivos são criados depois que o desenho das skills fechar.

## Ainda em aberto

Os detalhes de cada skill (arquivos, formatos, scripts), decididos um de cada vez, quando a skill for construída.
