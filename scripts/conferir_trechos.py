# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Confere se o que um texto cita como fonte existe de verdade nas fontes do aluno.

Todo trecho entre aspas logo depois de uma marca [FONTE: ...] precisa estar, palavra por
palavra, em algum arquivo .md de estudo/fontes/. Não contam diferenças de espaço, quebra de
linha, hífen, maiúsculas e marcação de markdown. Partes puladas se marcam com (...).
Toda marca [QUESTÃO: TEC nº] precisa apontar para uma questão de estudo/questoes.jsonl.

Uso (a partir da pasta do projeto):
    uv run scripts/conferir_trechos.py estudo/rascunho.md

Sai com código 1 se alguma citação não for encontrada.
"""

import re
import sys
from pathlib import Path

from comum import FONTES, QUESTOES, aspas_retas, ler_jsonl, normalizar, utf8

_OMISSAO = re.compile(r"\((?:\.\.\.|…)\)|\[(?:\.\.\.|…)\]")
_FONTE = re.compile(r'\[FONTE:([^\]]*)\]\s*(?:"([^"]+)")?')
_QUESTAO = re.compile(r"\[QUEST[ÃA]O:\s*TEC\s*(?:n[º°o.]\s*)?(\d+)\s*\]", re.IGNORECASE)

_cache: dict[Path, str] = {}


def _texto(arquivo: Path) -> str:
    if arquivo not in _cache:
        _cache[arquivo] = normalizar(arquivo.read_text(encoding="utf-8", errors="replace"))
    return _cache[arquivo]


def _pedacos(trecho: str) -> list[str]:
    pedacos = (normalizar(p).strip(".,;:…") for p in _OMISSAO.split(trecho))
    return [p for p in pedacos if p]


def onde_esta(trecho: str, arquivo: Path | str | None = None) -> Path | None:
    """Devolve o arquivo de fonte que contém o trecho (na ordem, se houver omissões), ou None."""
    pedacos = _pedacos(trecho)
    if not pedacos:
        return None
    arquivos = [Path(arquivo)] if arquivo else sorted(FONTES.rglob("*.md"))
    for a in arquivos:
        if not a.is_file():
            continue
        alvo, pos = _texto(a), 0
        for p in pedacos:
            i = alvo.find(p, pos)
            if i < 0:
                break
            pos = i + len(p)
        else:
            return a
    return None


def conferir_texto(texto: str) -> tuple[int, list[str]]:
    """Devolve quantas citações foram conferidas e a lista de problemas."""
    texto = aspas_retas(texto)
    conferidas, problemas = 0, []
    for m in _FONTE.finditer(texto):
        rotulo, trecho = m.group(1).strip(), m.group(2)
        if not trecho:
            problemas.append(f'[FONTE: {rotulo}] sem trecho entre aspas logo depois.')
            continue
        conferidas += 1
        if not onde_esta(trecho):
            problemas.append(f'Trecho não encontrado nas fontes ({rotulo}): "{trecho[:90]}"')
    tec_ids = {str(q.get("tec_id")) for q in ler_jsonl(QUESTOES) if q.get("tec_id")}
    for m in _QUESTAO.finditer(texto):
        conferidas += 1
        if m.group(1) not in tec_ids:
            problemas.append(f"[QUESTÃO: TEC {m.group(1)}] não está em {QUESTOES}.")
    return conferidas, problemas


def main() -> None:
    utf8()
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    conferidas, problemas = conferir_texto(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if problemas:
        print("Problemas:")
        for p in problemas:
            print(f"- {p}")
        sys.exit(1)
    if conferidas:
        print(f"{conferidas} citação(ões) conferida(s). Tudo encontrado.")
    else:
        print("Nenhuma citação [FONTE] ou [QUESTÃO] no texto.")


if __name__ == "__main__":
    main()
