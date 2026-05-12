# Codecs and formats supported

The skill never trusts file extensions. Detection always happens through
ffmpeg, which understands hundreds of containers and codecs.

## Audio inputs (verified)

| Format | Extension | Notes |
|--------|-----------|-------|
| MP3 | `.mp3` | Standard. |
| AAC in M4A | `.m4a` | Common from voice memo apps. |
| Wave | `.wav` | Lossless, large. |
| Ogg / Vorbis / Opus | `.ogg`, `.opus` | |
| FLAC | `.flac` | |
| AMR | `.amr` | Older mobile recorders. |
| QuickTime audio (any track) | `.mov`, `.qta` | The motivating case: an iPhone recording arrived as `.qta` but was a QuickTime container. ffmpeg reads it. |

## Video inputs (audio extracted automatically)

| Format | Extension | Notes |
|--------|-----------|-------|
| MP4 / H.264 / H.265 | `.mp4`, `.m4v` | |
| QuickTime | `.mov` | |
| Matroska | `.mkv` | |
| WebM | `.webm` | |
| AVI / MPEG | `.avi`, `.mpg` | |
| Flash | `.flv` | |

## Image inputs

| Format | Extension | Conversion needed |
|--------|-----------|-------------------|
| HEIC / HEIF | `.heic`, `.heif` | Yes. iPhone default. Convert to PNG first so Claude can read it. |
| AVIF | `.avif` | Yes. Convert to PNG. |
| PNG | `.png` | No. Claude reads directly. |
| JPEG | `.jpg`, `.jpeg` | No. |
| WebP | `.webp` | No. |
| TIFF | `.tiff`, `.tif` | Convert if Claude refuses to read. |
| BMP | `.bmp` | No. |

The HEIC case is the one that bites users daily. Use
`scripts/convert_image.py` before reading.

## Edge cases

- **HEIC bursts**: a single `.heic` may hold multiple frames. The conversion
  script uses `-update 1 -frames:v 1` to keep only the first frame. Reasonable
  for a photographed sketch; not appropriate for sequence content.
- **Mismatched extension**: rely on `file` or `ffprobe` to identify the actual
  container. Never decide based on extension alone.
- **Stereo to mono**: faster-whisper handles both. No conversion needed.
- **Two languages in one recording**: pass `--lang` matching the dominant
  language. The model still recognizes occasional code switches.
