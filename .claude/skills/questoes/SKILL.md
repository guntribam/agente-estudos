---
name: questoes
description: Busca questões reais da banca no TEC Concursos pelo navegador, na conta do aluno, e guarda em estudo/questoes.jsonl ligadas aos itens do edital, como referência para o treino. Use quando o aluno pedir questões do TEC sobre um assunto ou quando o treino precisar de questões reais de um item.
---

# Questões

Junta questões reais da banca, do TEC Concursos, sobre um item do edital. Elas são material de referência, como as fontes: mostram como a banca cobra, o estilo, as pegadinhas e o que ela deu como certo. O aluno não resolve essas questões aqui; quem as usa é o treino.

Pré-requisitos:
- `estudo/edital.md`, para os ids e a banca. Se não existir, comece pela skill `edital`.
- Um navegador que você controle, com a ferramenta de executar JavaScript na página (no Claude Code, o navegador embutido do app desktop ou a extensão Claude in Chrome). Sem navegador, diga ao aluno que esta parte precisa dele e pare.

**Antes de começar, leia `tec.md`, nesta mesma pasta.** Ele tem o que se sabe do site: a árvore de assuntos, os filtros, os seletores e os tropeços já vistos.

## Conversa com o aluno

```
aluno:  traz questões de conflito de interesses
você:   Trouxe 14 questões do Cebraspe sobre conflito de interesses (3.1).
        Sobre o código de conduta da CGU (2.2) não achei nenhuma; ali o treino
        vai se apoiar nas fontes.
```

## Passo a passo

1. **Item e recorte.** Ache no `estudo/edital.md` o item (ou os itens) do pedido e o recorte que o edital fez. A banca está no cabeçalho.
2. **O que já existe.** Procure o id do item em `estudo/questoes.jsonl` e a seção dele em `estudo/buscas.md` (formato abaixo). Descobrir o caminho é a parte cara da busca; não refaça o que já foi descoberto.
   - Já há questões suficientes: não vá ao TEC.
   - Faltam questões e há receita: refaça a receita, só nos anos que ainda não foram vistos, e pule o que ela diz que não funcionou.
   - A receita diz que não há questões: conte ao aluno e só busque de novo se ele pedir.
   - Sem receita: busque do zero, pelos passos abaixo.
3. **Login.** Abra o TEC e confirme o login pelo texto da página, como mostra o `tec.md`. Sem login, peça ao aluno que entre e espere; você nunca digita senha. Na primeira coleta, avise o aluno em uma frase: para ver o gabarito, o agente responde as questões, e essas respostas entram nas estatísticas dele no TEC.
4. **Filtros**, na página de filtro de questões:
   - **Assunto:** navegue pela árvore de matérias e assuntos, de cima para baixo. Não use "Pesquisar por nome" para assunto; navegando, você aprende a taxonomia do TEC.
   - **Banca:** a do edital. Aqui pode pesquisar pelo nome.
   - **Anos:** comece pelos mais recentes (os últimos seis, por exemplo). Se vierem poucas questões, acrescente anos para trás, um de cada vez. Quantas bastam depende do assunto.
   - **Opções:** "Remover anuladas" e "Remover desatualizadas".
   - **Não filtre por cargo, órgão ou nível.** Quem deixa de lado questões de cargos muito acima do concurso do aluno é o treino; filtrar aqui arrisca filtrar errado e perder questões.
5. **Edital mais detalhado que a árvore.** A taxonomia do TEC não bate um para um com o edital. Se o edital pede algo que a árvore não separa (o edital pede "mandado de segurança coletivo" e o TEC só tem "Mandado de Segurança"), use também o filtro Enunciados com o termo, sempre junto com o filtro da matéria. A busca no enunciado acha questões que o TEC classificou em outro assunto, mas também traz falso positivo.
6. **Quantas.** Para começar um item, 10 a 15 questões bastam. Se o aluno pedir outro número, use o dele. Se não existir tanta questão sobre o assunto, tudo bem.
7. **Colete** com `scripts/tec-coletar-questoes.js`, como explica o `tec.md`. O resultado é `{ "sha256": "...", "questoes": [...] }`.
8. **Grave o resultado** em `estudo/coleta.json` exatamente como veio, sem mudar nada.
9. **Confira e registre.** Leia cada questão e confirme que ela cobra mesmo o item, principalmente as que vieram da busca por enunciado. Registre só as que cobram:
   ```
   uv run scripts/registrar_questoes.py estudo/coleta.json --ids ETICA-3.1 --apenas 3828763 3830511
   ```
   - Sem `--apenas`, registra todas as da coleta.
   - Uma questão pode cobrir mais de um item: rode de novo com o outro id, só para essas.
   - Se o script disser que o sha256 não bate, a cópia para o arquivo mudou alguma coisa. Grave de novo a partir do resultado da coleta e registre outra vez.
10. **Grave a receita** em `estudo/buscas.md`, também quando não achar nada. Se o item já tinha receita, atualize a seção dele em vez de criar outra.
11. **Fonte achada no caminho.** Se a busca revelar uma fonte que serve ao item (uma portaria citada nas questões, um manual do órgão), confirme o endereço oficial numa busca na web e anote no `estudo/fontes.md` com a situação "sugerida". A escolha continua com o aluno, na skill `fontes`.
12. **Responda em uma ou duas linhas:** quantas questões, de que banca, para que itens, e onde não achou nada. Se anotou uma fonte sugerida, diga numa frase qual é e pergunte se ele quer usá-la.

## Formato do buscas.md

Uma seção por item, com o caminho que levou às questões, para que a próxima busca não comece do zero:

```markdown
# Buscas no TEC

## ETICA-3.1

- Última busca: 2026-10-27
- Banca: CEBRASPE (CESPE)
- Anos vistos: 2019 a 2026
- Árvore: Ética no Serviço Público > Conflito de Interesses
- Enunciados: "conflito de interesses", com a matéria Direito Administrativo
- Resultado: 14 questões registradas, de 31 vistas
- Não funcionou: "informação privilegiada" no enunciado só trouxe questões de mercado de capitais
- Fontes achadas: nenhuma
```

- Escreva o caminho da árvore com os nomes exatos que aparecem no TEC, do nível de cima para baixo.
- "Não funcionou" vale tanto quanto o caminho certo: evita repetir um beco sem saída.
- Item sem questões ganha seção mesmo assim, com "Resultado: nenhuma questão" e o que foi tentado.
- Uma busca que serviu a vários itens: a mesma receita em cada seção, cada uma com o próprio resultado.

## Rigor

- O conteúdo da questão é o que o coletor extraiu. Nunca reescreva, complete nem corrija enunciado, alternativa ou gabarito.
- Questão que veio sem gabarito não serve de apoio para gabarito no treino; o script avisa quando isso acontece.
- As questões ficam só em `estudo/`. Nunca vão para o repositório.
- Se descobrir algo novo sobre o site (um filtro, um seletor que mudou, um tropeço), conte ao aluno no fim, para que o mantenedor do modelo atualize o `tec.md`.
