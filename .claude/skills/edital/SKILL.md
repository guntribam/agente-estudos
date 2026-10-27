---
name: edital
description: Monta o conteúdo programático do cargo do aluno a partir do PDF do edital, na hierarquia do edital, com o texto literal e um id por item. Use quando o aluno trouxer o edital, pedir para montar ou organizar o edital, ou quando ainda não existir estudo/edital.md.
---

# Edital

Transforma o PDF do edital em `estudo/edital.md`: o conteúdo programático do cargo do aluno, organizado como o edital organiza e com o texto copiado sem resumir. Todas as outras skills partem desse arquivo, e os ids dos itens ligam tudo: fontes, questões, respostas.

## Conversa com o aluno

```
aluno:  monta o meu edital (o PDF está na pasta)
você:   Achei 4 cargos no edital: Auditoria, TI Ciência de Dados, TI Infraestrutura
        e TI Desenvolvimento de Sistemas. Qual é o seu?
aluno:  desenvolvimento
você:   Pronto. Seu edital tem 13 matérias em 3 blocos.
```

São duas falas do aluno. O resto é com você, sem mostrar ids nem arquivos.

## Passo a passo

1. **Ache o PDF.** Se o aluno não disse onde está, procure PDFs na pasta do projeto, fora de `old/`. Se houver mais de um, ou nenhum, pergunte. Copie o PDF para `estudo/edital.pdf`.
   - Se vierem vários PDFs (edital, anexos, retificação), use o que traz o conteúdo programático.
   - Retificação ainda não é tratada por esta skill. Se o aluno trouxer uma, diga isso e pergunte qual PDF usar.
2. **Converta para texto:**
   ```
   uv run scripts/pdf_para_md.py estudo/edital.pdf estudo/edital-texto.md
   ```
   Se o script sair com código 2, o PDF é escaneado e não tem texto. Diga ao aluno, em uma frase, que esse PDF é imagem das páginas e que você precisa da versão com texto (a do site da banca costuma ter). Pare aí: sem texto não dá para garantir que o conteúdo é literal.
3. **Ache o conteúdo programático e os cargos.** O conteúdo costuma ficar perto do fim, com títulos como "Conteúdos programáticos", "Objetos de avaliação" ou "Conhecimentos". Pergunte o cargo do aluno mostrando os cargos que achou.
4. **Escreva `estudo/edital.md`** no formato abaixo, com os blocos comuns a todos os cargos e os blocos do cargo do aluno.
5. **Confira:**
   ```
   uv run scripts/conferir_edital.py estudo/edital.pdf estudo/edital.md
   ```
   - "Texto não encontrado": o item ficou diferente do PDF. Copie de novo do `estudo/edital-texto.md` e rode outra vez.
   - "Numeração": confira no PDF. Se foi engano seu, corrija. Se o próprio edital pula ou repete um número, mantenha como está e conte ao aluno.
   - Só diga ao aluno que terminou quando a conferência passar, ou quando o único aviso restante for uma numeração que o próprio edital tem.
6. **Responda em uma ou duas linhas:** quantas matérias, em quantos blocos.

## Formato do edital.md

```markdown
# Edital CGU 2026

- Órgão: Controladoria-Geral da União (CGU)
- Banca: CEBRASPE
- Cargo: Auditor Federal de Finanças e Controle, TI, Desenvolvimento de Sistemas
- Arquivo: estudo/edital.pdf

## Conhecimentos básicos

### Ética Pública e Responsabilidade Profissional [ETICA]

- 1 Fundamentos da ética pública.
  - 1.1 Interesse público, dignidade, justiça e responsabilidade; relações entre deveres, consequências e virtudes profissionais; conflitos entre valores em decisões públicas.
- 2 Deveres profissionais.
  - 2.1 Imparcialidade, probidade, diligência e respeito; autonomia técnica e responsabilidade; limites da obediência hierárquica; uso adequado de informação e recursos públicos.
  - 2.2 Aplicação dos valores e deveres de conduta ética da CGU a situações de trabalho.
- 3 Conflitos de interesses e imparcialidade.
  - 3.1 Identificação de interesses privados em conflito com a função pública e medidas de prevenção, consulta e encaminhamento, nos termos dos arts. 3º a 5º, 8º e 10 da Lei nº 12.813/2013.
```

Regras:

- **Texto literal.** Copie cada item como está no edital: sem resumir, sem corrigir, sem trocar palavras, sem juntar nem separar itens. Pode tirar só a quebra de linha e o hífen de fim de linha que vêm do PDF.
- **Hierarquia.** `##` para o bloco (com o nome que o edital usa: conhecimentos básicos, específicos...), `###` para a matéria, e uma lista com recuo para os itens numerados, um nível de recuo por nível de numeração (`1`, `1.1`, `1.1.1`).
- **Sigla.** Cada matéria ganha uma sigla curta, em maiúsculas, sem acento e única no edital (ETICA, ESTADO, ENGSOFT). Ela aparece só no título da matéria, entre colchetes.
- **Id do item.** É a sigla mais o número do edital: `ETICA-3.1`. Não subdivida itens que juntam vários assuntos; o número do edital é o id.
- **Matéria sem numeração no edital.** Numere os assuntos na ordem em que aparecem, separando-os como o próprio edital separa, e acrescente `(numeração criada pelo agente)` no fim do título da matéria, depois da sigla. Conte isso ao aluno.
- **Cabeçalho.** Órgão, banca, cargo e arquivo de origem, como no exemplo. A banca é usada pela skill `questoes`.

## Fica para depois

Esta skill ainda não trata as regras do edital que mudam o estudo (corte de legislação e de jurisprudência, penalidade por erro, número de itens e pesos) nem retificações.
