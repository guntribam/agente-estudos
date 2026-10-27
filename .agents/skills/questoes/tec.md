# O TEC Concursos por dentro

O que se sabe do site, aprendido com o Gunter e testado em outubro de 2026. Se algo não bater com o que você vê, o site mudou: avise o aluno no fim, para o mantenedor atualizar este arquivo.

## Login

- O aluno entra com a conta dele. O login tem reCAPTCHA; você nunca digita senha nem resolve captcha. Peça e espere.
- Confira o login pelo texto da página, não por print. Com a janela estreita, o cabeçalho vira um menu recolhido e o "Seja bem-vindo" some da tela, mas continua na página:
  ```js
  (() => { const t = document.body.textContent; return /Seja bem-vindo/i.test(t) && /\bSair\b/.test(t); })()
  ```
- O login pode se perder (já aconteceu depois de o navegador fechar e abrir de novo). Sem login, a questão abre e dá para ler, mas "Resolver Questão" leva para a tela de login ("Faça o login novamente para continuar").

## Página de filtro

- Endereço: `https://www.tecconcursos.com.br/questoes/filtrar` (menu Estudo > Filtrar questões).
- No topo: Objetivas (todas), Objetivas (inéditas), Discursivas. Use "Objetivas (todas)".
- Coluna da esquerda, as abas de filtro: Matéria e assunto, Banca, Órgão e cargo, Ano, Área (Carreira), Escolaridade, Formação, Região, Favoritas, Enunciados, Opções.
- À direita: os filtros ativos, o total de questões encontradas e, com algum filtro ativo, "Limpar", "Salvar", "Carregar" e as opções "Remover anuladas" e "Remover desatualizadas".
- O total às vezes demora a atualizar depois de um clique. Confira de novo antes de decidir recuar nos anos.
- Abaixo dos filtros, a página já mostra as questões encontradas ("Questão 1 de N"), uma por vez, com setas para a anterior e a próxima. Não precisa gerar caderno.

## A árvore de matérias e assuntos

- O primeiro nível são matérias com nomes do próprio TEC, que não seguem o edital (ex.: "Direito Constitucional (CF/1988 e Doutrina)", "AFO, Direito Financeiro e Contabilidade Pública").
- Pastas têm ícone de pasta e se abrem com um clique no nome. Itens finais aparecem com seta verde; clicar seleciona o assunto, a seta vira um X vermelho e o assunto entra em "Filtros ativos". Clicar no X desfaz.
- Toda pasta aberta começa com "Todo o conteúdo de ..." (seta azul), que seleciona a pasta inteira. Com a pasta inteira marcada, os itens de dentro ficam com seta cinza.
- Muitos nomes trazem os artigos da lei entre parênteses, o que ajuda a casar com itens do edital que citam artigos.
- Há nós que não são assunto: "Questões Mescladas de ..." / "Tópicos Mesclados de ..." (questões que cruzam vários irmãos; marque quando o item do edital cobre esses irmãos juntos) e "Questões sem classificação de assunto".
- A árvore inteira já vem carregada na página, mesmo com as pastas fechadas. Para navegar sem abrir pasta por pasta, liste os filhos de uma pasta pelo título exato (deixe `PASTA` vazio para o primeiro nível):
  ```js
  (() => {
    const PASTA = 'AFO, Direito Financeiro e Contabilidade Pública';
    const titulo = (li) => (li.getAttribute('title') || '').trim();
    const itens = [...document.querySelectorAll('li.arvore-item')];
    const lista = PASTA ? itens.find((li) => titulo(li) === PASTA)?.querySelector('ul') : itens[0]?.parentElement;
    return [...(lista?.children || [])].map((li) => titulo(li) + (li.classList.contains('arvore-item-pasta') ? ' [pasta]' : ''));
  })()
  ```
  Desça nível por nível, escolhendo a pasta pelo sentido do item do edital. Para clicar num item, as pastas acima dele precisam estar abertas: só dá para clicar no que está visível.

Caminhos já usados:

