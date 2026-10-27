# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf"]
# ///
"""Confere o edital.md contra o PDF do edital.

Verifica se cada item do edital.md está no PDF com o mesmo texto (sem contar espaços,
quebras de linha, hífens e maiúsculas), se o nome de cada matéria está no PDF, se as siglas
não se repetem e se a numeração segue 1, 2, 3... em cada nível, sem pular nem repetir.

Uso (a partir da pasta do projeto):
    uv run scripts/conferir_edital.py estudo/edital.pdf estudo/edital.md

Sai com código 1 se encontrar algum problema.
"""

import sys
from collections import defaultdict
from pathlib import Path

import pymupdf

from comum import QUEBRA_DE_PAGINA, ler_edital, normalizar, utf8

# Quanto texto (cabeçalho, rodapé, número de página) se aceita pular numa quebra de página.
PULO_MAXIMO = 300


def _casa_com_quebra(alvo: str, item: str, i: int) -> bool:
    """Casa o item a partir da posição i, pulando texto só onde há quebra de página."""
    j = 0
    while j < len(item):
        if i < len(alvo) and alvo[i] == item[j]:
            i += 1
            j += 1
            continue
        quebra = alvo.find(QUEBRA_DE_PAGINA, i, i + PULO_MAXIMO)
        if quebra < 0:
            return False
        resto = item[j:j + 20]
        k = alvo.find(resto, quebra, quebra + PULO_MAXIMO + len(resto))
        if k < 0:
            return False
        i = k
    return True


def encontra(alvo: str, item: str) -> bool:
    if item in alvo:
        return True
    ancora = item[:20]
    pos = alvo.find(ancora)
    while pos >= 0:
        if _casa_com_quebra(alvo, item, pos):
            return True
        pos = alvo.find(ancora, pos + 1)
    return False


def main() -> None:
    utf8()
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    pdf, md = Path(sys.argv[1]), Path(sys.argv[2])
    doc = pymupdf.open(pdf)
    alvo = normalizar(QUEBRA_DE_PAGINA.join(pagina.get_text() for pagina in doc))
    entradas, problemas = ler_edital(md)
    if not entradas:
        problemas.append("Nenhum item no edital.md (formato: '### Matéria [SIGLA]' e '- 1.1 texto').")

    nomes = defaultdict(set)
    for e in entradas:
        nomes[e["sigla"]].add(e["materia"])
    for sigla, materias in nomes.items():
        if len(materias) > 1:
            problemas.append(f"A sigla {sigla} foi usada em mais de uma matéria: {', '.join(sorted(materias))}.")
    for materia in sorted({e["materia"] for e in entradas}):
        if not encontra(alvo, normalizar(materia)):
            problemas.append(f"Nome da matéria não encontrado no PDF: {materia}")

    for e in entradas:
        if not encontra(alvo, normalizar(e["texto"])):
            problemas.append(f'{e["id"]} (linha {e["linha"]}): texto não encontrado no PDF: "{e["texto"][:80]}"')

    numeros = defaultdict(list)
    for e in entradas:
        numeros[e["sigla"]].append(tuple(int(x) for x in e["numero"].split(".")))
    for sigla, lista in numeros.items():
        vistos, filhos = set(), defaultdict(list)
        for n in lista:
            if n in vistos:
                problemas.append(f"{sigla}-{'.'.join(map(str, n))} aparece duas vezes.")
            vistos.add(n)
            filhos[n[:-1]].append(n[-1])
        for pai, ordem in filhos.items():
            nome_pai = f"{sigla}-{'.'.join(map(str, pai))}"
            onde = f"dentro de {nome_pai}" if pai else f"no primeiro nível de {sigla}"
            if ordem != list(range(1, len(ordem) + 1)):
                problemas.append(f"Numeração {onde}: {ordem}; o esperado é 1 a {len(ordem)}, em ordem e sem pular.")
            if pai and pai not in vistos:
                problemas.append(f"{nome_pai} tem subitens, mas não aparece no edital.md.")

    if problemas:
        print("Problemas:")
        for p in problemas:
            print(f"- {p}")
        sys.exit(1)
    print(f"{len(nomes)} matéria(s) e {len(entradas)} item(ns) conferidos com o PDF. Tudo confere.")


if __name__ == "__main__":
    main()
