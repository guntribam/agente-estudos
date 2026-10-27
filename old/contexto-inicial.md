# Contexto do projeto agente-estudos

Este documento resume uma conversa longa, em 27/10/2026, entre o Gunter (dono do repositório) e o Claude, no app. O problema foi sendo entendido aos poucos, com idas e voltas, e várias propostas foram corrigidas pelo Gunter no caminho. As decisões só fazem sentido junto com o raciocínio que levou a elas, por isso o raciocínio está aqui, não só as conclusões.

Leia tudo antes de propor qualquer coisa. O projeto está em **fase de desenho**: nada de código nem de estrutura de pastas ainda. O Gunter quer desenhar a solução junto. Traga opções com trade-offs e deixe a decisão com ele.

Arquivos que acompanham este documento:

- `docs/rascunhos-de-prompts.md`: os prompts que já foram escritos e testados na conversa (são o protótipo do comportamento do agente).
- `docs/exemplo-cgu/edital-cgu-conteudo.pdf` e `.txt`: o trecho do edital da CGU usado como caso de teste (itens 14.28 a 15 do edital).

Sumário: 1 quem e para quem · 2 o cenário · 3 o problema · 4 como a conversa evoluiu · 5 princípios · 6 o que já existe · 7 as quatro capacidades pedidas e as calibragens propostas · 8 decisões · 9 em aberto · 10 evidências e fatos verificados · 11 o exemplo CGU · 12 como começar.

---

## 1. Quem e para quem

- **Gunter**: analista de sistemas e professor de desenvolvimento de software. Toca a **DevEstavel** (sempre escrito sem acento), preparatório de concursos de T.I. com cerca de 200 alunos de mentoria. Programa em Python, Java, Kotlin e TypeScript e mantém infraestrutura própria. Prefere manutenção a velocidade e simplicidade a flexibilidade prematura. Não quer concentrar o trabalho num único fornecedor de IA.
- **Alunos**: profissionais de T.I. Terminal, pasta e git não assustam. Mas **não sabem nada de IA**: nunca escreveram um prompt e não sabem que o modelo pode inventar coisas com total confiança.
- **Todos os alunos têm acesso ao TEC Concursos.**
- O Gunter já tem uma **aplicação de ciclo de estudos**: o aluno sobe uma planilha com a projeção de acertos por matéria, monta o ciclo e controla o avanço nele. O template não substitui essa aplicação; deve alimentá-la.
- O Gunter **não quer construir uma aplicação para os alunos**. Um repositório-template, operado por um agente de programação (Claude Code, Codex), é aceitável.

## 2. O cenário que originou tudo

Saiu o edital da CGU (banca Cebraspe, itens de certo/errado). Os cursinhos ainda não têm material para ele. O aluno tem um edital enorme e uns dois meses. Na prática, vai estudar com Claude, ChatGPT ou Gemini.

O Gunter parte de uma premissa que não está em discussão: **fazer questão é central**, porque no dia da prova o que existe são questões. A pergunta dele é como encaixar as questões no estudo de forma que:

1. não sejam elaboradas a partir de premissas desencontradas do que vai ser cobrado;
2. tragam feedback e ensino com base no desempenho do aluno nas próprias questões.

A CGU é um exemplo. O template serve para **qualquer concurso**, mas a CGU é o caso de teste e deve ser usada do começo ao fim.

## 3. O problema, de verdade

Gerar questão não é o problema; qualquer chatbot gera. O problema é que, quando o aluno pede "crie 10 questões no estilo Cebraspe sobre conflito de interesses", o modelo decide sozinho três coisas que não deveria decidir:

1. **O recorte.** Quem escolhe o que cobrar é a IA, pelo que ela acha relevante, e não o item do edital. No edital da CGU, conflito de interesses é cobrado "nos termos dos arts. 3º a 5º, 8º e 10 da Lei nº 12.813/2013". A IA não sabe disso.
2. **O gabarito.** Sai da memória do modelo, que pode estar errada ou desatualizada. O edital da CGU (14.32) cobra a legislação com vigência até a data de publicação do edital, e (14.33.1) jurisprudência publicada até 30 dias antes da prova. A memória do modelo não acompanha isso.
3. **O estilo.** Vira um "estilo Cebraspe" genérico, que não é como a banca pergunta de fato.

E um quarto problema, menos visível:

4. **O histórico.** Cada conversa morre ali. O chatbot não junta os erros da semana, então não existe diagnóstico. O aluno faz 300 questões e não sabe em que item do edital está fraco.

A conclusão que orientou tudo depois: **tirar essas decisões do modelo** e deixar com ele só o que ele faz bem, que é redigir, explicar e conversar.

Outras dimensões do problema que apareceram na conversa:

