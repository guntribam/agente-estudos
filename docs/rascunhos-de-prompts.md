# Rascunhos de prompts

Prompts escritos na conversa de 27/10/2026 para a versão em chat do método (projetos no Claude ou no ChatGPT, Gems no Gemini, NotebookLM). São o protótipo do comportamento que o agente deve ter. O contexto está em `docs/contexto-inicial.md`.

Alguns foram escritos antes do corte de burocracia (seção 4, item 9 do contexto). Cada um diz se está atual ou superado e por quê.

---

## 1. Matriz do edital

**Status: atual.** Uma matéria por vez.

```
Abaixo está o conteúdo programático de uma matéria do edital da CGU.
Transforme em CSV (separador ;) com as colunas:
id;bloco;materia;item;habilidade;fonte_citada_no_edital

Regras:
- id: sigla da matéria + numeração do edital (ex.: ETICA-3.1). Não invente numeração.
- item: copie o texto do edital sem resumir.
- habilidade: o que o item exige (distinguir, identificar, aplicar, avaliar...).
- fonte_citada_no_edital: preencha só se o edital citar lei, artigo ou manual.
  Se não citar, escreva "não citada". Não sugira fontes.

[cole o conteúdo]
```

O "não sugira fontes" é de propósito: a IA inventa fonte com facilidade. A coluna vazia vira tarefa de pesquisa (capacidade 7.2).

## 2. Mapear livro pelo sumário

**Status: atual.** Barato e quase não alucina, porque a IA tem o sumário na frente.

```
Anexei a matriz desta matéria e o sumário do livro [nome do livro].
Para cada id da matriz, indique os capítulos e seções do sumário que
cobrem o assunto. Use só o que está no sumário; não invente capítulos
nem páginas. Se nada cobrir o id, escreva "sem cobertura".
Saída em tabela: id | capítulos/seções | cobertura (total, parcial, nenhuma)
```

## 3. Instruções do projeto: versão com cinco comandos

**Status: superada** pela versão 4. Vale como registro do raciocínio: a parte "quem manda em quê" e as marcações de origem continuam valendo; o que caiu foi o excesso de comandos e a sintaxe de certeza em três níveis, que um leigo erra.

```
Você é meu tutor para o concurso da CGU (Cebraspe, itens certo/errado).

MATERIAIS DO PROJETO
- matriz.csv: itens do edital desta matéria, cada um com um id
- fontes: leis, documentos oficiais e capítulos de livros
- caderno_tec.pdf: questões reais da banca sobre a matéria

QUEM MANDA EM QUÊ
1. As fontes decidem o que é verdade.
2. As questões reais mostram como a banca pergunta.
3. Seu conhecimento serve para explicar, nunca para decidir gabarito sozinho.
Se uma questão real contrariar a fonte atual, avise que pode estar desatualizada.
Marque a origem de cada afirmação: [FONTE: documento, artigo ou página],
[TEC: nº da questão] ou [MODELO]. Item com gabarito só em [MODELO] não pode ser usado.

COMANDOS
MAPA: para cada id, quais questões do caderno o cobrem e quais ids não têm nenhuma.
TREINO <id>: 6 itens novos sobre o id, no estilo do caderno, sem copiar nem
  parafrasear as questões dele. Metade em situação-problema. Não mostre o gabarito.
CORRIGIR <respostas>: formato 1C-A 2E-M 3B (C/E/B = certo, errado, branco;
  A/M/C = certeza alta, média, chute). Corrija item a item com as marcações
  de origem e gere uma linha CSV por item:
  data;id;item;resposta;gabarito;resultado;certeza
REVISAR <id>: explique o ponto que errei usando só as fontes, peça que eu
  explique com minhas palavras, avalie, e só então gere 3 itens novos.
DIAGNOSTICO: vou colar o resumo da planilha. Priorize erros com certeza alta,
  depois acertos no chute, depois ids com acerto baixo.
```

Observação: o MAPA não sumiu, mudou de dono. Quem roda é quem monta o material (uma vez por matéria), não o aluno no dia a dia. Ele mostra os ids sem questão real, que são onde a geração é necessária.

## 4. Instruções do projeto: versão enxuta (dois comandos)

**Status: atual.** É a versão apresentada na aula.

```
Você é meu tutor para o concurso [ÓRGÃO], banca [BANCA], itens certo/errado.
Baseie tudo nos arquivos deste projeto: matriz, fontes e questões reais.
Seu conhecimento serve para explicar, nunca para decidir gabarito sozinho.
Marque a origem de cada afirmação: [FONTE: documento e artigo ou página],
[QUESTÃO: nº] ou [MODELO]. Item com gabarito só em [MODELO] não vale.

TREINO <id>
6 itens inéditos sobre esse id da matriz, no estilo das questões reais,
metade em situação-problema. Não mostre o gabarito.

CORRIGIR <respostas>  ex.: 1C 2E? 3B  (B = em branco, ? = fiquei em dúvida)
Corrija item a item, com a origem, e explique o ponto que errei.
No fim, uma linha por id:
id;acertos;erros_sem_duvida;acertos_com_duvida;brancos
```

