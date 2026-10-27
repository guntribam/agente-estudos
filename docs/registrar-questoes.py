"""Grava questões no arquivo de questões do aluno, uma por linha (JSONL).

Recebe um arquivo JSON com a lista que o coletor do TEC devolve (docs/tec-coletar-questoes.js)
e os ids do edital que essas questões cobrem. Questão nova entra no fim do arquivo. Questão que
já existe (mesmo tec_id) não se repete: só ganha os ids novos.

Uso:
    uv run docs/registrar-questoes.py coletadas.json --ids FINPUB-2.1

Vai para a skill `questoes` quando ela for criada.
"""

import argparse
import json
import sys
from pathlib import Path


def ler(destino: Path) -> list[dict]:
    if not destino.exists():
        return []
    with destino.open(encoding="utf-8") as f:
        return [json.loads(linha) for linha in f if linha.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("entrada", type=Path, help="JSON com a lista de questões coletadas")
    parser.add_argument("--ids", nargs="+", required=True, help="ids do edital, ex.: FINPUB-2.1")
    parser.add_argument("--origem", default="tec", choices=["tec", "gerada"])
    parser.add_argument("--destino", type=Path, default=Path("estudo/questoes.jsonl"))
    args = parser.parse_args()
    # No Windows o console não usa UTF-8 por padrão e estraga os acentos das mensagens.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    coletadas = json.loads(args.entrada.read_text(encoding="utf-8"))
    questoes = ler(args.destino)
    por_id = {q["tec_id"]: q for q in questoes if q.get("tec_id")}

    novas = atualizadas = sem_gabarito = 0
    for q in coletadas:
        tec_id = q.get("tec_id")
        if not tec_id:
            print(f"Ignorada: questão sem tec_id ({(q.get('enunciado') or '')[:60]!r})", file=sys.stderr)
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
        nova = {"tec_id": tec_id, "ids": list(args.ids), "origem": args.origem, **resto}
        questoes.append(nova)
        por_id[tec_id] = nova
        novas += 1

    args.destino.parent.mkdir(parents=True, exist_ok=True)
    with args.destino.open("w", encoding="utf-8", newline="\n") as f:
        for q in questoes:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")

    repetidas = len(coletadas) - novas
    print(f"{novas} nova(s), {repetidas} já existia(m) ({atualizadas} com id novo). Total: {len(questoes)}.")
    if sem_gabarito:
        print(f"Atenção: {sem_gabarito} questão(ões) nova(s) sem gabarito.")


if __name__ == "__main__":
    main()
