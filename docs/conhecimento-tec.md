# Conhecimento sobre o TEC Concursos

O que o Gunter ensinou sobre navegar no TEC, para virar instrução da skill `questoes`. Vai sendo completado a cada sessão.

## Regra geral

Buscar assunto navegando pela árvore de matérias e assuntos. O "Pesquisar por nome" só entra em último caso: navegando, o agente aprende a taxonomia do TEC; pesquisando por nome, não aprende.

## Página de filtragem

- Endereço: `https://www.tecconcursos.com.br/questoes/filtrar` (menu Estudo > Filtrar questões). Exige login, feito pelo aluno.
- No topo: Objetivas (todas), Objetivas (inéditas), Discursivas.
- Filtros na coluna da esquerda: Matéria e assunto, Banca, Órgão e cargo, Ano, Área (Carreira), Escolaridade, Formação, Região, Favoritas, Enunciados, Opções.
- À direita: filtros ativos, total de questões encontradas e o botão para gerar caderno numa pasta.

## A árvore de matérias e assuntos

- O primeiro nível são matérias com nomes próprios do TEC, que não seguem o edital (ex.: "Direito Constitucional (CF/1988 e Doutrina)").
- Cada pasta aberta começa com um item "Todo o conteúdo de ..." (seta azul), que seleciona a pasta inteira.
- Pastas têm ícone de pasta e se abrem. Itens finais, sem filhos, aparecem com seta verde.
- Muitos nomes trazem os artigos da lei entre parênteses, o que ajuda a casar com itens do edital que citam artigos.
- Existem nós de sobra que não são assunto: "Questões Mescladas de ..." (questões que cruzam vários filhos da pasta) e "Questões sem classificação de assunto".

## Exemplo: habeas corpus

Caminho:

```
Direito Constitucional (CF/1988 e Doutrina)
  > Dos Direitos e Garantias Fundamentais (arts. 5º a 17 da CF/1988)
    > Remédios Constitucionais (art. 5º, LXVIII a LXXIII e LXXVII da CF/1988)
      > Habeas Corpus
```

Irmãos de Habeas Corpus: Mandado de Segurança, Mandado de Injunção, Habeas Data, Ação Popular e Questões Mescladas de Remédios Constitucionais.

- A árvore inteira já vem carregada na página, mesmo com as pastas fechadas. Para planejar o caminho, o agente lê os títulos (`li.arvore-item`, atributo `title`) pela ferramenta de JavaScript, sem abrir pasta por pasta. Para selecionar um item, porém, as pastas acima dele precisam estar abertas, porque só dá para clicar no que está visível.

## A taxonomia do TEC não bate um para um com o edital

