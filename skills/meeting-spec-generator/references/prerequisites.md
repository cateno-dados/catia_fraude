# Prerequisites

The skill needs **Python 3.10+** and **ffmpeg**, plus three Python packages.

## Quick check

```bash
python -c "import faster_whisper, docx, yaml; print('ok')" && ffmpeg -version | head -1
```

If both lines succeed the skill is ready.

## Install Python packages

```bash
pip install --user faster-whisper python-docx pyyaml
```

`faster-whisper` brings its own `ctranslate2` runtime. On Windows you also need
the **Microsoft Visual C++ Redistributable 2015 to 2022**. Install via:

```powershell
winget install Microsoft.VCRedist.2015+.x64
```

## Install ffmpeg

| OS | Command |
|----|---------|
| Windows | `winget install Gyan.FFmpeg` |
| macOS | `brew install ffmpeg` |
| Debian / Ubuntu | `sudo apt install ffmpeg` |

The transcription script auto-detects the Gyan.FFmpeg location used by winget,
so you do not need to add ffmpeg to PATH manually after installing.

## Models and disk

faster-whisper downloads the model on first use. Sizes:

| Model | Disk | RAM | PT-BR quality |
|-------|------|-----|---------------|
| `tiny` | 75 MB | 1 GB | low |
| `base` | 142 MB | 1 GB | medium |
| `small` | 466 MB | 2 GB | good |
| `medium` | 1.5 GB | 5 GB | very good (default) |
| `large-v3` | 2.9 GB | 10 GB | best |

For meetings up to about 1 hour, `medium` on CPU `int8` is the right balance.

## GPU acceleration (optional)

If a CUDA GPU is available:

```bash
python transcribe.py <file> --device cuda --compute-type float16
```

You also need CUDA Toolkit and cuDNN matching the ctranslate2 requirements.
On most machines CPU `int8` is faster to set up and fast enough.