- **Edital novo.** As matérias da CGU têm nomes e recortes novos, interdisciplinares, que não batem um a um com as disciplinas tradicionais de concurso (Ética Pública, por exemplo, junta Lei 12.813, Lei 9.784 e o código de conduta da CGU). O banco histórico de questões cobre mal, e a tentação é preencher com questão gerada. Questão gerada com gabarito errado faz o aluno aprender o erro com convicção.
- **Penalidade.** No certo/errado do Cebraspe, em geral, errar tira ponto (confirmar no edital completo da CGU; o trecho que temos não traz). Então o aluno precisa saber o que sabe, e não só acertar: a confiança na resposta é informação.
- **Habilidades (15.1).** O edital avisa que os itens vão além da memorização (compreensão, aplicação, análise, síntese, avaliação) e que um item pode cruzar mais de um objeto de avaliação. Isso pune quem aprende a reconhecer a redação da questão em vez do conceito, e pede questões de situação-problema.
- **Itens sem fonte normativa.** Nem todo item tem lei por trás. "Heranças da escravidão, hierarquias sociais e construção da cidadania" não tem artigo para citar. Ali a fonte vira referência acadêmica, e a questão gerada fica menos confiável.
- **Volume.** Cada cargo tem 13 ou 14 matérias. Se montar o material de uma matéria leva meia hora, são mais de seis horas de montagem para alguém que tem dois meses e nunca usou IA. A maioria trava aí.

## 4. Como a conversa evoluiu (e o que o Gunter corrigiu)

Esta seção existe para você não repetir caminhos que já foram descartados.

1. **Ponto de partida.** O Gunter ia dar uma aula sobre IA para concursos. O Claude sugeriu três temas genéricos (IA como examinador, onde a IA mente, IA para planejar o estudo). Não era isso. Ele queria saber de rankings de IA para ensino e se dava para montar um **ambiente de estudos**: gerador de questões, auditor de resultados, feedback do que estudar. A primeira ideia dele foi usar os plugins do DeepSeek Harness.
2. **Arquitetura inicial.** O Claude propôs: gerador (questões estruturadas por assunto, com gabarito e justificativa) → verificador (um segundo modelo resolve às cegas; só entra o que bate) → **auditor determinístico, em código, sem LLM**, que calcula acerto por assunto e tendência → o LLM só transforma os números em recomendação → revisão espaçada. A separação "código calcula, LLM interpreta" nasceu aqui e continua valendo.
3. **Pesquisa.** O StudentBench (seção 10) entrou como evidência e como modelo de fluxo: pré-teste → plano → exercícios → tutoria → pós-teste.
4. **Estrutura do edital.** O Gunter pediu os macrotópicos e as matérias da CGU (seção 11).
5. **Correção importante.** O Gunter pediu uma reflexão sobre o processo de estudo. O Claude respondeu com pedagogia (efeito de testagem, efeito pré-teste, reversão da expertise) e um ciclo genérico de sete etapas. **Resposta do Gunter: "você construiu o processo, mas ainda não é bem isso."** Ele não queria teoria de estudo; queria resolver o cenário concreto da seção 2. Lição: **ancore no cenário concreto, não em pedagogia abstrata.** A pedagogia continua válida como fundamento (seção 10), mas não é o produto.
6. **O desenho que o Gunter aprovou** ("perfeito, você delineou bem o problema"): a unidade de tudo é o **item do edital**; cada item tem uma **ficha de fontes**; o estilo vem de **questões reais**; o **ensino nasce do erro**; e o trabalho pesado é feito **uma vez por edital**, não por aluno ("isso é produto, não prompt"). Começar por uma matéria só: Ética Pública.
7. **A aula.** O método virou uma versão em chat, para qualquer ferramenta (projetos no Claude e no ChatGPT, Gems no Gemini, NotebookLM): matriz do edital, fontes oficiais, um projeto por matéria com instruções fixas, treino com correção citando a fonte, auditoria cruzada e diagnóstico. Os prompts estão em `docs/rascunhos-de-prompts.md`.
8. **A tríade.** O Gunter enriqueceu: fonte nem sempre é lei (em T.I. há bibliografia consagrada, que o aluno baixa em PDF, e isso é outro processo); todos os alunos têm TEC, então dá para ter uma base de questões reais. A tríade dele: **conhecimento do modelo + questões do TEC + fontes baixadas pelo aluno.** O Claude definiu o papel de cada parte (princípio 3, seção 5) e desaconselhou raspar o TEC pelo navegador (seção 7.3).
9. **Burocracia.** O Gunter perguntou se tinha burocratizado demais. Resposta: **um pouco, e parte veio do Claude** (cinco comandos, certeza em três níveis com sintaxe "1C-A 2E-M", uma linha de CSV por questão colada à mão, auditoria de toda questão gerada). O desenho estava certo; o problema era quem carregava o peso. Critério que ficou: **numa hora de estudo, o aluno não pode gastar mais que uns 10 minutos administrando o processo**, ou larga na terceira semana. Cortes: montagem centralizada, dois comandos, um único sinal de dúvida ("?"), registro por sessão, auditoria por exceção, começar com 2 ou 3 matérias. E uma observação: burocracia não some, muda de lugar. Processo com muito passo manual quer virar software.
10. **Agente.** O Gunter disse que não quer construir aplicação, mas que usar um agente no lugar dos projetos do chat "não seria má opção, se der mais flexibilidade, agilidade e diminuir a probabilidade de erro". O Claude primeiro entendeu "assistente compartilhado no chat"; **ele se referia ao Claude Code**. Análise feita (seção 7, introdução).
11. **O pedido do template.** O Gunter definiu o projeto como um **template para qualquer concurso** e listou quatro capacidades (seção 7), pedindo opinião e calibragem. A resposta foi adiada por causa da aula. **Essa resposta ainda está devendo**; as propostas estão na seção 7, marcadas como não discutidas.
12. **Criação do repositório.** Público, `guntribam/agente-estudos`. Dados em CSV/JSONL. Sobre o TEC, o Gunter pediu: "calma, não precisa tomar todas as decisões agora".
13. **Este documento.** A primeira versão do handoff era um resumo de decisões, e o Gunter achou fraca com razão: sem o problema, nenhum agente propõe boa solução. Daí este texto.

