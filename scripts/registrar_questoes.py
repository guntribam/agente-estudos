# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Grava as questões coletadas no TEC em estudo/questoes.jsonl, uma por linha.

Recebe o resultado do coletor (scripts/tec-coletar-questoes.js) gravado num arquivo, sem
mudança nenhuma, e os ids do edital que essas questões cobrem. Antes de gravar, confere o
sha256 que o coletor calculou: se a cópia para o arquivo alterou alguma coisa, não grava.
Questão nova entra no fim do arquivo. Questão que já existe (mesmo tec_id) não se repete:
só ganha os ids novos.

Uso (a partir da pasta do projeto):
    uv run scripts/registrar_questoes.py estudo/coleta.json --ids ETICA-3.1
    uv run scripts/registrar_questoes.py estudo/coleta.json --ids ETICA-3.1 --apenas 3828763 3830511
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from comum import EDITAL, QUESTOES, gravar_jsonl, ler_edital, ler_jsonl, utf8


def sha256_canonico(questoes: list[dict]) -> str:
    """O mesmo cálculo do coletor: JSON com as chaves em ordem alfabética, sem espaços."""
    texto = json.dumps(questoes, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def main() -> None:
    utf8()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("entrada", type=Path, help="arquivo com o resultado do coletor")
    parser.add_argument("--ids", nargs="+", required=True, help="ids do edital, ex.: ETICA-3.1")
    parser.add_argument("--apenas", nargs="+", default=[], help="tec_ids que devem ser gravados")
    parser.add_argument("--destino", type=Path, default=QUESTOES)
    args = parser.parse_args()

    dados = json.loads(args.entrada.read_text(encoding="utf-8"))
    questoes = dados.get("questoes", []) if isinstance(dados, dict) else dados
    esperado = dados.get("sha256") if isinstance(dados, dict) else None
    if not esperado:
        print("Atenção: a coleta não tem sha256; não deu para conferir a cópia.")
    elif sha256_canonico(questoes) != esperado:
        sys.exit("O arquivo não bate com o resultado da coleta (sha256 diferente). "
                 "Grave de novo o resultado do coletor, sem mudar nada.")

    if EDITAL.exists():
        validos = {e["id"] for e in ler_edital(EDITAL)[0]}
        invalidos = [i for i in args.ids if i not in validos]
        if invalidos:
            sys.exit(f"Ids que não existem em {EDITAL}: {', '.join(invalidos)}")

    apenas = {t for a in args.apenas for t in a.split(",") if t}
    if apenas:
        presentes = {str(q.get("tec_id")) for q in questoes}
        faltam = sorted(apenas - presentes)
        if faltam:
            sys.exit(f"Estes tec_ids não estão na coleta: {', '.join(faltam)}")
        questoes = [q for q in questoes if str(q.get("tec_id")) in apenas]

    guardadas = ler_jsonl(args.destino)
    por_id = {str(q["tec_id"]): q for q in guardadas if q.get("tec_id")}
    novas = atualizadas = sem_gabarito = 0
    for q in questoes:
        tec_id = str(q.get("tec_id") or "")
        if not tec_id:
            print(f"Ignorada: questão sem tec_id ({(q.get('enunciado') or '')[:60]!r}).")
            continue
        if tec_id in por_id:
            existente = por_id[tec_id]
            faltam = [i for i in args.ids if i not in existente["ids"]]
            if faltam:
                existente["ids"].extend(faltam)
                atualizadas += 1
            continue
        if not q.get("gabarito") and not q.get("anulada"):
            sem_gabarito += 1
        resto = {k: v for k, v in q.items() if k not in ("tec_id", "ids", "origem")}
        nova = {"tec_id": tec_id, "ids": list(args.ids), "origem": "tec", **resto}
        guardadas.append(nova)
        por_id[tec_id] = nova
        novas += 1

    gravar_jsonl(args.destino, guardadas)
    print(f"{novas} nova(s), {len(questoes) - novas} já existia(m) ({atualizadas} com id novo). "
          f"Total no arquivo: {len(guardadas)}.")
    if sem_gabarito:
        print(f"Atenção: {sem_gabarito} questão(ões) nova(s) sem gabarito; não servem de apoio no treino.")


if __name__ == "__main__":
    main()
