"""Skeleton para gerar uma especificação funcional em Word.

Copie este arquivo para o projeto (ex: codigos/gerar_especificacao_<escopo>.py),
ajuste os caminhos e o conteúdo. Os helpers vêm da skill meeting-spec-generator.

Estilo visual padrão: cabeçalhos azuis, tabelas com cabeçalho azul e zebra,
callouts verdes para pontos críticos, capa com título e subtítulos
hierárquicos. Cores e fonte são ajustáveis em lib/spec_helpers.py.

Estilo de redação (ajuste conforme a preferência do projeto):
  - sem travessão ou hífen como pontuação em texto corrido,
  - frases curtas e diretas,
  - identificadores em maiúsculas (RF01, R1, P14).
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

# Aponte para a pasta lib da skill instalada no usuário.
SKILL_LIB = Path.home() / ".claude" / "skills" / "meeting-spec-generator" / "lib"
sys.path.insert(0, str(SKILL_LIB))

from spec_helpers import (  # noqa: E402
    Doc,
    add_bullets,
    add_callout,
    add_heading,
    add_image,
    add_para,
    add_table,
    cover,
    metadata_block,
    summary,
    version_table,
)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------- ajuste estes valores por projeto ----------
BASE = Path(r"C:\caminho\para\projeto\analise")
OUT = BASE / "especificacoes" / "Especificacao_Exemplo.docx"
IMG_FIGURA1 = BASE / "evidencias" / "figura1.png"

VERSAO = "1.0"
DATA = date.today().strftime("%d/%m/%Y")
AUTOR = "Seu Nome"
PROJETO = "MEU_PROJETO"
ESCOPO = "Nome do Escopo"
# ------------------------------------------------------

doc = Doc()

# Capa.
cover(
    doc,
    title="Especificação Funcional",
    subtitle=ESCOPO,
    subtitle2="Subtítulo descritivo opcional",
    subtitle3="Linha extra em itálico",
)

# Bloco de metadados.
metadata_block(
    doc,
    [
        ("Projeto", f"{PROJETO}  |  Aplicação"),
        ("Versão", f"{VERSAO}   |   Estado: Especificação inicial"),
        ("Data", DATA),
        ("Autor", AUTOR),
        ("Fontes", "Reunião de DD/MM/YYYY. Rascunhos e evidências em evidencias/."),
    ],
)
doc.add_page_break()

# Controle de versão.
version_table(
    doc,
    [
        (VERSAO, DATA, AUTOR, "Primeira versão. Resumo do conteúdo desta release."),
    ],
)

# Sumário.
summary(
    doc,
    [
        "1. Visão geral",
        "2. Contexto",
        "3. Atores",
        "4. Escopo",
        "5. Glossário",
        "6. Regras de negócio",
        "7. Requisitos funcionais",
        "8. Requisitos não funcionais",
        "9. Pendências",
        "10. Anexos",
    ],
)

# 1. Visão geral.
add_heading(doc, "1. Visão geral", level=1)
add_heading(doc, "1.1 Problema", level=2)
add_para(doc, "Descrição do problema em parágrafo único.")
add_heading(doc, "1.2 Objetivo", level=2)
add_para(doc, "Texto do objetivo. Frases curtas e diretas.")
add_heading(doc, "1.3 Resultado esperado", level=2)
add_bullets(
    doc,
    [
        "Resultado 1.",
        "Resultado 2.",
        "Resultado 3.",
    ],
)
add_callout(
    doc,
    "ESCOPO DESTA ESPECIFICAÇÃO",
    "Este documento cobre apenas o tema X. O tema Y fica para spec separada.",
)

# 6. Regras de negócio.
add_heading(doc, "6. Regras de negócio", level=1)
add_table(
    doc,
    ["ID", "Regra"],
    [
        ("R01", "Texto da primeira regra."),
        ("R02", "Texto da segunda regra."),
    ],
    widths_cm=[1.8, 14.2],
)

# 7. Requisitos funcionais.
add_heading(doc, "7. Requisitos funcionais", level=1)
add_table(
    doc,
    ["ID", "Requisito"],
    [
        ("RF01", "O sistema deve fazer A."),
        ("RF02", "O sistema deve fazer B."),
    ],
    widths_cm=[1.6, 14.4],
)

# 10. Anexos.
add_heading(doc, "10. Anexos", level=1)
if IMG_FIGURA1.exists():
    add_image(
        doc,
        IMG_FIGURA1,
        width_cm=12,
        caption="Figura 1. Legenda explicativa.",
    )

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUT))
print(f"salvo: {OUT}")