## 5. Princípios do desenho

Cada princípio vem com o motivo, porque é o motivo que permite aplicar o princípio a casos que ninguém previu.

1. **O edital decide o que estudar. A fonte decide o que é verdade. A IA explica, treina e corrige.** O modelo responde com a mesma confiança tendo ou não o material na frente. A analogia usada com os alunos: a IA é um aluno brilhante que leu quase tudo e lembra de tudo meio borrado; com o livro aberto, responde pelo livro; sem o livro, responde de cabeça. Todo o método é entregar o livro aberto.
2. **A unidade é o item do edital, com id estável** (ex.: `ETICA-3.1`, sigla da matéria mais a numeração do próprio edital). Toda questão aponta para um ou mais ids; todo resultado volta para um id. É daí que saem diagnóstico, prioridade e a soma por matéria que alimenta a aplicação de ciclo de estudos. O edital da CGU ajuda: é granular e escrito como competência ("distinção entre indício, falha de gestão, irregularidade e responsabilidade" já diz como o item vai ser cobrado), e o 15.1 é quase a taxonomia de Bloom. Funciona como matriz de referência da prova.
3. **Hierarquia de autoridade: fonte vigente > questão real > modelo.** A fonte (lei na versão da data do edital, norma oficial, especificação, livro) decide o que é verdade. A questão real mostra como a banca pergunta e o que ela deu como certo no gabarito definitivo. O modelo explica, conecta e cria variações; nunca decide gabarito sozinho. Questão real antiga que contraria a fonte vigente provavelmente está desatualizada.
4. **Toda afirmação da correção marca a origem**: `[FONTE: documento, artigo ou página]`, `[QUESTÃO: nº]` ou `[MODELO]`. Item cujo gabarito só se apoia em `[MODELO]` não vale. Para o leigo, é a forma de enxergar quando a IA falou "de cabeça".
5. **Código calcula, LLM interpreta.** Estatística por item, prioridade, agenda de revisão e a checagem de que um trecho citado existe na fonte são feitas por script. LLM erra conta e não percebe; checagem determinística é o que reduz erro de verdade.
6. **Questão real vale mais que questão gerada.** Gerar só onde o banco real não cobre o item.
7. **O ensino nasce do erro.** Errou: explicação do ponto específico que falhou, com a fonte; o aluno explica com as próprias palavras; o agente avalia; libera 2 ou 3 itens novos do mesmo id; o erro entra na revisão espaçada.
8. **A confiança é informação.** O aluno marca com "?" a resposta dada na dúvida. Prioridade de revisão: (1) erro sem dúvida, que é conceito errado na cabeça e o que mais tira ponto no Cebraspe; (2) acerto com dúvida, que é conhecimento frágil; (3) item com acerto baixo.
9. **Auditoria por exceção.** Conferir a correção só quando o aluno errou sem dúvida ou discorda do gabarito. É exatamente aí que um gabarito errado faz mais estrago: a IA "corrige" quem sabia, e o aluno desaprende. A conferência usa a fonte ou um modelo de outro fornecedor com a mesma fonte. Se divergirem, quem desempata é a fonte, nunca uma terceira IA. Item ambíguo sai, porque na prova seria anulado ou tiraria ponto.
10. **O peso fica fora do aluno.** Montagem pesada acontece uma vez por edital. No dia a dia, o aluno usa poucos comandos, sem sintaxe frágil, e gasta no máximo uns 10 minutos por hora com administração.
11. **Portável e neutro.** Instruções num `AGENTS.md` como fonte única, scripts em Python, dados em texto. Tem que rodar em Claude Code e Codex. Nada que prenda a um fornecedor. Rodar em dois fornecedores ainda dá a auditoria cruzada de brinde.
12. **Simplicidade antes de flexibilidade; manutenção antes de velocidade.** Preferência declarada do Gunter.
13. **Não redistribuir conteúdo de terceiros.** O repositório é público. Caderno do TEC e capítulos de livros ficam com cada aluno; o repositório só leva texto oficial ou aberto.
14. **Questão primeiro, com base mínima.** Começar pela questão tem apoio na pesquisa (efeito de testagem, efeito pré-teste), mas o iniciante sem base precisa de explicação estruturada (reversão da expertise). Por isso a teoria entra enxuta e dirigida ao erro, não capítulo inteiro.