- O edital pode ser mais fino que a árvore. Exemplo: o edital pede "mandado de segurança coletivo", mas no TEC só existe "Mandado de Segurança" (item final, sem filhos). As questões do coletivo muito provavelmente estão dentro dele.
- Nesses casos, usar o filtro Enunciados para buscar pelo texto (ex.: "mandado de segurança coletivo"). O termo aparece em Filtros ativos como "Enunciado: mandado de seguranca coletivo".
- Busca por enunciado sozinha pega questões de qualquer matéria. Enunciado "mandado de seguranca coletivo" + só a banca CEBRASPE deu 307 questões (27/10/2026). Por isso, ao buscar enunciado de um assunto, filtrar também pela matéria (ou pela pasta) correspondente na árvore.
- Com a matéria inteira selecionada ("Todo o conteúdo de Direito Constitucional"), os itens de dentro ficam com seta cinza, e o resultado caiu de 307 para 142 questões.
- A busca por enunciado acha questões que o TEC classificou em outro assunto. A primeira das 142 estava em "Gerações de Direitos Fundamentais" (#329026, CEBRASPE 2016, Analista Judiciário TRE-PI). Filtrar só por "Mandado de Segurança" teria perdido essa questão.
- Busca por enunciado traz falso positivo (o termo aparece, mas o item cobra outra coisa). A skill confere cada questão ao guardar.

## Exemplo: PPA, LDO e LOA (teste de 27/10/2026)

Item do edital CGU, Finanças Públicas, Orçamento e Contabilidade Pública, 2.1 "PPA, LDO e LOA em aplicação". Caminho:

```
AFO, Direito Financeiro e Contabilidade Pública
  > Orçamento Público
    > Instrumentos Orçamentários na CF 88 (PPA, LDO e LOA)
      > PPA - Plano Plurianual (CF/1988 e Lei nº 4.320/1964)
      > LDO - Lei de Diretrizes Orçamentárias (CF/1988 e Lei nº 4.320/1964)
      > LOA - Lei Orçamentária Anual (CF/1988 e Lei nº 4.320/1964)
      > Tópicos Mesclados de PPA, LDO e LOA
      > Vedações Constitucionais em Matéria Orçamentária (Art. 167 da CF/1988)   (não selecionado)
```

Os quatro primeiros + CEBRASPE + 2021 a 2026 deram 395 questões. A coleta de 5 levou uns 3 segundos, numa chamada só.

As 5 primeiras vieram todas de PPA e quase todas da mesma prova (TELEBRAS 2026), porque a lista vem agrupada por assunto e prova. Para o Gunter isso não é problema: o que importa é a filtragem estar certa.

## Gravar as questões

- Arquivo `estudo/questoes.jsonl`, uma questão por linha. A pasta `estudo/` está no `.gitignore`: fica só no computador do aluno.
- Cada linha é o JSON do coletor, com `ids` (itens do edital, lista) e `origem` (`tec` ou `gerada`) no começo.
- Quem grava é o script `docs/registrar-questoes.py`, não a IA à mão: `uv run docs/registrar-questoes.py coletadas.json --ids FINPUB-2.1`. Questão repetida (mesmo `tec_id`) não duplica; só ganha os ids novos. Testado em 27/10/2026 com as 5 questões de PPA.

## Selecionar um assunto

- Clicar num item de seta verde seleciona o assunto: a seta vira um X vermelho, e o item aparece em "Filtros ativos" (ex.: "Assunto: Habeas Corpus"). Clicar no X desfaz a seleção.
- O total de questões é atualizado na hora. Habeas Corpus sozinho deu 276 questões (27/10/2026, sem outros filtros).
- Quando há filtro ativo, aparece "Limpar" (tira todos os filtros) e, no painel da direita, as opções "Remover anuladas" e "Remover desatualizadas", além de "Salvar" e "Carregar" filtros.

## Filtrar por banca

- Na aba Banca, pesquisar pelo nome é o caminho normal: é uma lista simples, sem taxonomia para aprender. O Gunter digitou "cebr".
- O nome no TEC é "CEBRASPE (CESPE)". Selecionada, aparece em Filtros ativos como "Banca: CEBRASPE (CESPE)".
- Filtros de abas diferentes se combinam: Habeas Corpus + CEBRASPE (CESPE) caiu de 276 para 68 questões (27/10/2026).

## Filtrar por ano

- Na aba Ano, a lista vai do ano mais recente para trás, e cada ano se seleciona separadamente (não há intervalo). Cada ano vira um filtro ativo ("Ano: 2026", "Ano: 2025"...).
- O Gunter selecionou de 2021 a 2026, os últimos seis anos. Habeas Corpus + CEBRASPE + 2021 a 2026 deu 15 questões (27/10/2026).
- Regra do corte: começar pelos anos recentes. Se vierem questões suficientes, ótimo; se vierem poucas, ir acrescentando anos para trás. O quanto é "suficiente" depende do assunto. No exemplo, estender até 2015 deu 18 questões, e até 2014, 21.

## Nível do concurso

- Questões de cargos muito acima do concurso do aluno mais atrapalham que ajudam. Para a CGU, por exemplo, juiz, promotor e delegado.
- Esse corte NÃO é feito no TEC. Filtrar ali arrisca filtrar errado e perder questões. A skill `questoes` traz tudo e guarda o cargo de cada questão; quem decide o que usar é o `treino`, na hora de calibrar.

## Quantas questões trazer

- Para começar um tópico, 10 a 15 questões já está bom.
- Se mesmo recuando os anos não aparecerem muitas, tudo bem: às vezes não existe tanta questão sobre o assunto.

## Questões na própria página

- Abaixo dos filtros, a página já mostra as questões encontradas ("Questão 1 de 18", com a matéria), sem precisar gerar caderno.
- Antes da lista ficam os campos do caderno: Nome do caderno, Pasta de destino, "Gerar cadernos em série" e o botão GERAR CADERNO.
- Cada questão mostra: "Questão N de T", matéria, assunto, código (ex.: `#3962903`), banca, ano, órgão e cargo (ex.: "CEBRASPE (CESPE) - 2026 - Técnico Legislativo (CAM DEP)/Policial Legislativo Federal"), o enunciado de comando ("Julgue o item que se segue...") e o item, com as opções Certo e Errado.
- Na barra da questão há ícones para comentário do professor, comentários dos alunos (com contador), favoritar, anotar e estatísticas. Setas passam para a questão anterior ou a próxima.
- O gabarito aparece depois de responder ("RESOLVER QUESTÃO").
- Fluxo da skill: navegar pelas questões, ler os comentários (o do professor principalmente), responder para ver o gabarito e guardar cada questão conforme encontra.

## Capturar a questão em JSON

- Não ler a questão por print nem pelo texto da página. Rodar `docs/tec-coletar-questoes.js` pela ferramenta de JavaScript do navegador: devolve as questões já em JSON, numa chamada só, gastando muito menos limite. Com `QUANTAS = 1` e `RESPONDER = false`, só lê a questão aberta. Com `QUANTAS = n` e `RESPONDER = true`, na página de filtro, marca a primeira alternativa, resolve, extrai e passa para a próxima, n vezes.
- O script é a parte de extração do userscript "TEC Concursos → JSON + Coleções", do Gunter, sem painel, coleções, localStorage, clipboard ou atalhos. Acrescenta `cargo` (o que vem depois do ano em "prova") e devolve o gabarito sempre como letra (C/E nas de certo/errado).
- Campos: `tec_id`, `link`, `banca`, `ano`, `orgao`, `cargo`, `prova`, `materia`, `assunto`, `formato_item`, `texto_associado`, `enunciado`, `alternativas`, `gabarito`, `anulada`, `tem_imagem`, `imagens`, `pct_acertos`, `capturado_em`. Os ids do edital o agente acrescenta depois, ao classificar a questão.
- Testado em 27/10/2026 na questão #3291915: saiu igual ao JSON da extensão, mais o `cargo`. Sem responder, `gabarito` vem `null`. Depois de responder, veio `"gabarito": "E"`.
- Como responder: clicar numa alternativa (o agente marca qualquer uma, por exemplo a primeira) e em "RESOLVER QUESTÃO". A página mostra "Você errou! Gabarito: Errado. Ver resolução" (ou o equivalente de acerto), e aí o extrator pega o gabarito. `pct_acertos` continuou `null`: o percentual não aparece nessa tela.
- Toda questão tem endereço próprio: `https://www.tecconcursos.com.br/questoes/<tec_id>`.
- A página de uma questão abre e o extrator funciona mesmo sem login. Para resolver, precisa de login: sem ele, "Resolver Questão" leva para a tela de login ("Faça o login novamente para continuar").
- O login tem reCAPTCHA. Quem faz é sempre o aluno; o agente pede e espera.
- O login do navegador embutido pode se perder (aconteceu em 27/10/2026, depois que o painel do navegador fechou e reabriu). Antes de resolver questões, conferir o login pelo texto da página ("Seja bem-vindo" e "Sair"), e não pelo print: com o painel estreito, o cabeçalho vira um menu recolhido e o "Seja bem-vindo" some da tela, mas continua na página.
- Seletores usados na coleta: primeira alternativa `#label-alternativa-0`, botão resolver `.botao-resolver`, próxima questão `.questao-navegacao-botao-proxima.ng-isolate-scope` (há também "Próxima não resolvida", tecla N).
- O total de questões às vezes demora a atualizar depois de um filtro; conferir de novo antes de decidir recuar nos anos.
- Atalhos de teclado do TEC na questão: `o` comentário da questão, `t` teoria, `f` fórum, Enter resolve. Ao responder, a resposta entra nas estatísticas do aluno no TEC.
