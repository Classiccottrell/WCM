# wcm-hero-skill
### West Coast Modern — AI Hero Image Selector

> Takes Trent from 300 photos to 5 hero candidates without him touching a folder.

---

## What This Is

A skill + agent system that uses Claude's vision AI to review batches of property photography and select the best hero image — the lead shot that goes on the website, email, Instagram, and MLS listing.

Built for anyone to run independently. Designed around **Trent's** eye. Final sign-off always stays with Trent.

The system knows what West Coast Modern looks for: architect-designed homes with cinematic West Coast light, warm materiality, breathing room, and an emotional hook. It scores every image against a rubric and returns a production-ready report.

---

## The Problem It Solves

West Coast Modern receives 200–400 photos per property shoot. Trent has been the single point of selection — manually reviewing every set before production can begin. This is the biggest bottleneck in the content pipeline.

This skill takes the first pass. Trent reviews 3–5 options, not 300.

---

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Core instructions for Claude — the rubric, scoring system, output format |
| `AGENT.md` | Extended agent identity, capabilities, automation mode, escalation rules |
| `TASTE_REFERENCE_TEMPLATE.md` | Template for Trent to document 10 hero + 10 not-hero examples |
| `WCM_STYLE_PROFILE.md` | Extracted visual taste and brand aesthetic — feeds into skill calibration |
| `INSTALL.md` | Step-by-step setup for all three modes — written for non-coders |
| `wcm_cli.py` | The `wcm` command — `run`, `watch`, and `doctor` subcommands |
| `pyproject.toml` | Makes `wcm` installable with `pip install -e .` |
| `PIPELINE_README.md` | Technical deep-dive on the two-stage Python pipeline (`hero_select.py` + `watch_folder.py`) — run by hand, via `wcm`, or auto-run on new folders via launchd |

---

## Quick Start (Manual Mode — No Setup Required)

1. Open [claude.ai](https://claude.ai)
2. Paste the contents of `SKILL.md` into Claude
3. Optionally paste `TASTE_REFERENCE_TEMPLATE.md` (completed by Trent) for better results
4. Upload 20–50 property photos
5. Type: `Property: [House Name]. Run hero selection.`
6. Review the Hero Report

That's it. No API keys, no install, no configuration.

---

## Automated Mode (`wcm` Python pipeline)

For hands-free use — run hero selection straight from a folder on your machine, no uploading:

```
Photos land in a property folder
  → wcm run /path/to/PropertyName
  → Stage 1 scores every image (fast model, in parallel)
  → Stage 2 sends the top picks to a stronger model
  → triage_scores.csv + hero_report.md written into the folder
  → Trent reviews 3 options instead of 300
```

Or point `wcm watch` at a parent folder and it processes each new shoot automatically as it lands.

See `INSTALL.md` for plain-language setup and `PIPELINE_README.md` for the technical deep-dive.

---

## Outputs

For every property, the skill produces:

- **Hero (horizontal)** — primary lead image for website, email header, MLS image 1
- **Hero vertical** — Instagram stories, email vertical grid
- **Hero 2** — backup / second campaign option
- **Shortlist of 5–8** — gallery and tour sequence
- **MLS set** — up to 40 images, horizontals prioritized, ordered
- **Cuts list** — what not to use and why
- **Flags for Trent** — close calls and edge cases that need a human eye

---

## How to Improve the AI's Taste

The skill gets better with calibration. Fill out `TASTE_REFERENCE_TEMPLATE.md`:

- 10 examples of past WCM hero images and why they worked
- 10 examples of shots that were passed over and why
- Takes Trent ~45 minutes once; meaningfully improves every run after

Even 3–4 examples help. 10 examples produces output that's very close to Trent's instinct.

---

## Tech Stack

| Component | Tool |
|---|---|
| AI Vision | Claude API (`claude-opus-4-5` + `claude-haiku-4-5`) via Anthropic |
| Automated interface | `wcm` CLI — local Python (`hero_select.py` + `watch_folder.py`) |
| Auto-run on new folders | macOS `launchd` (or `cron`) running `wcm watch` |
| Photo storage | Local folder (e.g. a synced Dropbox/Drive folder) |
| Report storage | The property folder itself (`hero_report.md`) |
| Interface (manual) | claude.ai / Claude Cowork |

---

## Workflow Context

This skill is part of a larger WCM content production pipeline:

```
WF1: Content Consolidation
  → Photographer uploads to Dropbox
  → [THIS SKILL] Hero selection runs
  → Curated set confirmed

WF2: Content Creation
  → Copy person writes copy for each deliverable
  → Hero images matched to copy
  → Instagram, Email, Website sets prepared

WF3: Deployment
  → Squarespace listing published
  → MailChimp campaign sent
  → Instagram posted on schedule
```

---

## Contributing

1. Trent completes `TASTE_REFERENCE_TEMPLATE.md` → commit to `/taste-reference/`
2. Run a test batch and compare AI selection to Trent's manual pick
3. Note any consistent misses → update `SKILL.md` rubric or `WCM_STYLE_PROFILE.md`
4. Re-test

The skill is a living document. It gets better with real data.

---

_West Coast Modern. Architecture, not real estate._