```
Direito Constitucional (CF/1988 e Doutrina)
  > Dos Direitos e Garantias Fundamentais (arts. 5º a 17 da CF/1988)
    > Remédios Constitucionais (art. 5º, LXVIII a LXXIII e LXXVII da CF/1988)
      > Habeas Corpus | Mandado de Segurança | Mandado de Injunção | Habeas Data | Ação Popular

AFO, Direito Financeiro e Contabilidade Pública
  > Orçamento Público
    > Instrumentos Orçamentários na CF 88 (PPA, LDO e LOA)
      > PPA - Plano Plurianual (CF/1988 e Lei nº 4.320/1964)
      > LDO - Lei de Diretrizes Orçamentárias (CF/1988 e Lei nº 4.320/1964)
      > LOA - Lei Orçamentária Anual (CF/1988 e Lei nº 4.320/1964)
      > Tópicos Mesclados de PPA, LDO e LOA
      > Vedações Constitucionais em Matéria Orçamentária (Art. 167 da CF/1988)
```

## Banca, ano e enunciado

- **Banca:** na aba Banca, "Pesquisar por nome" é o caminho normal, porque é uma lista simples. O Cebraspe aparece como "CEBRASPE (CESPE)".
- **Ano:** a lista vai do mais recente para trás, e cada ano se marca separadamente; não há intervalo. Comece pelos últimos anos e acrescente para trás enquanto vierem poucas questões. Exemplo: Habeas Corpus + Cebraspe deu 15 questões de 2021 a 2026, 18 até 2015 e 21 até 2014.
- **Enunciado:** a aba Enunciados busca um termo no texto da questão; o filtro aparece como "Enunciado: termo". Sozinha, a busca pega questões de qualquer matéria: "mandado de seguranca coletivo" + Cebraspe deu 307 questões; com a matéria Direito Constitucional junto, 142. Ela acha questões que o TEC classificou em outro assunto (uma delas estava em "Gerações de Direitos Fundamentais") e também traz falso positivo. Confira cada questão antes de registrar.
- A lista de questões vem agrupada por assunto e por prova. As primeiras costumam ser do mesmo assunto e da mesma prova; isso não é problema, o que importa é o filtro estar certo.

## A questão

- Cada questão mostra matéria, assunto, código (`#3291915`), banca, ano, órgão e cargo ("CEBRASPE (CESPE) - 2025 - Analista ... /Sistemas e Governança de TI"), o comando ("Julgue o item a seguir") e o item, com Certo e Errado ou com as alternativas.
- Na barra da questão: comentário do professor (tecla `o`), teoria (`t`), fórum dos alunos (`f`), favoritar, anotar e estatísticas. Os comentários ajudam a entender um gabarito, mas não são guardados.
- O gabarito só aparece depois de responder: marcar uma alternativa e clicar em "RESOLVER QUESTÃO" (ou Enter). A página mostra, por exemplo, "Você errou! Gabarito: Errado". A resposta entra nas estatísticas do aluno no TEC.
- Toda questão tem endereço próprio: `https://www.tecconcursos.com.br/questoes/<tec_id>`.

## Coletar com o script

Não leia questões por print nem pelo texto da página. Leia o arquivo `scripts/tec-coletar-questoes.js`, ajuste no texto as duas constantes do começo da função e rode o arquivo inteiro pela ferramenta de executar JavaScript na página:

- **Coletar na página de filtro:** `QUANTAS` = quantas questões, `RESPONDER = true`. A partir da questão que está na tela, para cada uma: marca a primeira alternativa, resolve, extrai e passa para a próxima. Cinco questões levam uns 3 segundos, numa chamada só.
- **Ler só a questão aberta, sem tocar em nada:** `QUANTAS = 1`, `RESPONDER = false`. O gabarito vem `null` se a questão não estiver respondida.

O resultado é `{ "sha256": "...", "questoes": [...] }`. Cada questão traz `tec_id`, `link`, `banca`, `ano`, `orgao`, `cargo`, `prova`, `materia`, `assunto`, `formato_item`, `texto_associado`, `enunciado`, `alternativas`, `gabarito` (sempre a letra: C/E no certo/errado), `anulada`, `tem_imagem`, `imagens`, `pct_acertos` (essa tela não mostra o percentual; costuma vir `null`) e `capturado_em`.

Seletores que o script usa, para quando o site mudar: enunciado `.questao-enunciado-texto`, cabeçalho `.questao-cabecalho-informacoes-materia`, alternativas `.questao-enunciado-alternativas li`, resolução `.questao-enunciado-resolucao`, primeira alternativa `#label-alternativa-0`, botão resolver `.botao-resolver`, próxima questão `.questao-navegacao-botao-proxima.ng-isolate-scope`.
