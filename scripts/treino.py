# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Rodadas de treino: confere as questões criadas, corrige as respostas e anota os erros.

Uso (a partir da pasta do projeto):
    uv run scripts/treino.py preparar estudo/rodada.json
    uv run scripts/treino.py corrigir estudo/rodada.json "1C 2E? 3B"
    uv run scripts/treino.py anotar estudo/rodada.json 1 "o que o aluno errou e onde a fonte diz o contrário"

preparar  Confere a rodada (item do edital, tamanho, gabaritos e apoio de cada questão) e, se
          estiver tudo certo, dá um código a cada questão e guarda as questões em
          estudo/questoes.jsonl. Se houver problema, não grava nada.
corrigir  Compara as respostas com os gabaritos e grava uma linha por questão em
          estudo/respostas.csv. Quem decide acerto, erro ou branco é este script.
anotar    Escreve, na linha de uma questão errada, a frase com o ponto que o aluno errou.

Respostas: certo/errado usa C, E e B (em branco); múltipla escolha usa a letra e - (em
branco). Um ? depois da resposta marca resposta dada na dúvida.
"""

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from comum import EDITAL, QUESTOES, RESPOSTAS, gravar_jsonl, ler_edital, ler_jsonl, utf8
from conferir_trechos import onde_esta

TAMANHOS = (3, 5, 10)
FORMATOS = ("certo_errado", "multipla_escolha")
CAMPOS = ["data", "item", "questao", "resposta", "gabarito", "resultado", "duvida", "ponto"]


def _ler_rodada(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


def _gravar_rodada(caminho: Path, rodada: dict) -> None:
    caminho.write_text(json.dumps(rodada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _parar(mensagens: list[str] | str) -> None:
    if isinstance(mensagens, str):
        mensagens = [mensagens]
    print("Problemas:" if len(mensagens) > 1 else "Problema:")
    for m in mensagens:
        print(f"- {m}")
    sys.exit(1)


def preparar(caminho: Path) -> None:
    rodada = _ler_rodada(caminho)
    questoes = rodada.get("questoes") or []
    if any("codigo" in q for q in questoes):
        _parar("Esta rodada já foi preparada. Para uma rodada nova, escreva um rodada.json novo.")

    problemas = []
    item, formato = rodada.get("item"), rodada.get("formato")
    if not EDITAL.exists():
        problemas.append(f"Não existe {EDITAL}. Monte o edital antes de treinar.")
    elif item not in {e["id"] for e in ler_edital(EDITAL)[0]}:
        problemas.append(f"O item {item!r} não existe em {EDITAL}.")
    if formato not in FORMATOS:
        problemas.append(f"Formato {formato!r} inválido; use certo_errado ou multipla_escolha.")
    if len(questoes) not in TAMANHOS:
        problemas.append(f"A rodada tem {len(questoes)} questão(ões); precisa ter 3, 5 ou 10.")

    reais = {str(q["tec_id"]): q for q in ler_jsonl(QUESTOES) if q.get("tec_id")}
    for n, q in enumerate(questoes, 1):
        p = f"Questão {n}:"
        if not (q.get("enunciado") or "").strip():
            problemas.append(f"{p} sem enunciado.")
        gabarito = q.get("gabarito")
        if formato == "certo_errado" and gabarito not in ("C", "E"):
            problemas.append(f"{p} gabarito {gabarito!r}; em certo/errado tem de ser C ou E.")
        if formato == "multipla_escolha":
            alternativas = q.get("alternativas") or {}
            if len(alternativas) < 2:
                problemas.append(f"{p} múltipla escolha precisa de pelo menos duas alternativas.")
            elif gabarito not in alternativas:
                problemas.append(f"{p} gabarito {gabarito!r} não é uma das alternativas.")

        apoio = q.get("apoio") or {}
        if apoio.get("trecho"):
            fonte = Path(apoio.get("fonte") or "")
            if not fonte.is_file():
                problemas.append(f"{p} o arquivo de fonte {str(fonte)!r} não existe.")
            elif not onde_esta(apoio["trecho"], fonte):
                problemas.append(f"{p} o trecho de apoio não está em {fonte}. Copie o trecho sem mudar nada.")
        elif apoio.get("questao"):
            real = reais.get(str(apoio["questao"]))
            if not real:
                problemas.append(f"{p} a questão de apoio {apoio['questao']} não está em {QUESTOES}.")
            elif real.get("anulada") or not real.get("gabarito"):
                problemas.append(f"{p} a questão de apoio {apoio['questao']} está anulada ou sem gabarito.")
        else:
            problemas.append(f"{p} sem apoio. Toda questão precisa de um trecho de fonte ou de uma questão real.")

        for tec_id in q.get("inspirada_em") or []:
            if str(tec_id) not in reais:
                problemas.append(f"{p} inspirada_em {tec_id}, que não está em {QUESTOES}.")

    if problemas:
        _parar(problemas)

    codigos = [int(m.group(1)) for q in ler_jsonl(QUESTOES)
               if (m := re.fullmatch(r"g-(\d+)", str(q.get("codigo", ""))))]
    proximo = max(codigos, default=0) + 1
    agora = datetime.now().isoformat(timespec="seconds")
    novas = []
    for n, q in enumerate(questoes, 1):
        q["n"], q["codigo"] = n, f"g-{proximo:04d}"
        proximo += 1
        alternativas = q.get("alternativas") or {"C": "Certo", "E": "Errado"}
        novas.append({
            "codigo": q["codigo"],
            "ids": [item],
            "origem": "gerada",
            "formato_item": formato,
            "enunciado": q["enunciado"],
            "alternativas": alternativas,
            "gabarito": q["gabarito"],
            "apoio": q["apoio"],
            "inspirada_em": [str(t) for t in q.get("inspirada_em") or []],
            "pegadinha": q.get("pegadinha"),
            "criada_em": agora,
        })
    gravar_jsonl(QUESTOES, ler_jsonl(QUESTOES) + novas)
    rodada["preparada_em"] = agora
    _gravar_rodada(caminho, rodada)
    print(f"Rodada pronta: {len(questoes)} questões ({novas[0]['codigo']} a {novas[-1]['codigo']}). "
          "Mostre ao aluno sem os gabaritos.")


def _respostas(texto: str, rodada: dict) -> dict[int, tuple[str, bool]]:
    questoes, formato = rodada["questoes"], rodada["formato"]
    padrao = re.compile(r"(\d+)\s*([A-Za-z-])\s*(\?)?")
    sobra = padrao.sub("", texto).strip(" ,;\n\t")
    if sobra:
        _parar(f"Não entendi esta parte das respostas: {sobra!r}. Pergunte ao aluno.")
    respostas = {}
    for numero, letra, duvida in padrao.findall(texto):
        n, letra = int(numero), letra.upper()
        if not 1 <= n <= len(questoes):
            _parar(f"A rodada não tem a questão {n}.")
        if n in respostas:
            _parar(f"A questão {n} aparece duas vezes nas respostas.")
        validas = {"C", "E", "B"} if formato == "certo_errado" else set(questoes[n - 1].get("alternativas") or {}) | {"-"}
        if letra not in validas:
            _parar(f"Resposta {letra!r} não vale para a questão {n}. Válidas: {', '.join(sorted(validas))}.")
        respostas[n] = (letra, bool(duvida))
    faltam = [n for n in range(1, len(questoes) + 1) if n not in respostas]
    if faltam:
        _parar(f"Faltou a resposta da(s) questão(ões) {', '.join(map(str, faltam))}. Pergunte ao aluno.")
    return respostas


def _ler_csv() -> list[dict]:
    if not RESPOSTAS.exists():
        return []
    with RESPOSTAS.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def _gravar_csv(linhas: list[dict]) -> None:
    RESPOSTAS.parent.mkdir(parents=True, exist_ok=True)
    with RESPOSTAS.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";", lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(linhas)


def corrigir(caminho: Path, texto: str) -> None:
    rodada = _ler_rodada(caminho)
    questoes = rodada.get("questoes") or []
    if not questoes or not all("codigo" in q for q in questoes):
        _parar("Esta rodada ainda não foi preparada. Rode o comando preparar antes.")
    if rodada.get("corrigida_em"):
        _parar("Esta rodada já foi corrigida.")
    respostas = _respostas(texto, rodada)
    em_branco = "B" if rodada["formato"] == "certo_errado" else "-"

    hoje, linhas = date.today().isoformat(), []
    contagem = {"acerto": 0, "erro": 0, "branco": 0}
    erros_sem_duvida = acertos_com_duvida = 0
    for q in questoes:
        resposta, duvida = respostas[q["n"]]
        if resposta == em_branco:
            resultado = "branco"
        else:
            resultado = "acerto" if resposta == q["gabarito"] else "erro"
        contagem[resultado] += 1
        erros_sem_duvida += resultado == "erro" and not duvida
        acertos_com_duvida += resultado == "acerto" and duvida
        linhas.append({"data": hoje, "item": rodada["item"], "questao": q["codigo"], "resposta": resposta,
                       "gabarito": q["gabarito"], "resultado": resultado,
                       "duvida": "sim" if duvida else "nao", "ponto": ""})
        print(f"{q['n']}: {resultado} (respondeu {resposta}, gabarito {q['gabarito']}"
              f"{', com dúvida' if duvida else ''})")

    _gravar_csv(_ler_csv() + linhas)
    rodada["corrigida_em"] = datetime.now().isoformat(timespec="seconds")
    _gravar_rodada(caminho, rodada)
    print(f"Total: {contagem['acerto']} acerto(s), {contagem['erro']} erro(s) "
          f"({erros_sem_duvida} sem dúvida), {contagem['branco']} em branco; "
          f"{acertos_com_duvida} acerto(s) com dúvida.")


def anotar(caminho: Path, numero: int, ponto: str) -> None:
    rodada = _ler_rodada(caminho)
    questao = next((q for q in rodada.get("questoes") or [] if q.get("n") == numero), None)
    if not questao or "codigo" not in questao:
        _parar(f"A rodada não tem a questão {numero} preparada.")
    linhas = _ler_csv()
    alvo = next((l for l in reversed(linhas) if l["questao"] == questao["codigo"]), None)
    if not alvo:
        _parar(f"A questão {numero} ainda não foi corrigida.")
    if alvo["resultado"] != "erro":
        _parar(f"A questão {numero} não foi um erro ({alvo['resultado']}); ponto só se anota em erro.")
    alvo["ponto"] = " ".join(ponto.split())
    _gravar_csv(linhas)
    print(f"Ponto anotado na questão {numero} ({questao['codigo']}).")


def main() -> None:
    utf8()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="comando", required=True)
    p = sub.add_parser("preparar")
    p.add_argument("rodada", type=Path)
    c = sub.add_parser("corrigir")
    c.add_argument("rodada", type=Path)
    c.add_argument("respostas")
    a = sub.add_parser("anotar")
    a.add_argument("rodada", type=Path)
    a.add_argument("numero", type=int)
    a.add_argument("ponto")
    args = parser.parse_args()
    if args.comando == "preparar":
        preparar(args.rodada)
    elif args.comando == "corrigir":
        corrigir(args.rodada, args.respostas)
    else:
        anotar(args.rodada, args.numero, args.ponto)


if __name__ == "__main__":
    main()
