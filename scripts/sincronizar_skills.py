# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Copia as skills de .agents/skills (versão oficial, lida pelo Codex) para .claude/skills
(lida pelo Claude Code). A cópia é apagada e refeita; nunca edite .claude/skills à mão.

Uso (a partir da pasta do projeto):
    uv run scripts/sincronizar_skills.py
"""

import shutil
import sys
from pathlib import Path

from comum import utf8

ORIGEM = Path(".agents/skills")
DESTINO = Path(".claude/skills")


def main() -> None:
    utf8()
    if not ORIGEM.is_dir():
        sys.exit(f"Não achei {ORIGEM}. Rode a partir da pasta do projeto.")
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEM, DESTINO)
    skills = sorted(p.name for p in DESTINO.iterdir() if (p / "SKILL.md").is_file())
    print(f"{len(skills)} skill(s) copiada(s) para {DESTINO}: {', '.join(skills)}.")


if __name__ == "__main__":
    main()
