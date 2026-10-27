"""Funções usadas por mais de um script do modelo."""

import json
import re
import sys
import unicodedata
from pathlib import Path

ESTUDO = Path("estudo")
EDITAL = ESTUDO / "edital.md"
FONTES = ESTUDO / "fontes"
QUESTOES = ESTUDO / "questoes.jsonl"
RESPOSTAS = ESTUDO / "respostas.csv"

# Marca a divisa entre páginas no texto extraído de um PDF.
QUEBRA_DE_PAGINA = "\x00"

_ASPAS = str.maketrans({
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "‘": "'", "’": "'",
})
# Na comparação de textos não contam espaços, quebras de linha, hífens e marcação de markdown.
_IGNORAR = re.compile(r"[\s\-­‐‑*_#>|`]+")

_MATERIA = re.compile(r"^###\s+(.+?)\s+\[([A-Z0-9]+)\]")
_ENTRADA = re.compile(r"^\s*[-*]\s+(\d+(?:\.\d+)*)\.?\s+(.+?)\s*$")


def utf8() -> None:
    """No Windows o console não usa UTF-8 por padrão e estraga os acentos das mensagens."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def aspas_retas(texto: str) -> str:
    return unicodedata.normalize("NFC", texto).translate(_ASPAS)


def normalizar(texto: str) -> str:
    return _IGNORAR.sub("", aspas_retas(texto).casefold())


def ler_jsonl(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    with caminho.open(encoding="utf-8") as f:
        return [json.loads(linha) for linha in f if linha.strip()]


def gravar_jsonl(caminho: Path, linhas: list[dict]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="\n") as f:
        for linha in linhas:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def ler_edital(caminho: Path = EDITAL) -> tuple[list[dict], list[str]]:
    """Lê o edital.md. Devolve as entradas numeradas e os problemas de formato encontrados.

    Cada entrada tem: sigla, materia, numero, id (sigla-numero), texto e linha.
    """
    entradas, problemas = [], []
    materia = sigla = None
    for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
        if m := _MATERIA.match(linha):
            materia, sigla = m.group(1), m.group(2)
        elif m := _ENTRADA.match(linha):
            if not sigla:
                problemas.append(f"Linha {n}: item fora de uma matéria (falta o título '### Matéria [SIGLA]').")
                continue
            entradas.append({
                "sigla": sigla,
                "materia": materia,
                "numero": m.group(1),
                "id": f"{sigla}-{m.group(1)}",
                "texto": m.group(2),
                "linha": n,
            })
    return entradas, problemas
