---
name: fontes
description: Ajuda o aluno a escolher, negociar e obter as fontes de estudo de cada assunto do edital (leis, normas, documentação oficial, livros), monta com ele o catálogo de fontes e converte tudo para .md. Use quando o aluno pedir material, fontes, bibliografia ou livros para uma matéria ou um assunto, ou quando trouxer um PDF de livro ou apostila.
---

# Fontes

No treino, a fonte decide o que é verdade e sustenta o gabarito. Esta skill garante que cada assunto do edital tenha uma fonte confiável, combinada com o aluno e legível por você. Ela tem três momentos: conversar, negociar e obter.

Pré-requisito: `estudo/edital.md`. Se não existir, comece pela skill `edital`.

## 1. Conversar

O aluno pede material para uma matéria inteira ou para alguns assuntos, às vezes colando o texto do edital.

- Ache os itens correspondentes no `estudo/edital.md`. O edital é a fonte da verdade: não questione se um assunto deve ser estudado.
- Agrupe os itens por afinidade, dentro de uma mesma categoria didática. Exemplo: Java e PHP são linguagens de programação; OpenSSL e OWASP são segurança.
- Onde o edital já cita a fonte (lei, artigos, manual), não há o que escolher: a fonte é essa. Só conte ao aluno.
- Para cada grupo em que há escolha, pergunte como ele quer pesquisar. Exemplo: um material para cada assunto, ou uma base comum que cubra o grupo e depois o específico de cada um.

```
aluno:  preciso de material de Ética
você:   Separei Ética em três grupos.
        Lei citada pelo próprio edital (3.1 e 3.2): Lei 12.813/2013 e arts. 18 a 21
        da Lei 9.784/1999. Aqui não tem o que escolher, a fonte é a lei.
        Código de conduta da CGU (2.2): vou atrás da versão oficial.
        Conceitos de ética pública (1.1, 2.1, 4.1, 4.2 e 5.1): não têm lei por trás.
        Prefere um livro que cubra tudo ou material oficial, como guias de órgãos públicos?
```

## 2. Negociar

- Para cada grupo com escolha, busque na web e mostre duas ou três opções, cada uma com o link e o motivo de ser uma referência conhecida.
- **Só sugira o que encontrou na busca.** Livro, edição, autor ou link que você não viu na busca não entra. Se não houver ferramenta de busca na web, sugira apenas as fontes que o próprio edital cita e diga ao aluno que não consegue pesquisar outras.
- Ordem de preferência:
  1. a fonte que o edital cita;
  2. texto oficial: lei no Planalto, norma do órgão, Diário Oficial;
  3. documentação ou especificação oficial: RFC, OWASP, NIST, documentação oficial da linguagem ou do framework;
  4. livro consagrado, com várias edições e adotado em cursos de graduação.
  Nada obscuro ou pouco conhecido.
- O aluno aceita, recusa ou traz a dele ("já tenho o livro X"). Quando ele traz um livro, olhe o sumário e diga quais itens o livro cobre e quais ficam de fora.
- O combinado entra em `estudo/fontes.md` (formato abaixo). O catálogo é montado com o aluno, nessa conversa.

## 3. Obter

Toda fonte vira `.md` em `estudo/fontes/`. O aluno não vê nada disso; ele só ouve algo como "preparei o livro; os capítulos 3 e 5 cobrem conflito de interesses".

**Lei, norma e página oficial.** Baixe você mesmo, só de site oficial (planalto.gov.br, in.gov.br, gov.br, camara.leg.br, senado.leg.br, o site do órgão, a documentação oficial):

```
uv run scripts/baixar_fonte.py URL estudo/fontes/lei-12813-2013.md
```

O script deixa de fora o texto riscado (nas leis compiladas do Planalto, é o texto revogado) e anota no arquivo o endereço e a data em que baixou. Se a URL for de um PDF, ele salva o PDF ao lado; converta com o comando de livro abaixo, sem `--capitulos`.

**Livro e apostila.** Só cópia legítima, que o próprio aluno coloca na pasta. Converta um capítulo por arquivo:

```
uv run scripts/pdf_para_md.py caminho/do/livro.pdf estudo/fontes/nome-do-livro --capitulos
```

- O script usa o sumário interno do PDF. Sem sumário interno, gera um arquivo só; nesse caso, use o sumário impresso do livro para saber onde está cada assunto.
- Se o script sair com código 2, o PDF é escaneado e não há OCR. Use o próprio PDF quando precisar dele, mesmo gastando mais, e diga ao aluno em uma frase que a leitura desse livro vai ser mais lenta.

**Mapeie pelo sumário** que capítulos cobrem cada item do edital e anote no `fontes.md`. O treino lê só os capítulos do item; carregar o livro inteiro piora as respostas.

Depois de obter, marque a fonte como "obtida" no `fontes.md`.

## Formato do fontes.md

```markdown
# Fontes

| Itens | Fonte | Onde está | Situação |
|---|---|---|---|
| ETICA-3.1 | Lei nº 12.813/2013, arts. 3º a 5º, 8º e 10 (citada no edital) | estudo/fontes/lei-12813-2013.md (Planalto, baixada em 2026-10-27) | obtida |
| ETICA-1.1, ETICA-2.1 | Livro escolhido pelo aluno, com autor e edição | estudo/fontes/nome-do-livro/03-....md e 05-....md | obtida |
| ETICA-2.2 | Código de conduta da CGU | link oficial encontrado na busca | combinada |
```

Situação: "combinada" (o aluno escolheu, falta obter) ou "obtida" (o `.md` existe).

## Rigor

- Nunca afirme que uma fonte existe, que tem tal edição ou que cobre tal assunto sem ter visto isso na busca ou no sumário.
- O texto em `estudo/fontes/` é a base dos gabaritos do treino. Não edite, não resuma e não corrija esse texto.
- A versão compilada do Planalto é a de hoje. Se o aluno ou o edital indicarem que a cobrança é de outra versão, avise que o arquivo baixado é a versão atual.