## 6. O que já existe

- **O método em chat** (versão da aula): está em `docs/rascunhos-de-prompts.md`. É o protótipo do comportamento que o agente deve ter.
- **A promessa feita aos alunos.** O deck da aula de 27/10 termina assim: "Próximo passo: um modelo de projeto para rodar no Claude Code ou no Codex. Ele organiza o edital do seu cargo, ajuda a achar fontes consagradas, registra suas questões e resume seus erros. Em construção."
- **Projetos do Gunter que podem ser reaproveitados** (não assuma detalhes; pergunte):
  - **Motor de questões**: schema em PocketBase e extrator em PyMuPDF para PDFs de cadernos do TEC. Classificação em seis eixos: nó taxonômico principal, tags secundárias, habilidade cognitiva, faixa de dificuldade (N1, N2, N3), catálogo de pegadinhas e metadados automáticos. O PDF impresso do TEC não traz o percentual de acertos. Objetivo: recomendar questões pelo nível do aluno.
  - **Ideia de RAG de concursos**: PDFs, livros e questões de T.I. gerando planos didáticos, cadernos de questões, slides e PDFs. Ele avaliava o Docling para converter PDFs.
  - **Aplicação de ciclo de estudos** (seção 1).
  - **Gateway de LLM** com LiteLLM e OpenRouter.

## 7. As quatro capacidades pedidas e as calibragens propostas

### Por que agente (Claude Code, Codex) e não projeto no chat

Os alunos são de T.I., então terminal não é barreira. O que o agente faz melhor que o projeto do chat:

- **Distribuição**: o kit vira uma pasta num repositório; o aluno clona, coloca os próprios arquivos nas pastas certas, e quando o Gunter corrige algo, o aluno atualiza. No chat, projeto compartilhado só existe em planos de organização.
- **Registro automático**: o agente grava cada sessão em arquivo. Acaba o copia-e-cola, que era a parte mais burocrática.
- **Checagem por código**: antes de mostrar uma questão gerada, um script confere se o trecho citado existe literalmente na fonte. A estatística por item também sai de script.
- **Comandos fixos**, que se comportam sempre igual, sem o aluno escrever prompt.

O que pesa contra, e o desenho precisa tratar:

- **Plano pago.** O Claude Code exige Pro ou superior, e o limite de uso é compartilhado com o chat. Sessões que leem arquivos e rodam scripts gastam mais. Contexto precisa ser enxuto.
- **Ferramenta de programação.** Menos confortável que o chat e sem celular.
- **Autonomia.** O agente edita arquivos e roda comandos. Restringir: ler as fontes, escrever só nas pastas de dados.
- **Fornecedor único.** Daí o princípio 11.

Na conversa ficou também a ideia de **dois níveis**: o método em chat como porta de entrada (funciona no celular e no plano grátis) e o template como modo completo.

Abaixo, as quatro capacidades com o texto do pedido do Gunter (próximo das palavras dele) e as **propostas do Claude, que ainda não foram discutidas com ele**. Trate as propostas como ponto de partida, não como decisão.

### 7.1 Edital → conteúdo programático

**Pedido.** O aluno traz os PDFs do edital, e o agente cria uma pasta ou um arquivo `.md` com o conteúdo programático. O que importa é o conteúdo, organizado de acordo com a hierarquia do edital. O agente pergunta ao aluno qual cargo ele pretende.

**Propostas:**

- Duas saídas do mesmo dado: um `.md` legível (macrotópico > matéria > item) e uma matriz em CSV, com uma linha por item: id, bloco, matéria, texto do item, habilidade exigida e fonte citada pelo próprio edital.
- **Texto literal**, sem resumir. Um script confere que cada item existe no texto extraído do PDF (normalizando quebra de linha e hifenização) e que a numeração é contínua. Isso pega a IA "resumindo" ou pulando item.
- Incluir os blocos comuns a todos os cargos e os específicos do cargo escolhido.
- Capturar também as **regras do edital que mudam o estudo**: corte de legislação (14.32), jurisprudência (14.33.1), habilidades (15.1), penalidade, número de itens e peso por bloco. O trecho da CGU que temos começa no 14.28; o resto exige o edital completo.
- **Granularidade** (pergunta aberta): vários itens juntam assuntos separados por ponto e vírgula. Ex.: "1.1 Estado, governo e administração; autoridade, legitimidade e poder; interesse público, pluralismo e conflitos distributivos". Subdividir (`ESTADO-1.1.a`, `1.1.b`...) melhora o diagnóstico, mas multiplica os ids. No cargo de Desenvolvimento, ao contrário, o edital já vem bem fatiado ("2.1 Linguagem Java: tipos de dados, estruturas de controle, métodos, classes e objetos").
- Registrar versão e data do edital, porque retificações acontecem.

