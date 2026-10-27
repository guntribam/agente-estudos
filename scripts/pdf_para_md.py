# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf", "pymupdf4llm"]
# ///
"""Converte um PDF em markdown: um arquivo só ou um arquivo por capítulo.

Uso (a partir da pasta do projeto):
    uv run scripts/pdf_para_md.py estudo/edital.pdf estudo/edital-texto.md
    uv run scripts/pdf_para_md.py livro.pdf estudo/fontes/nome-do-livro --capitulos

Com --capitulos, a saída é uma pasta, e os capítulos são os de primeiro nível do sumário
interno do PDF (os marcadores). O que vem antes do primeiro capítulo vai para 00-inicio.md.
Sem sumário interno, gera um arquivo só e avisa.

Sai com código 2 quando o PDF quase não tem texto (provavelmente escaneado). Nesse caso a
conversão não serve: leia o próprio PDF.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf
import pymupdf4llm

from comum import utf8

MIN_CARACTERES_POR_PAGINA = 200


def slug(titulo: str) -> str:
    ascii_ = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_.lower()).strip("-")[:60] or "capitulo"


def main() -> None:
    utf8()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("entrada", type=Path)
    parser.add_argument("saida", type=Path)
    parser.add_argument("--capitulos", action="store_true", help="um arquivo por capítulo")
    args = parser.parse_args()

    doc = pymupdf.open(args.entrada)
    caracteres = sum(len(pagina.get_text().strip()) for pagina in doc)
    if doc.page_count and caracteres / doc.page_count < MIN_CARACTERES_POR_PAGINA:
        print(f"O PDF quase não tem texto ({caracteres} caracteres em {doc.page_count} páginas). "
              "Provavelmente é escaneado; a conversão não serve.")
        sys.exit(2)

    if not args.capitulos:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(pymupdf4llm.to_markdown(doc), encoding="utf-8")
        print(f"{doc.page_count} páginas convertidas em {args.saida}.")
        return

    args.saida.mkdir(parents=True, exist_ok=True)
    capitulos = [(titulo, pagina - 1) for nivel, titulo, pagina in doc.get_toc() if nivel == 1 and pagina > 0]
    if not capitulos:
        destino = args.saida / "livro.md"
        destino.write_text(pymupdf4llm.to_markdown(doc), encoding="utf-8")
        print(f"O PDF não tem sumário interno. Gerei um arquivo só: {destino} ({doc.page_count} páginas).")
        return

    partes = []
    if capitulos[0][1] > 0:
        partes.append(("Início", 0, capitulos[0][1]))
    for i, (titulo, inicio) in enumerate(capitulos):
        fim = capitulos[i + 1][1] if i + 1 < len(capitulos) else doc.page_count
        partes.append((titulo, inicio, max(fim, inicio + 1)))

    for k, (titulo, inicio, fim) in enumerate(partes):
        paginas = list(range(inicio, min(fim, doc.page_count)))
        destino = args.saida / f"{k:02d}-{slug(titulo)}.md"
        destino.write_text(f"# {titulo}\n\n{pymupdf4llm.to_markdown(doc, pages=paginas)}", encoding="utf-8")
        print(f"{destino.name}: páginas {inicio + 1} a {fim}")


if __name__ == "__main__":
    main()
