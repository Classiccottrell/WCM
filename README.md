# West Coast Modern — Hero Image Selection Pipeline

This repository automates hero image selection for West Coast Modern property photography. A two-stage AI pipeline turns 200–400 raw photos into a production-ready Hero Report in one command.

**What it does:**
1. **Stage 1 — Triage** — every image is scored 0–60 for WCM hero fit using a fast model in parallel. Results go to `triage_scores.csv`.
2. **Stage 2 — Hero Pick** — the top-N scoring images are sent at full quality to a stronger model with the full `SKILL.md` rubric. Output is `hero_report.md`.

---

## Three Ways to Use This

| Mode | Best for | Setup time |
|---|---|---|
| **Manual — claude.ai** | Ad-hoc sessions from any device, small batches | 0 min |
| **Manual — Claude Cowork** | Large local shoots, no uploads needed | 5 min |
| **Automated — Python pipeline** | Hands-free, triggered by folder drop | 15 min |

---

## Mode 1 — Manual (claude.ai)

No setup required. Best for running a selection session from any device or when photos are already in Google Drive / Dropbox.

1. Open [claude.ai](https://claude.ai) (Pro plan recommended for large batches)
2. Paste the full contents of `Hero-Image-Agent/SKILL.md` into a new conversation with this prompt:

```
I'm going to run a hero image selection session for West Coast Modern.
Here are your instructions:

[PASTE FULL CONTENTS OF SKILL.md HERE]

Ready to receive photos.
```

3. (Optional) Paste the completed `TASTE_REFERENCE_TEMPLATE.md` next for calibrated taste.
4. Upload photos and run:

```
Property: [House Name]
Hook: [One sentence about what makes this property unique]
Target: [MLS | Instagram | Email | Feature Story | All]

[DRAG AND DROP PHOTOS — up to 20 at a time]

Run the hero selection.
```

5. Claude outputs the Hero Report. Review, confirm, save to Google Drive.

**Tips:** Upload 20–30 photos per batch. For 200+ photos, pull the top 40–50 exteriors first, then run the skill on those.

---

## Mode 2 — Manual (Claude Cowork)

Best for Trent reviewing a fresh shoot directly from his Mac. Photos stay local — no uploading.

1. Open a new Claude Cowork session (desktop app, sign in with claude.ai credentials)
2. Paste `SKILL.md` contents the same as Mode 1
3. Point Claude at the folder instead of uploading:

```
Property: [House Name]
Hook: [One sentence about what makes this property unique]
Target: [MLS | Instagram | Email | Feature Story | All]

Photos are in this folder on my Mac:
/Users/[yourname]/Dropbox/WCM/[PropertyName]/photography/raw/

Please read all images in that folder and run the hero selection.
```

Claude Cowork reads images directly from that path. You can ask follow-up questions, request score breakdowns, or compare specific candidates before confirming.

---

## Mode 3 — Automated Python Pipeline

Runs entirely from the command line. No manual uploads. Outputs land directly in the property folder.

### Setup

```bash
cd Hero-Image-Agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

The API key is required. The script exits clearly with instructions if it is not set.

### Run on a single folder

```bash
python3 hero_select.py /path/to/PropertyName
```

**All options:**

| Flag | Default | Description |
|---|---|---|
| `--top N` | `12` | How many top-scoring images go to Stage 2 |
| `--workers N` | `5` | Parallel workers for Stage 1 triage |
| `--skill PATH` | `SKILL.md` next to the script | Override the Stage-2 prompt file |
| `--resume` | off | Skip Stage 1 and reload scores from an existing `triage_scores.csv` — use when Stage 1 finished but Stage 2 failed |

**Examples:**

```bash
# Standard run
python3 hero_select.py /path/to/PropertyName

# Review more candidates in Stage 2, more parallelism
python3 hero_select.py /path/to/PropertyName --top 20 --workers 10

# Stage 1 already ran but Stage 2 failed — pick up where you left off
python3 hero_select.py /path/to/PropertyName --resume

# Use a different skill file
python3 hero_select.py /path/to/PropertyName --skill /path/to/custom-SKILL.md
```

**Outputs written into the property folder:**
- `triage_scores.csv` — every image with `file, score, isExterior, note`, sorted highest to lowest
- `hero_report.md` — the full Hero Report (hero horizontal, vertical alt, hero 2, shortlist, tour sequence, cuts, flags)

### Watch a parent folder (automatic mode)

`watch_folder.py` monitors a parent directory. When a new property subfolder appears and its contents stop changing for ~30 seconds (copy finished), the pipeline runs automatically. Folders that already have `hero_report.md` are skipped.

```bash
python3 watch_folder.py /path/to/Parent
```

**All options:**

| Flag | Default | Description |
|---|---|---|
| `--top N` | `12` | Passed through to `hero_select.py` |
| `--workers N` | `5` | Passed through to `hero_select.py` |
| `--skill PATH` | `SKILL.md` next to the script | Override the Stage-2 prompt file |
| `--scan-existing` | off | Also process pre-existing subfolders that have no report yet |

**Examples:**

```bash
# Watch for new folders
python3 watch_folder.py /path/to/Parent

# Watch AND process any existing unfinished folders on start
python3 watch_folder.py /path/to/Parent --scan-existing

# Watch with custom settings
python3 watch_folder.py /path/to/Parent --top 20 --workers 8 --scan-existing
```

### Start the watcher automatically at login (macOS launchd)

1. Edit `Hero-Image-Agent/com.westcoastmodern.heroselect.plist` — fill in the four `CHANGE_ME` values:
   - Absolute path to `python3` (run `which python3` to find it)
   - Absolute path to `watch_folder.py`
   - The parent directory to watch
   - Your `ANTHROPIC_API_KEY`

   > The API key must be in the plist's `EnvironmentVariables` block. A login launchd agent does not read `~/.zshrc`, so a shell `export` will not reach it.

2. Install and start:

```bash
cp Hero-Image-Agent/com.westcoastmodern.heroselect.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.westcoastmodern.heroselect.plist
launchctl start com.westcoastmodern.heroselect
```

Logs: `/tmp/wcm-hero-watch.out.log` and `/tmp/wcm-hero-watch.err.log`

3. Stop / uninstall:

```bash
launchctl unload ~/Library/LaunchAgents/com.westcoastmodern.heroselect.plist
```

---

## Folder Structure

```
/WCM/
  /[PropertyName]/
    /photography/
      /raw/           ← Photographer uploads here
      /curated/       ← Hero report lands here
      /final/         ← Approved selects
      /sets/
        /mls/
        /email/
        /instagram/
        /website/
```

---

## Files in This Repo

```
/Hero-Image-Agent/
├── hero_select.py                        ← Two-stage pipeline engine + CLI
├── watch_folder.py                       ← Folder watcher (runs engine automatically)
├── requirements.txt                      ← anthropic, Pillow, watchdog
├── com.westcoastmodern.heroselect.plist  ← launchd agent for auto-start at login
├── SKILL.md                              ← Stage-2 system prompt (the full hero rubric)
├── AGENT.md                              ← Agent identity and capabilities
├── TASTE_REFERENCE_TEMPLATE.md          ← Trent fills this in (10 good + 10 not-hero)
├── WCM_STYLE_PROFILE.md                 ← Brand aesthetic reference
├── INSTALL.md                            ← Detailed setup instructions per mode
├── MAKE_AUTOMATION_SETUP.md             ← Make.com + Dropbox automation guide
└── PIPELINE_README.md                   ← Technical deep-dive on the Python pipeline
```

---

## Who Does What

| Person | Role |
|---|---|
| **Trent** | Completes `TASTE_REFERENCE_TEMPLATE.md`; runs Cowork sessions; final hero sign-off |
| **Mica** | Runs the skill (manual or automated); reviews reports; confirms selects before Trent |
| **James (Photographer)** | Uploads to `/raw/` by deadline |
| **Philippe** | Receives confirmed hero list for copy pairing |
| **Jacob** | Receives confirmed hero list for B-roll pairing |

---

## Configurable Constants

These are at the top of `hero_select.py` and can be changed without touching anything else:

| Constant | Default | Meaning |
|---|---|---|
| `TRIAGE_MODEL` | `claude-haiku-4-5` | Model used for Stage 1 (fast, cheap) |
| `HERO_MODEL` | `claude-opus-4-5` | Model used for Stage 2 (full quality) |
| `TRIAGE_LONG_EDGE` | `768` | Downscale long edge for Stage 1 (px) |
| `HERO_LONG_EDGE` | `1568` | Downscale long edge for Stage 2 (px) |
| `DEFAULT_TOP_N` | `12` | Default images passed to Stage 2 |
| `DEFAULT_WORKERS` | `5` | Default parallel triage workers |

---

## Support

If Claude's selections feel off, the fastest fix is more taste reference examples from Trent in `TASTE_REFERENCE_TEMPLATE.md`. Each new example meaningfully improves output quality.
