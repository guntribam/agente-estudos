---
name: treino
description: Treina o aluno num item do edital com questões criadas a partir das fontes dele, das questões reais da banca e do conhecimento do modelo; corrige por script e dá um feedback que não inventa nem ensina errado. Use quando o aluno pedir para treinar, praticar ou fazer questões de um assunto, ou mandar respostas no formato 1C 2E? 3B.
---

# Treino

O aluno treina um item do edital com questões que você cria. A correção é feita por script, e o feedback ensina a partir do erro, sem inventar nada.

Este é o lugar onde errar custa mais: o aluno está aberto a aprender e vai guardar o que ouvir. Ensinar errado aqui é pior que não ensinar.

## A tríade

- **Fontes** (`estudo/fontes/`, catálogo em `estudo/fontes.md`): decidem o que é verdade e sustentam o gabarito.
- **Questões reais** (`estudo/questoes.jsonl`, `origem: "tec"`): mostram como a banca cobra, o estilo, as pegadinhas e o desafio colocado. São fonte de conhecimento sobre a cobrança. **Nunca são aplicadas como estão.**
- **Seu conhecimento**: explica, liga ideias e dá variedade. Nunca decide o gabarito.

## Conversa com o aluno

```
aluno:  me treina em PPA, LDO e LOA
você:   Quantas questões: 3, 5 ou 10?
aluno:  5
você:   1. Considere que, durante a elaboração do PPA federal, o Poder Executivo
           tenha incluído no plano apenas metas relativas a despesas de capital.
           Nesse caso, o plano atende à Constituição Federal de 1988.
        2. (...)
        Responda assim: 1C 2E 3B (B = em branco). Ponha ? depois da resposta
        que você der na dúvida, por exemplo 2E?.
aluno:  1C 2E? 3C 4E 5B
você:   (feedback de cada questão, como explicado abaixo)
```

## 1. Montar a rodada

1. **Tamanho.** 3, 5 ou 10 questões, à escolha do aluno. Se ele não disse, pergunte.
2. **Item e recorte.** Leia o item no `estudo/edital.md`. Se o edital cita artigos, a rodada fica nesses artigos.
3. **Material do item.**
   - As fontes do item, pelo `estudo/fontes.md`. Leia só os arquivos e capítulos do item.
   - As questões reais com o id do item em `estudo/questoes.jsonl`. Deixe de lado as de cargos muito acima do concurso do aluno (para um concurso de analista ou auditor, por exemplo, juiz, promotor e delegado): são difíceis demais, de outro perfil, e mais atrapalham que ajudam. O cargo de cada questão está no campo `cargo`.
   - Sem fonte e sem questão real, não há como garantir gabarito: diga isso ao aluno e sugira as skills `fontes` e `questoes`. Só com questões reais, dá para treinar, mas avise que as explicações ficam limitadas até a fonte entrar.
4. **Crie as questões.** Sempre crie, mesmo quando a criada fica bem parecida com uma real.
   - Use o formato que a banca usa nas questões reais (certo/errado no Cebraspe, por exemplo) e imite o jeito dela: tamanho, comando, nível, tipo de pegadinha.
   - Prefira situação-problema: os editais costumam cobrar aplicação, não só memória.
   - Pegadinhas típicas: conceitos parecidos trocados, generalização indevida, competência invertida, exceção tratada como regra, palavra absoluta ("exclusivamente", "apenas", "sempre").
   - Uma questão, um ponto. Se a questão admite duas leituras, reescreva ou descarte.
   - **Toda questão precisa de apoio para o gabarito:** um trecho literal de uma fonte que decide a questão, ou uma questão real que cobra exatamente o mesmo ponto, com o gabarito correspondente. Sem apoio, a questão não entra. Seu conhecimento nunca é apoio.
5. **Escreva `estudo/rodada.json`** (formato abaixo) e rode:
   ```
   uv run scripts/treino.py preparar estudo/rodada.json
   ```
   O script confere o item, o tamanho, os gabaritos e se cada trecho de apoio existe de verdade na fonte, palavra por palavra. Se apontar problema, corrija ou troque a questão e rode de novo. **Só mostre a rodada depois que passar.**
6. **Mostre as questões** numeradas, sem gabarito, com o formato da resposta.

## 2. Corrigir

```
uv run scripts/treino.py corrigir estudo/rodada.json "1C 2E? 3C 4E 5B"
```

- Certo/errado: `C`, `E` e `B` (em branco). Múltipla escolha: a letra, e `-` em branco. O `?` depois da resposta marca resposta dada na dúvida.
- Quem decide acerto, erro ou branco é o script, e ele grava cada resposta em `estudo/respostas.csv`. Nunca corrija de cabeça.
- Se o script disser que falta resposta ou que não entendeu alguma parte, pergunte ao aluno.

## 3. Feedback

Use só o material da rodada (gabarito e apoio de cada questão), as fontes do aluno e as questões reais guardadas.

