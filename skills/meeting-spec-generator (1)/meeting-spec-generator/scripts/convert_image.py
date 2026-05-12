"""Convert HEIC and other image formats to PNG using ffmpeg.

Useful before reading photos of whiteboards or handwritten notes shot from an
iPhone (HEIC) so Claude can ingest them via the Read tool.

Usage:
    python convert_image.py <input> <output.png>           single file
    python convert_image.py --folder <dir> --out <dir>     batch
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

IMAGE_EXTS = {".heic", ".heif", ".png", ".jpg", ".jpeg", ".webp", ".tiff", ".tif", ".bmp", ".avif"}


def find_ffmpeg() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    candidates = [
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages",
    ]
    for base in candidates:
        if not base.exists():
            continue
        for sub in base.glob("Gyan.FFmpeg_*/ffmpeg-*-full_build/bin/ffmpeg.exe"):
            return str(sub)
    raise SystemExit("ffmpeg não encontrado. Instale via winget/brew/apt e tente novamente.")


def convert_one(ffmpeg: str, src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg, "-y", "-i", str(src), "-update", "1", "-frames:v", "1", str(dst)]
    print(f"convertendo {src.name} -> {dst}", flush=True)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # ffmpeg often emits warnings on the first file pattern; rely on output existence.
    if not dst.exists() or dst.stat().st_size == 0:
        sys.stderr.write(proc.stderr[-2000:] + "\n")
        raise SystemExit(f"falha ao gerar {dst}")
    print(f"salvo: {dst} ({dst.stat().st_size:,} bytes)", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert images to PNG via ffmpeg.")
    parser.add_argument("input", nargs="?", help="Single input file.")
    parser.add_argument("output", nargs="?", help="Single output PNG path.")
    parser.add_argument("--folder", help="Source folder for batch conversion.")
    parser.add_argument("--out", help="Output folder for batch conversion.")
    args = parser.parse_args()

    ffmpeg = find_ffmpeg()

    if args.folder:
        out_dir = Path(args.out or "evidencias")
        out_dir.mkdir(parents=True, exist_ok=True)
        sources = [p for p in Path(args.folder).rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
        if not sources:
            print("nenhuma imagem encontrada.", file=sys.stderr)
            return 1
        for src in sources:
            dst = out_dir / (src.stem + ".png")
            convert_one(ffmpeg, src, dst)
        return 0

    if not args.input or not args.output:
        parser.error("informe <input> <output.png> OU use --folder e --out.")

    convert_one(ffmpeg, Path(args.input), Path(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
