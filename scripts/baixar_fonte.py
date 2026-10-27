# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Baixa uma página oficial (lei, norma, documentação) e grava o texto em markdown.

O texto riscado da página (nas leis compiladas do Planalto, é o texto revogado) fica de fora.
O arquivo começa com o endereço e a data em que foi baixado. Se o endereço for de um PDF,
o PDF é salvo ao lado, com a extensão .pdf, para ser convertido com pdf_para_md.py.

Uso (a partir da pasta do projeto):
    uv run scripts/baixar_fonte.py https://www.planalto.gov.br/ccivil_03/... estudo/fontes/lei-x.md
"""

import re
import sys
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

from comum import utf8

AGENTE = "Mozilla/5.0 (agente-estudos DevEstavel)"


class _Texto(HTMLParser):
    BLOCOS = {"p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "table",
              "section", "article", "blockquote", "pre", "dd", "dt", "center", "hr"}
    PULAR = {"script", "style", "head", "title", "noscript"}
    RISCADO = {"strike", "s", "del"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self.pular = 0
        self.riscado = 0
        self.spans: list[bool] = []
        self.trechos_riscados = 0

    def _riscando(self) -> bool:
        return self.riscado > 0 or any(self.spans)

    def handle_starttag(self, tag, attrs):
        if tag in self.PULAR:
            self.pular += 1
        elif tag in self.RISCADO:
            self.riscado += 1
            self.trechos_riscados += 1
        elif tag == "span":
            estilo = (dict(attrs).get("style") or "").replace(" ", "").lower()
            linha = "line-through" in estilo
            self.spans.append(linha)
            self.trechos_riscados += linha
        if tag in self.BLOCOS:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in self.PULAR:
            self.pular = max(0, self.pular - 1)
        elif tag in self.RISCADO:
            self.riscado = max(0, self.riscado - 1)
        elif tag == "span" and self.spans:
            self.spans.pop()
        if tag in self.BLOCOS:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self.pular and not self._riscando():
            self.partes.append(data)

    def texto(self) -> str:
        linhas = (" ".join(linha.split()) for linha in "".join(self.partes).splitlines())
        return re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()


def _decodificar(corpo: bytes, charset: str | None) -> str:
    if not charset:
        m = re.search(rb'charset=["\']?([\w-]+)', corpo[:4096], re.IGNORECASE)
        charset = m.group(1).decode() if m else None
    for tentativa in (charset, "utf-8", "cp1252"):
        if not tentativa:
            continue
        try:
            return corpo.decode(tentativa)
        except (LookupError, UnicodeDecodeError):
            continue
    return corpo.decode("utf-8", errors="replace")


def main() -> None:
    utf8()
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    url, destino = sys.argv[1], Path(sys.argv[2])
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=60) as resposta:
        corpo = resposta.read()
        tipo = resposta.headers.get_content_type()
        charset = resposta.headers.get_content_charset()

    destino.parent.mkdir(parents=True, exist_ok=True)
    if tipo == "application/pdf" or corpo[:5] == b"%PDF-":
        pdf = destino.with_suffix(".pdf")
        pdf.write_bytes(corpo)
        print(f"É um PDF. Salvo em {pdf}. Converta com: uv run scripts/pdf_para_md.py {pdf} {destino}")
        return

    leitor = _Texto()
    leitor.feed(_decodificar(corpo, charset))
    texto = leitor.texto()
    destino.write_text(f"Fonte: {url}\nBaixada em: {date.today().isoformat()}\n\n{texto}\n", encoding="utf-8")
    print(f"{len(texto)} caracteres gravados em {destino}. Trechos riscados (revogados) deixados de fora: "
          f"{leitor.trechos_riscados}.")


if __name__ == "__main__":
    main()