### 7.2 Fontes

**Pedido.** O aluno pode conversar com o agente sobre as fontes. Se não souber as fontes de um tópico, o agente sugere: **jamais fontes inexistentes, e sempre fontes consagradas**, nada obscuro ou pouco conhecido. O aluno pode colar uma matéria inteira em vez de um tópico; o agente pergunta qual abordagem ele quer, procura fontes de cada tópico em separado e **junta os tópicos por afinidade dentro de uma mesma categoria didática**. Exemplo do Gunter: o aluno cola Java, PHP, OpenSSL e OWASP; o agente junta Java e PHP como linguagens de programação e pergunta como o aluno quer fazer a pesquisa. O agente deve ajudar o aluno a entender o escopo dos conteúdos, para facilitar a busca de fontes.

**Propostas:**

- **"Nunca inventar" garantido por verificação, não por promessa.** Toda fonte sugerida vem com um localizador verificável (URL oficial, número da lei, número da RFC, ISBN e edição), e o agente confere na web antes de apresentar. O que não foi conferido sai marcado como "não verificada".
- **Ordem de preferência:** (1) a fonte que o próprio edital cita; (2) norma oficial (Planalto, DOU, site do órgão); (3) especificação ou padrão oficial (RFC, OWASP, NIST, Scrum Guide, documentação oficial de Java, Spring, Vue); (4) livro consagrado; (5) referência acadêmica, para itens de ciências sociais.
- **Catálogo curado pelo Gunter.** Ele sabe qual autor o Cebraspe costuma seguir em cada área. Um arquivo de catálogo no template, que o agente consulta primeiro e só abandona com justificativa, resolve o "nada obscuro" melhor do que o critério do modelo.
- **Agrupamento usando o edital.** No exemplo do Gunter, o edital ajuda a decidir o escopo: o cargo de Desenvolvimento da CGU nomeia Java, Spring, Spring Boot, JPA, Spring Data JPA, Spring Batch, JavaScript e Vue.js, OAuth 2.0, OpenID Connect, Scrum e Kanban. PHP não aparece, então a pergunta certa ao aluno é se ele quer mesmo estudar PHP. E a pergunta de abordagem por grupo é: estudar o conceito que atravessa as tecnologias ou cada tecnologia em profundidade?
- Saída: um mapa item → fonte → localizador (artigo, capítulo, seção) → situação (sugerida, verificada, baixada).
- **Livros**: só cópia legítima. Mapear item → capítulo pelo sumário e carregar só os capítulos mapeados. Subir o livro inteiro piora as respostas. PDF cujo texto não dá para selecionar é imagem escaneada e precisa de OCR.
- **Leis**: guardar a versão vigente na data do edital, com a data. Se a lei mudar depois, a versão compilada do Planalto deixa de ser a cobrada.

### 7.3 Questões do TEC

**Pedido.** O aluno pede ao agente questões do TEC sobre um assunto. O agente busca no navegador (o Gunter não sabe se isso funciona no navegador do Claude Code), pega as questões e registra num arquivo. Ele perguntou se vale ter um SQLite.

**Situação: em aberto por decisão do Gunter.** O que já foi levantado:

- **Caminho A, PDF do caderno.** O aluno monta o caderno no TEC (filtro por banca e assunto, excluindo anuladas e desatualizadas) e exporta o PDF; o agente extrai. O extrator do motor de questões já faz isso. Prós: sem robô, sem risco para a conta, robusto. Contras: um passo manual; o PDF não traz o percentual de acertos.
- **Caminho B, navegador.** Agentes de programação conseguem controlar um navegador com o login do próprio aluno (verificar o que Claude Code e Codex suportam hoje). Prós: menos passos para o aluno. Contras: os termos de uso de plataformas desse tipo costumam proibir extração automatizada (os do TEC **não foram conferidos**); quem arrisca é a conta do aluno; quebra quando a página muda ou aparece captcha; gasta mais tokens.
- Sugestão do Claude, ainda não aceita: A como padrão e B como opção, lenta e com aviso. Conferir os termos do TEC antes de qualquer coisa.
- **Papel das questões reais:** mostrar como a banca pergunta; dar cobertura por item (quais ids têm questão real e quais não têm, o que diz onde a geração é necessária). Onde o TEC cobre bem, o aluno pode continuar resolvendo no próprio TEC, que tem estatística e comentários, e só registrar o resultado por id.
- **Armazenamento** (o Gunter escolheu texto, não SQLite): questões em JSONL, porque têm enunciado longo, alternativas e comentários; respostas e matriz em CSV. Campos mínimos de uma questão: código do TEC, banca, órgão, ano, cargo, enunciado, tipo (certo/errado ou múltipla escolha), gabarito definitivo, flags de anulada e desatualizada, assuntos do TEC, **lista** de ids do edital (um item pode cruzar vários objetos, 15.1.2), origem (real ou gerada) e, para gerada, o trecho de fonte que a sustenta. Deduplicar pelo código. Se um dia as consultas pesarem, um SQLite pode ser um índice derivado dos arquivos, não a fonte de verdade.

