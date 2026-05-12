"""Generate a Word specification from a YAML description.

Usage:
    python generate_spec.py <input.yaml> <output.docx>

The YAML schema is documented in templates/spec_minimal.yaml. The schema
intentionally covers the common cases (metadata, version table, sections with
paragraphs, tables, bullets, callouts, images, page breaks). For anything more
elaborate, fall back to copying templates/spec_skeleton.py and customizing it.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running this file directly without installing the skill.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lib"))

import yaml  # type: ignore

from spec_helpers import (
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


def render_block(doc, block: dict, base_dir: Path) -> None:
    """Render a single content block."""
    if "heading" in block:
        add_heading(doc, block["heading"], level=block.get("level", 1))
    if "paragraph" in block:
        add_para(doc, block["paragraph"], bold=block.get("bold", False), italic=block.get("italic", False))
    if "paragraphs" in block:
        for p in block["paragraphs"]:
            add_para(doc, p)
    if "bullets" in block:
        add_bullets(doc, block["bullets"])
    if "table" in block:
        t = block["table"]
        add_table(
            doc,
            t["headers"],
            t["rows"],
            widths_cm=t.get("widths_cm"),
        )
    if "callout" in block:
        c = block["callout"]
        add_callout(doc, c["title"], c["body"], fill=c.get("fill", "DDF0DD"), border=c.get("border", "548235"))
    if "image" in block:
        img = block["image"]
        path = (base_dir / img["path"]).resolve() if not Path(img["path"]).is_absolute() else Path(img["path"])
        add_image(doc, path, width_cm=img.get("width_cm", 14), caption=img.get("caption"))
    if block.get("page_break"):
        doc.add_page_break()


def main() -> int:
    if len(sys.argv) != 3:
        print("uso: generate_spec.py <input.yaml> <output.docx>", file=sys.stderr)
        return 2

    yaml_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    with yaml_path.open("r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    base_dir = yaml_path.parent
    doc = Doc()

    meta = spec.get("metadata", {})
    cover(
        doc,
        title=meta.get("title", "Especificação"),
        subtitle=meta.get("subtitle", ""),
        subtitle2=meta.get("subtitle2", ""),
        subtitle3=meta.get("subtitle3", ""),
    )

    if "metadata_rows" in spec:
        metadata_block(doc, [(k, v) for k, v in spec["metadata_rows"]])

    doc.add_page_break()

    if "versions" in spec:
        version_table(doc, [tuple(r) for r in spec["versions"]])

    if "summary" in spec:
        summary(doc, spec["summary"])

    for block in spec.get("sections", []):
        render_block(doc, block, base_dir)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    print(f"salvo: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