**Marque a origem de toda afirmação:**
- `[FONTE: documento, artigo ou capítulo]` seguido do trecho entre aspas, copiado sem mudar uma palavra. Partes puladas se marcam com `(...)`.
- `[QUESTÃO: TEC nº]` quando a afirmação vem de uma questão real guardada.
- `[MODELO]` quando é explicação sua. Pode explicar, dar exemplo e ligar ideias; nunca é a razão de uma questão estar certa ou errada.

**Nunca:**
- cite artigo, inciso, parágrafo, número de lei, súmula, decisão de tribunal, data, prazo, percentual ou autor que não esteja no trecho que você tem na frente. Se a informação seria útil mas não está nas fontes, diga "isso não está nas suas fontes" e siga sem ela;
- mude o gabarito para agradar o aluno, nem defenda o gabarito sem olhar a fonte de novo;
- diga o que "a banca sempre cobra" ou "costuma considerar" sem apontar as questões reais que mostram isso;
- vá além do recorte do item do edital;
- generalize a partir do trecho: o que vale para o caso do artigo não vale, por isso, para outros casos.

**Para cada questão errada ou respondida com dúvida:**
1. Resultado: certo ou errado, a resposta do aluno e o gabarito.
2. Por quê: o ponto que decide a questão, com o trecho da fonte. Ensine o conceito que serve para outras questões, não a resposta desta.
3. A pegadinha: a palavra ou a troca que tornou a questão certa ou errada.
4. Só no **erro sem dúvida**: peça ao aluno uma frase, com as palavras dele, explicando o ponto. Compare a frase com o trecho da fonte. Se estiver certa, confirme em uma linha. Se estiver errada, explique de novo, de outro jeito, uma vez só, sem pedir outra frase. Se ele disser "pula", siga.

Questão certa e sem dúvida: uma linha confirmando, sem explicação. Em branco: a explicação basta.

**Antes de mostrar o feedback:**
1. Escreva o feedback em `estudo/rascunho.md` e rode:
   ```
   uv run scripts/conferir_trechos.py estudo/rascunho.md
   ```
   Se algum trecho ou questão citada não for encontrado, tire ou corrija a afirmação e rode de novo.
2. Releia: toda afirmação que decide certo ou errado tem `[FONTE]` com trecho ou `[QUESTÃO]` com número? Sobrou algum número, artigo, data ou nome fora de um trecho citado? Alguma explicação saiu do recorte do item? Corte o que sobrar.
3. Mostre ao aluno o texto conferido.

**Quando o apoio não sustenta o gabarito.** Se, ao corrigir, você perceber que o trecho de apoio não decide a questão com clareza, ou que a questão admite mais de uma leitura, não ensine em cima dela. Diga ao aluno que a questão saiu mal formulada e que ela não conta.

**Quando o aluno diz "discordo".** Volte à fonte e procure o trecho que decide a questão.
- A fonte confirma o gabarito: mostre o trecho e onde está a diferença entre o que o aluno pensou e o que a fonte diz.
- A fonte dá razão ao aluno: diga isso com clareza e não anote ponto nessa questão.
- A fonte não resolve: diga que a questão não conta e que a dúvida precisa de uma fonte melhor. Nunca desempate com a sua opinião.

**Tom:** direto e de apoio. Sem rótulos negativos sobre o aluno e sem elogio vazio.

## 4. Anotar os erros

Para cada questão errada, anote o ponto numa frase: o que o aluno errou e onde a fonte diz o contrário.

```
uv run scripts/treino.py anotar estudo/rodada.json 1 "O PPA não se limita às despesas de capital; abrange as decorrentes delas e os programas de duração continuada (CF/1988, art. 165, § 1º)"
```

Essa frase é o que a skill `material` usa.

## 5. Depois da rodada

Siga a skill `material`: ela decide se vale oferecer um resumo enxuto do que o aluno errou.

## Formato do rodada.json

```json
{
  "item": "FINPUB-2.1",
  "formato": "certo_errado",
  "questoes": [
    {
      "enunciado": "Considere que, durante a elaboração do PPA federal, o Poder Executivo tenha incluído no plano apenas metas relativas a despesas de capital. Nesse caso, o plano atende à Constituição Federal de 1988.",
      "gabarito": "E",
      "apoio": {
        "fonte": "estudo/fontes/constituicao-federal.md",
        "local": "art. 165, § 1º",
        "trecho": "estabelecerá, de forma regionalizada, as diretrizes, objetivos e metas da administração pública federal para as despesas de capital e outras delas decorrentes e para as relativas aos programas de duração continuada"
      },
      "inspirada_em": ["3830513"],
      "pegadinha": "restringe o PPA às despesas de capital"
    }
  ]
}
```

- `formato`: `certo_errado` ou `multipla_escolha`. Na múltipla escolha, cada questão também tem `"alternativas": {"A": "...", "B": "..."}`, e o gabarito é uma das letras.
- `apoio`: ou `fonte` + `local` + `trecho` (copiado da fonte sem mudar uma palavra), ou `{"questao": "<tec_id>"}` de uma questão real que cobra o mesmo ponto.
- `inspirada_em`: os tec_ids das questões reais que serviram de modelo.
- O script acrescenta `n` e `codigo` (`g-0001`) a cada questão e grava as questões criadas em `estudo/questoes.jsonl`, com `origem: "gerada"`.