### 7.4 Treino, feedback, análise e materiais enxutos

**Pedido.** Toda a parte de treino, feedback didático, análise do conhecimento a partir de como as perguntas foram respondidas, e elaboração de materiais super enxutos para as próximas sessões.

**Propostas:**

- **Treino por id**: primeiro as questões reais do id; questões geradas só se faltarem. A geração parte apenas da ficha do id (os trechos de fonte), com metade dos itens em situação-problema e as pegadinhas típicas da banca (conceitos parecidos trocados, generalização indevida, competência invertida, exceção tratada como regra). O script confere se o trecho citado existe na fonte; sem trecho, o item é descartado.
- **Resposta simples**: `1C 2E? 3B` (C certo, E errado, B em branco, "?" respondeu na dúvida). Nada além disso.
- **Correção** item a item, com a origem marcada (princípio 4). Explica o ponto específico que falhou, pede que o aluno explique com as próprias palavras, avalia e libera 2 ou 3 itens novos do mesmo id.
- **Registro automático** por sessão, uma linha por item respondido. Agregação por id e por matéria via script.
- **Análise por script**: por id, acertos, erros sem dúvida, acertos com dúvida, brancos e a última vez que o id foi visto. Prioridade conforme o princípio 8. Um indicador de **calibração**: quanto das respostas "sem dúvida" estava errado. Em prova com penalidade, isso diz se o aluno deveria deixar mais itens em branco.
- **Materiais super enxutos = caderno de erros por id.** Uma nota de poucas linhas com o conceito que falhou, o trecho da fonte e a pegadinha que pegou o aluno. Nasce do erro real, não do resumo do capítulo, e volta em intervalos crescentes (por exemplo 1, 3, 7 e 21 dias; calibrar). Combina com o formato de "teoria enxuta" que o Gunter já usa nas aulas.
- **Pré-teste** ao começar uma matéria: diagnóstico inicial e efeito pré-teste.
- **Exportação** por matéria no formato da planilha da aplicação de ciclo de estudos (formato a pedir ao Gunter).
- **Auditoria por exceção** (princípio 9), de preferência rodando a outra ferramenta: o que foi gerado no Claude Code é conferido no Codex, e vice-versa.

### 7.5 O que o Claude acrescentaria (propostas)

- **Onboarding** para quem nunca usou IA: um comando de início que pergunta concurso e cargo, recebe o edital e sugere começar por 2 ou 3 matérias prioritárias.
- **Vigência**: verificar retificação do edital e mudança nas leis mapeadas, e congelar a versão da data do edital.
- **Separar o template dos dados do aluno.** Instruções, comandos e scripts de um lado; edital, fontes, questões e progresso do aluno do outro, numa pasta ignorada pelo git. Assim a atualização do template não conflita com os dados, e conteúdo de terceiros nunca vai parar no repositório público.
- **Permissões** restritas: o agente lê as fontes e escreve só nas pastas de dados, nunca fora do repositório.
- **Contexto enxuto**: carregar só a ficha do id da vez, não a lei inteira. Economiza limite de uso e melhora a precisão.
- **Adaptadores finos por ferramenta**: a lógica em markdown neutro e Python, o `CLAUDE.md` apontando para o `AGENTS.md`, e uma verificação de como cada ferramenta implementa comandos e skills hoje, antes de escolher o formato.

## 8. Decisões tomadas

- Repositório público `guntribam/agente-estudos`, clonado em `C:\Users\Gunter\devestavel\agente-estudos`.
- Template genérico para qualquer concurso. A CGU (Cebraspe, certo/errado) é o caso de teste.
- Roda em Claude Code e Codex. Não depender de um fornecedor.
- Dados em texto (CSV e JSONL), não SQLite. Escolha feita na criação do repositório; é a direção, revisável se as consultas pesarem.
- Não construir aplicação para os alunos. O template é uma pasta com instruções, comandos e scripts pequenos.
- Os princípios da seção 5, que saíram do desenho aprovado na conversa.
- A marca é DevEstavel, sem acento, em qualquer texto voltado ao aluno.

## 9. Em aberto

- **TEC**: PDF ou navegador (7.3). Conferir os termos de uso do TEC.
- **Estrutura**: pastas, nomes de arquivo e esquema exato dos dados.
- **Comandos e skills**: a lista final e como implementar em cada ferramenta.
- **Granularidade dos ids** (7.1).
- **Formato de exportação** para a aplicação de ciclo de estudos (pedir a planilha ao Gunter).
- **Quem monta o quê.** Na conversa, a montagem pesada ficaria com o Gunter, uma vez por edital (pacote por concurso). Com o agente, parte disso pode ser feita pelo próprio aluno a partir do edital. Decidir o equilíbrio.
- **Estrutura da prova da CGU**: penalidade, número de itens, pesos e se há discursiva. O trecho que temos não traz. Discursiva, se houver, é outra frente: questão objetiva não cobre.
- **Itens sem fonte normativa** (ciências sociais): como gerar ou se não gerar.

