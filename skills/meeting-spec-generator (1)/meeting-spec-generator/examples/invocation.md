# Example invocations

## Example 1. Single meeting with audio + photographed whiteboard

User says:

> Tivemos uma reunião hoje. O áudio está em `audio/reuniao.qta` e tem uma foto
> do rascunho em `img/rascunho.HEIC`. Transcreva e gere uma especificação.

Expected behavior:

1. Glob both folders to confirm the inputs.
2. Convert the HEIC to PNG via `convert_image.py`.
3. Read the PNG to understand the sketch.
4. Run `transcribe.py` on the audio (`run_in_background: true` if longer than
   15 min).
5. Read the transcription text.
6. Identify the central topic. Ask the user only if ambiguous.
7. Suppress side conversations and unrelated topics.
8. Generate the spec via YAML or custom Python.
9. Save artifacts under `transcricoes/`, `evidencias/` and
   `especificacoes/`, or under whatever folder convention the project already
   uses. Append a session entry to any project memory file at the root
   (`MEMORIA.md`, `MEMORY.md`, `NOTES.md`, `JOURNAL.md`, `CLAUDE.md`) if one
   exists. Do not create such a file if it does not already exist.

## Example 2. Folder with several recordings

User says:

> Pasta `gravacoes/` tem 5 áudios de uma sequência de reuniões sobre o produto
> X. Quero uma especificação consolidada.

Expected behavior:

1. `transcribe.py --folder gravacoes/ --out transcricoes/`.
2. Read each `.txt`.
3. Build a unified outline before generating the doc.
4. The spec gets a single version label (1.0) with all recordings cited as
   sources in the metadata block and the version table.

## Example 3. Only transcription requested

User says:

> Só transcreva esse áudio aí, não precisa de doc.

Expected behavior:

1. Run `transcribe.py`.
2. Show the path to the `.txt` and a short preview.
3. Stop. Do not generate any docx.

## Example 4. Quick image conversion

User says:

> Pode converter esse `IMG_1234.HEIC` pra PNG?

Expected behavior:

1. Run `convert_image.py`.
2. Read the resulting PNG to confirm the conversion.
3. Show the output path.
4. Stop. No transcription, no docx.

## Example 5. Updating an existing spec

User says:

> Tem uma nova reunião complementando a especificação anterior. Refaça mantendo
> histórico.

Expected behavior:

1. Locate the current `<spec_name>.docx` and move it to
   `backups/<spec_name>_old_YYYY-MM-DD.docx` using today's absolute date.
2. Transcribe the new audio.
3. Merge the new content into the existing spec script or YAML, bumping the
   version. Minor bump (1.x → 1.x+1) for incremental edits; major bump
   (x.0 → x+1.0) when scope or canonical source changes.
4. Regenerate. Update the version control table.
5. If a project memory file exists, append an entry describing the merge and
   the version bump.

## Tips

- When the user provides files in unusual extensions (`.qta`, weird image
  containers), do **not** ask the user to rename them. Run the scripts; they
  detect the actual codec.
- When the audio is long, kick off transcription in background **immediately**
  and use the wait time to read images and prepare the outline.
- When the user provides only an image of a handwritten sketch, often the
  whole spec can be derived from the photo alone. Do not invent audio.
- Keep the YAML route as the default. Switch to custom Python only when the
  YAML schema does not accommodate something obvious.
- Folder layout (`transcricoes/`, `evidencias/`, `especificacoes/`) is a
  default. If the project already uses different names, follow the project.