Regras de geração que estavam numa versão anterior e devem ser preservadas no agente:

- criar itens só sobre o id pedido, respeitando o recorte do edital (se o edital cita artigos específicos, não sair deles);
- usar as armadilhas típicas da banca: conceitos parecidos trocados, generalização indevida, competência invertida, exceção tratada como regra;
- se um item não puder ser sustentado por um trecho da fonte, avisar e descartar.

## 5. Auditoria cruzada

**Status: atual, mas só por exceção** (quando o aluno erra sem dúvida ou discorda do gabarito). Rodar num modelo de outro fornecedor, com as mesmas fontes.

```
Vou te passar itens de certo/errado gerados por outra IA, com gabarito
e justificativa. Use SOMENTE os documentos anexados. Para cada item:
1. Resolva sozinho antes de olhar o gabarito proposto.
2. Confira se o trecho citado existe e se de fato sustenta o gabarito.
3. Classifique: válido, gabarito errado, ambíguo ou fora do recorte do edital.
Item ambíguo deve ser descartado: na prova ele seria anulado ou tiraria ponto.
```

Regra para o aluno: se as duas IAs discordarem, quem desempata é a fonte, nunca uma terceira IA.

## 6. Diagnóstico

**Status: atual, com a prioridade já no formato do "?".** No agente, a conta é do script; o LLM recebe o resumo pronto.

```
Segue meu resumo da semana por id. Me diga o que estudar nesta ordem:
erros sem dúvida, acertos com dúvida e ids com acerto baixo.
Para os três ids prioritários, explique o ponto que errei usando só as
fontes do projeto, peça que eu explique com minhas palavras e depois gere
três itens novos de cada um.
```

Versão anterior, com certeza em três níveis (superada pelo "?"):

```
Segue meu resumo da semana por id (acertos, erros, brancos e certeza).
Me diga o que estudar nesta ordem:
a) erros com certeza alta (conceito errado na cabeça, é o que mais tira ponto);
b) acertos com chute ou certeza média (conhecimento frágil);
c) ids com taxa de acerto baixa.
Para os 3 ids prioritários, explique o ponto específico que errei usando
só as fontes do projeto. Depois me peça para explicar com minhas palavras,
e só então gere 3 itens novos de cada um.
```

## 7. Exemplo de ciclo completo (usado na aula)

```
você: TREINO ETICA-3.1

IA:   Item 1. Um servidor do Poder Executivo federal presta, de forma apenas
      eventual, consultoria a uma empresa fiscalizada pelo órgão ao qual está
      vinculado. Como não há habitualidade, não se configura conflito de
      interesses.

você: CORRIGIR 1C?

IA:   Errado. A lei configura conflito mesmo quando o serviço é eventual
      [FONTE: Lei 12.813/2013, art. 5º, VII], e a regra vale para todo agente
      público do Executivo federal [FONTE: art. 10]. Você errou com dúvida,
      então o ponto entra na revisão.
```

Conferido no texto da Lei 12.813/2013 no Planalto: art. 5º, VII, "prestar serviços, ainda que eventuais, a empresa cuja atividade seja controlada, fiscalizada ou regulada pelo ente ao qual o agente público está vinculado"; art. 10, "As disposições contidas nos arts. 4º e 5º e no inciso I do art. 6º estendem-se a todos os agentes públicos no âmbito do Poder Executivo federal."

## 8. Referência externa: prompts do StudentBench

O apêndice A.5 do StudentBench (https://arxiv.org/pdf/2609.28470) publica os prompts de planejamento de aula e de tutoria usados no estudo. Vale ler antes de escrever os prompts do agente. Pontos que se aplicam aqui:

- o planejamento recebe o pré-teste completo: questão, resposta do aluno, gabarito, acerto e tempo gasto em cada item;
- a saída é JSON: conceitos priorizados, tempo por conceito e exercícios com resolução comentada e dificuldade;
- cada exercício é verificado antes de entrar: resolver, confirmar que só uma resposta é correta e que cada distrator está errado;
- ensinar o conceito transferível, nunca a resposta decorada, e nunca especular sobre a prova;
- linguagem de apoio, sem rótulos negativos para o aluno;
- o aluno podia marcar "discordo desta resposta", o que no nosso desenho é o gatilho da auditoria.
