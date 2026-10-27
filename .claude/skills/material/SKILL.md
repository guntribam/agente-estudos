---
name: material
description: Depois de uma rodada de treino, avalia se vale um material enxuto sobre os pontos que o aluno errou, oferece em uma linha e, se ele quiser, escreve no chat, apoiado só nas fontes e nas questões reais. Use ao fim de uma rodada da skill treino ou quando o aluno pedir resumo, revisão ou material curto de um assunto.
---

# Material

Um material enxuto, escrito no chat, sobre o que o aluno errou. Nasce do erro real, não do resumo de um capítulo. Segue o mesmo rigor do feedback do treino: nada inventado.

## Quando oferecer

Depois da correção de uma rodada, olhe o resultado (o resumo que o `treino.py corrigir` imprime e as linhas do item em `estudo/respostas.csv`):

- **Vale a pena** quando houve erro sem dúvida, quando vários erros caíram no mesmo ponto, ou quando metade ou mais dos acertos foram na dúvida. Nesses casos, o conceito não está firme.
- **Não vale** quando a rodada saiu limpa ou quando o erro foi isolado e o feedback já resolveu. Aí diga em uma linha que não precisa de material, e siga.
- Quando vale, **ofereça em uma linha** e só escreva se o aluno quiser:
  ```
  Você errou duas vezes o que entra no PPA. Quer um resumo curto desse ponto?
  ```
- O aluno também pode pedir a qualquer momento ("me faz um resumo de PPA"). Nesse caso, parta dos erros anotados do item (coluna `ponto` em `estudo/respostas.csv`). Se não houver erro anotado, parta dos pontos que as questões reais do item mais cobram.

## Como é

- **No chat.** Nada de arquivo ou PDF, a não ser que o aluno peça. Se ele pedir um arquivo, salve em `estudo/materiais/<id-do-item>.md`. Se pedir PDF e você não tiver como gerar, diga isso.
- **Pelos conceitos que falharam**, não questão por questão. Cabe numa tela.
- **Cada conceito tem três partes:**
  1. O que a fonte diz: `[FONTE: documento, artigo ou capítulo] "trecho literal"`.
  2. Como a banca cobra: a pegadinha, com o número das questões reais que mostram isso (`[QUESTÃO: TEC nº]`). Sem questão real que mostre, não escreva essa parte.
  3. Como não cair: uma ou duas linhas suas, marcadas com `[MODELO]`, que explicam sem acrescentar nenhum fato novo.

Exemplo:

```
PPA: o que entra no plano

[FONTE: CF/1988, art. 165, § 1º] "A lei que instituir o plano plurianual
estabelecerá, de forma regionalizada, as diretrizes, objetivos e metas da
administração pública federal para as despesas de capital e outras delas
decorrentes e para as relativas aos programas de duração continuada."

Como a banca cobra: restringe o PPA a um só tipo de despesa
("exclusivamente às despesas de capital") [QUESTÃO: TEC 3830513].

Como não cair: são três coisas, não uma. Desconfie de "exclusivamente"
e "apenas" perto de PPA. [MODELO]
```

## Rigor

- Use só as fontes do aluno e as questões reais guardadas. Não cite artigo, número, data, prazo, súmula, decisão ou autor fora de um trecho citado.
- Não saia do recorte do item do edital.
- "A banca cobra assim" só com o número das questões reais que mostram isso.
- Antes de mostrar, escreva o material em `estudo/rascunho.md` e rode:
  ```
  uv run scripts/conferir_trechos.py estudo/rascunho.md
  ```
  Se algum trecho ou questão citada não for encontrado, tire ou corrija a afirmação e rode de novo. Só mostre o texto conferido.
