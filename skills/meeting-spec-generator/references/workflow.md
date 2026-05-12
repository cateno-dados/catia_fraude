# Detailed workflow

```
[ recording.{mp4,mov,m4a,qta,…} ]   [ photo.{heic,jpg,png} ]
              │                              │
              │                              ▼
              │                  scripts/convert_image.py
              │                              │
              ▼                              ▼
     scripts/transcribe.py        evidencias/<name>.png
              │                              │
              ▼                              ▼
   transcricoes/<name>.txt+.srt       Read tool (Claude)
              │                              │
              └─────────────┬────────────────┘
                            ▼
              Claude analyzes content
              and suppresses off-topic
                            │
                            ▼
                ┌─────────── ───────────┐
                │   YAML route          │   Custom Python route
                │   (simple specs)      │   (complex specs)
                ▼                       ▼
   templates/spec_minimal.yaml      templates/spec_skeleton.py
                │                       │
                ▼                       ▼
   scripts/generate_spec.py        custom script imports
                │                  lib/spec_helpers.py
                ▼                       │
                └─────────┬─────────────┘
                          ▼
              especificacoes/<name>.docx
```

## Decision points

### Background or foreground transcription?

Audio is split by faster-whisper VAD then fed to the model. On CPU `int8`,
expect roughly **1 minute of wall clock per minute of audio** for `medium`.

| Audio length | Recommendation |
|--------------|----------------|
| < 5 min | run foreground, wait |
| 5 to 15 min | run foreground; warn user |
| > 15 min | `run_in_background: true` and poll |

Polling pattern:

```bash
until grep -q "salvo:" transcribe.log; do sleep 5; done
```

### YAML or custom Python?

| Use YAML when | Use Python skeleton when |
|---------------|--------------------------|
| Sections are flat (heading + content) | You need conditional logic |
| Tables fit headers + rows model | You need to compute values from data |
| One image per section is enough | You need many images, complex layouts |
| The whole spec fits in one file | The spec mixes content from multiple sources |

### When to escalate to a multi-document spec

Split into multiple specs (functional + technical, or operational + quality)
when:

- The audience changes (operations vs. tech).
- The lifecycle changes (one is short term, one is long term).
- Different specs have different sponsors.

Typical split: a Functional spec for what the system does, a Technical spec
for how it is built, and side specs for adjacent concerns such as quality
control, governance or operations. Each spec carries its own version table
and lifecycle.

## Suppression of off-topic content

The user usually flags this explicitly: *"outros temas podem ter sido
tratados, conversas aleatórias, suprima quando o conteúdo não for o do tema
principal"*.

Heuristics for detection:

1. Sudden change of speaker subject mid-flow.
2. Mentions of people unrelated to the central topic.
3. References to physical surroundings (the office, the chairs, the weather).
4. Side projects or parallel deliveries.
5. Personal anecdotes.

Do not summarize off-topic stretches. Drop them entirely. They never appear in
the final document.

If unsure whether something is on or off topic, **ask the user** before
generating the document. One clarifying question is cheaper than a wrong spec.

## Versioning the document

Every generated `.docx` has:

1. **Cover** with title, subtitle, escopo.
2. **Metadata block** with project, version, date, author, sources.
3. **Version control table** with the change log.
4. **Summary** of sections.

Increment policy:

- `1.0` → first version.
- `1.1`, `1.2` → incremental edits, same scope.
- `2.0`, `3.0` → reorganization, new fonte canônica, scope change.

When regenerating preserving the previous version:

1. Move the current `<name>.docx` to `<name>_old_YYYY-MM-DD.docx` in a
   `backups/` folder.
2. Generate the new version.
3. Update the version control table.
