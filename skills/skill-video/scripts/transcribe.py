"""Transcribe audio or video files using faster-whisper.

Robust to extension mismatches (e.g. a QuickTime container saved as .qta).
ffmpeg is auto-detected from PATH; on Windows, also looks at the winget
location used by Gyan.FFmpeg.

Usage:
    python transcribe.py <file>                   transcribe one file
    python transcribe.py --folder <dir>           transcribe every media file in a folder
    python transcribe.py <file> --out <dir>       choose output folder (default: ./transcricoes)
    python transcribe.py <file> --lang en         override language (default: pt)
    python transcribe.py <file> --model small     pick a different model (default: medium)

Outputs <stem>.txt (plain text) and <stem>.srt (timestamped) per input.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import unicodedata
from datetime import timedelta
from pathlib import Path

# Force UTF-8 stdout so accented Portuguese prints cleanly on Windows cp1252 consoles.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MEDIA_EXTS = {
    ".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac", ".opus", ".amr",
    ".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".flv",
    ".qta",  # observed in the wild: QuickTime audio with non-standard extension
}


def find_ffmpeg() -> str | None:
    """Return a directory containing ffmpeg, or None if it is on PATH already."""
    if shutil.which("ffmpeg"):
        return None
    # Common Windows winget install location for Gyan.FFmpeg.
    candidates = [
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages",
    ]
    for base in candidates:
        if not base.exists():
            continue
        for sub in base.glob("Gyan.FFmpeg_*/ffmpeg-*-full_build/bin"):
            if (sub / "ffmpeg.exe").exists():
                return str(sub)
    return None


def fmt_ts(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)
    h, rem = divmod(total_ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ascii_safe(name: str) -> str:
    """Slug compatible with both Windows shells and bash."""
    import re
    decomposed = unicodedata.normalize("NFKD", name)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", stripped).strip("_")
    return slug or "saida"


def transcribe_one(model, src: Path, out_dir: Path, language: str) -> tuple[Path, Path]:
    print(f"\n=== {src.name} ===", flush=True)
    segments, info = model.transcribe(
        str(src),
        language=language,
        vad_filter=True,
        beam_size=5,
    )
    print(
        f"duração detectada: {info.duration:.1f}s | idioma: {info.language} (prob {info.language_probability:.2f})",
        flush=True,
    )

    stem = ascii_safe(src.stem)
    txt_path = out_dir / f"{stem}.txt"
    srt_path = out_dir / f"{stem}.srt"

    with txt_path.open("w", encoding="utf-8") as txt_f, srt_path.open("w", encoding="utf-8") as srt_f:
        for i, seg in enumerate(segments, start=1):
            text = seg.text.strip()
            txt_f.write(text + "\n")
            srt_f.write(f"{i}\n{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}\n{text}\n\n")
            if i % 20 == 0:
                print(f"  .. segmento {i} @ {seg.end:.0f}s", flush=True)

    print(f"salvo: {txt_path}", flush=True)
    print(f"salvo: {srt_path}", flush=True)
    return txt_path, srt_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe audio/video using faster-whisper.")
    parser.add_argument("input", nargs="?", help="Path to a single media file.")
    parser.add_argument("--folder", help="Path to a folder; every media file inside is transcribed.")
    parser.add_argument("--out", default="transcricoes", help="Output folder (default: ./transcricoes).")
    parser.add_argument("--lang", default="pt", help="Language code (default: pt).")
    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="faster-whisper model size (default: medium).",
    )
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda", "auto"])
    parser.add_argument("--compute-type", default="int8", help="int8 | int8_float16 | float16 | float32")
    args = parser.parse_args()

    if not args.input and not args.folder:
        parser.error("provide a file path or --folder.")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Make ffmpeg reachable for faster-whisper.
    ffmpeg_dir = find_ffmpeg()
    if ffmpeg_dir and ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    # Discover targets.
    if args.folder:
        folder = Path(args.folder)
        targets = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in MEDIA_EXTS)
    else:
        targets = [Path(args.input)]

    if not targets:
        print("nenhum arquivo de mídia encontrado.", file=sys.stderr)
        return 1

    # Lazy import so --help works even before faster-whisper is installed.
    from faster_whisper import WhisperModel

    print(f"carregando modelo faster-whisper '{args.model}' (baixa na 1a execução)…", flush=True)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    for t in targets:
        try:
            transcribe_one(model, t, out_dir, args.lang)
        except Exception as e:  # noqa: BLE001
            print(f"falha em {t.name}: {e}", file=sys.stderr)
            continue

    return 0


if __name__ == "__main__":
    sys.exit(main())