## 10. Evidências e fatos verificados

### Pesquisa que fundamenta o desenho

- **StudentBench** (Handshake AI, set/2026, https://arxiv.org/pdf/2609.28470; código em github.com/handshake-ai-research/studentbench, dados no Hugging Face). Estudo com 2.383 participantes: pré-teste, uma hora de tutoria (IA, tutor humano especialista ou nenhuma), pós-teste com questões diferentes, em questões do GRE. Achados:
  - tutoria por IA, somando os 13 tutores, teve ganho estatisticamente equivalente ao do tutor humano (p = .015). Ganho ajustado: tutores de IA de 12,1 a 16,0 pontos percentuais, tutor humano 14,9, sem tutoria 7,8;
  - entre os 12 tutores de IA comparados, o teste não encontrou diferença significativa de ganho (p = .755). Ou seja: o modelo importa menos que o processo;
  - especialistas preferiram os modelos Opus para plano de aula e criação de exercícios;
  - um modelo aberto e leve (Gemma 4 31B) chegou ao nível humano com custo centenas de vezes menor;
  - resposta mais rápida levou a mais mensagens do aluno, mais exercícios certos e mais aprendizado (parte quantitativa). O que move o resultado é a prática;
  - alunos contestaram cerca de 11% das respostas de exercícios do pior modelo nesse quesito. Gabarito gerado erra;
  - limites: GRE, em inglês, ganho imediato, sem medir retenção.
  - **Lições de desenho tiradas dos prompts publicados (apêndice A.5)**: o tutor recebe o pré-teste completo (questão, resposta do aluno, gabarito, acerto e tempo gasto em cada item); o plano sai em JSON com conceitos priorizados, tempo e exercícios com resolução comentada; a instrução manda **verificar cada exercício antes de incluí-lo** (resolver, confirmar que só uma alternativa é correta, confirmar que cada distrator está errado); ensinar o conceito transferível, nunca a resposta decorada; linguagem de apoio, sem rótulos negativos; e o aluno tinha um botão "discordo desta resposta". O equivalente no nosso desenho é o gatilho de auditoria quando o aluno discorda.
- **Bastani et al., PNAS, 2025** (doi.org/10.1073/pnas.2422633122): com IA sem limites, alunos de matemática do ensino médio foram melhor no treino e pior na prova feita sem ajuda. A IA serve para praticar, não para entregar a resposta.
- **Dunlosky et al., 2013** (Psychological Science in the Public Interest, 14(1)): entre dez técnicas de estudo, só praticar com testes e espaçar o estudo tiveram utilidade alta; reler e grifar ficaram embaixo.
- **Efeito pré-teste** (Richland, Kornell e Kao, 2009): tentar responder antes de estudar melhora o aprendizado depois, mesmo errando.
- **Reversão da expertise** (Kalyuga et al., 2003) e **exemplos resolvidos** (Sweller e Cooper, 1985; Renkl, 2014): para iniciante, exemplo resolvido e explicação estruturada rendem mais que resolver problema; para quem já domina, o contrário.
- **Auto-explicação** (Chi et al., 1994): pedir que o aluno explique melhora o entendimento. Base do passo "explique com as suas palavras".

### Fatos de plataforma (conferidos em 27/10/2026)

- Claude Code exige plano Pro, Max, Team, Enterprise ou conta de API; o plano grátis não inclui. O limite de uso é compartilhado entre o chat e o Claude Code (code.claude.com/docs/en/getting-started/installation; support.claude.com, artigo 11145838).
- Projeto do Claude só pode ser compartilhado nos planos Team e Enterprise, entre membros da mesma organização (support.claude.com, artigo 9517075).
- A OpenAI anunciou em 11/09/2026 que os GPTs personalizados serão aposentados em favor de plugins, com prazo variando por plano (help.openai.com, notas de versão do ChatGPT).
- Gems do Gemini podem ser compartilhados por link; o NotebookLM permite caderno público.
- O DeepSeek Harness (ideia inicial do Gunter) é um runtime de agente em que tudo é plugin, ainda em prévia, com mudanças incompatíveis esperadas.

## 11. O exemplo CGU

Arquivos em `docs/exemplo-cgu/`. O trecho cobre os itens 14.28 a 15 do edital: regras finais e todo o conteúdo programático. Não traz estrutura da prova, número de itens, pesos nem penalidade.

**Estrutura** (macrotópico > matéria):

- **Conhecimentos básicos** (todos os cargos): Estado, Democracia, Direitos e Ciência Política; Sociedade Brasileira, Desigualdades, Diversidade e Desenvolvimento; Ética Pública e Responsabilidade Profissional; Administração Pública e Fundamentos de Políticas Públicas.
- **Conhecimentos complementares** (todos os cargos): Fundamentos de Governança, Riscos e Integridade Pública e Privada; Fundamentos de Transparência, Ouvidoria e Participação Social; Fundamentos de Direito Público Aplicado, Controle e Responsabilização; Fundamentos de Evidências, Dados e Inteligência Artificial; Fundamentos de Auditoria Governamental e Atuação Integrada da CGU.
- **Conhecimentos específicos**, por cargo (todos Auditor Federal de Finanças e Controle):
  - Auditoria: Auditoria Governamental: Avaliação, Consultoria e Apuração; Finanças Públicas, Orçamento e Contabilidade Pública; Políticas Públicas e Métodos de Investigação e Avaliação; Auditoria de Contratações, Transferências e Execução de Recursos; Integridade, Transparência e Responsabilização Aplicadas ao Controle Público.
  - TI, Ciência de Dados: Estatística, Programação e Análise de Dados; Engenharia, Arquitetura e Governança de Dados; Aprendizado de Máquina e Inteligência Artificial; Operação, Governança e Gestão de Soluções de Dados e IA.
  - TI, Infraestrutura: Redes, Sistemas e Plataformas de Dados; Computação em Nuvem, Virtualização e Automação; Cibersegurança, Privacidade e Continuidade de Serviços; Operação, Governança e Gestão de Serviços Digitais.
  - TI, Desenvolvimento de Sistemas: Engenharia de Software e Programação; Arquitetura e Integração de Sistemas; Persistência, Integração e Proteção de Dados; Desenvolvimento Seguro, Qualidade e Gestão da Entrega.

**Itens do edital que mudam o desenho** (texto literal):

- 14.32: "As alterações de legislação com entrada em vigor até a data de publicação deste edital serão objeto de avaliação, ainda que não contempladas nos objetos de avaliação constantes do item 15 deste edital."
- 14.33: "A legislação que não esteja em vigor pode ser cobrada, desde que devidamente explicitada nos objetos de avaliação."
- 14.33.1: "As jurisprudências dos tribunais superiores poderão ser consideradas para fins de elaboração de itens desde que publicadas até 30 dias antes da data de realização das provas."
- 15.1.1: "Os itens das provas poderão avaliar habilidades que vão além do mero conhecimento memorizado, abrangendo compreensão, aplicação, análise, síntese e avaliação, com o intuito de valorizar a capacidade de raciocínio."
- 15.1.2: "Cada item das provas poderá contemplar mais de um objeto de avaliação."

**Por que Ética Pública é o primeiro corte vertical.** A fonte é pequena e fechada e o próprio edital cita os artigos:

- 3.1: "Identificação de interesses privados em conflito com a função pública e medidas de prevenção, consulta e encaminhamento, nos termos dos arts. 3º a 5º, 8º e 10 da Lei nº 12.813/2013."
- 3.2: "Impedimento e suspeição no processo administrativo federal, nos termos dos arts. 18 a 21 da Lei nº 9.784/1999; comunicação e abstenção quando exigidas."
- 2.2: "Aplicação dos valores e deveres de conduta ética da CGU a situações de trabalho." (fonte: código de conduta da CGU; localizar a versão oficial).

**Item de exemplo, conferido no texto da Lei 12.813/2013 no Planalto:**

> Um servidor do Poder Executivo federal presta, de forma apenas eventual, consultoria a uma empresa fiscalizada pelo órgão ao qual está vinculado. Como não há habitualidade, não se configura conflito de interesses.

Gabarito: errado. O art. 5º, VII, configura conflito ao "prestar serviços, ainda que eventuais, a empresa cuja atividade seja controlada, fiscalizada ou regulada pelo ente ao qual o agente público está vinculado", e o art. 10 estende o art. 5º a todos os agentes públicos do Executivo federal. A armadilha é a generalização indevida ("como não há habitualidade").

**Contraexemplo, item sem fonte normativa**: Sociedade Brasileira 2.1, "Heranças da escravidão, hierarquias sociais e construção da cidadania".

## 12. Como começar

1. Leia este documento, `docs/rascunhos-de-prompts.md` e `docs/exemplo-cgu/edital-cgu-conteudo.txt`.
2. Não escreva código nem crie estrutura ainda.
3. Devolva ao Gunter, nesta ordem:
   - o seu entendimento do problema, em poucas linhas e com as suas palavras;
   - o que você acha frágil, arriscado ou discorda neste documento (inclusive nas propostas do Claude da seção 7);
   - as perguntas que precisam de resposta para fechar os itens da seção 9;
   - duas ou três opções de estrutura do template, com trade-offs.
4. Primeiro corte vertical sugerido: CGU, Ética Pública, itens 3.1 e 3.2, indo do edital ao diagnóstico.
5. Escreva para o aluno em português natural, sem cara de texto gerado por IA, e com a marca escrita DevEstavel.
