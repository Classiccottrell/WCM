# Installation Instructions
## WCM Hero Image Selector Skill

---

## Overview

There are three ways to use the hero skill:

| Mode | What it is | Best for |
|---|---|---|
| **Manual — claude.ai** | Upload photos directly to claude.ai, paste the SKILL.md, run | Mica doing ad-hoc selections from any device |
| **Manual — Claude Cowork** | Point Claude at a local folder on your Mac; no uploading required | Trent reviewing a fresh shoot directly from his machine |
| **Automated — Make.com + Claude API** | Triggered by Dropbox upload, runs headlessly, posts result to Slack | Production pipeline without manual steps |

Start with one of the manual modes. Add Automated Mode once the workflow is validated.

---

## MODE 1 — Manual (claude.ai)
### No setup required. Ready in 5 minutes.

**Best for:** Mica running a selection session from any device, or when photos are already in Google Drive or Dropbox.

### Step 1: Get Claude access
- Mica needs a claude.ai account (Pro plan recommended for larger image batches)
- URL: https://claude.ai

### Step 2: Load the skill
Before uploading any photos, paste the full contents of `SKILL.md` into Claude with this prompt:

```
I'm going to run a hero image selection session for West Coast Modern.
Here are your instructions:

[PASTE FULL CONTENTS OF SKILL.md HERE]

Ready to receive photos.
```

### Step 3: (Optional but recommended) Load taste reference
If Trent has completed the `TASTE_REFERENCE_TEMPLATE.md`, paste it next:

```
Here is the taste reference for this skill:

[PASTE FULL CONTENTS OF COMPLETED TASTE_REFERENCE_TEMPLATE.md HERE]
```

### Step 4: Upload photos and run
```
Property: [House Name]
Hook: [One sentence about what makes this property unique]
Target: [MLS | Instagram | Email | Feature Story | All]

[UPLOAD PHOTOS — drag and drop up to 20 at a time]

Run the hero selection.
```

### Step 5: Review and confirm
Claude will output the Hero Report. Mica reviews it, confirms the hero pick, and flags anything for Trent. Trent does final sign-off.

### Tips for Manual Mode (claude.ai)
- Upload 20–30 photos at a time for best results
- If you have 200+ photos, do a first pass to pull the top 40–50 exteriors, then run the skill on those
- Always include the property name — it improves output formatting and file references
- Save the Hero Report as a Google Doc in the property folder

---

## MODE 2 — Manual (Claude Cowork + Local Folder)
### No uploads required. Works directly from your Mac. ~2 minutes to start.

**Best for:** Trent reviewing a fresh shoot from his local machine without uploading hundreds of photos. Cowork can read files from a local folder path, so the photos stay where they are.

### What is Claude Cowork?
Claude Cowork is a desktop application that gives Claude direct access to files on your computer. Instead of uploading photos one by one, you point Claude at a folder and it reads the images directly. This is the fastest manual option for large shoots.

### Step 1: Install and open Claude Cowork
- Download the Cowork desktop app if you haven't already
- Sign in with your Anthropic / claude.ai account (Pro plan required)
- Open a new Cowork session

### Step 2: Organize your photos locally
Before running the skill, make sure your photos are in a single folder on your Mac. The standard location is:

```
/Users/[yourname]/Dropbox/WCM/[PropertyName]/photography/raw/
```

Or wherever James has synced the shoot. Any local folder path works.

### Step 3: Load the skill
Paste the full contents of `SKILL.md` into the Cowork session, the same as Mode 1:

```
I'm going to run a hero image selection session for West Coast Modern.
Here are your instructions:

[PASTE FULL CONTENTS OF SKILL.md HERE]

Ready to begin.
```

### Step 4: Point Claude at the folder
Instead of uploading photos, give Claude the local path:

```
Property: [House Name]
Hook: [One sentence about what makes this property unique]
Target: [MLS | Instagram | Email | Feature Story | All]

Photos are in this folder on my Mac:
/Users/[yourname]/Dropbox/WCM/[PropertyName]/photography/raw/

Please read all images in that folder and run the hero selection.
```

Claude Cowork will read the images directly from that path without you uploading anything.

### Step 5: Review and confirm
Claude outputs the Hero Report in the Cowork session. You can ask follow-up questions, request score breakdowns, or ask Claude to compare two specific candidates. When you're done, copy the report and save it to Google Drive.

### Tips for Cowork Mode
- If the folder has 200+ images, you can ask Claude to do a first pass on exteriors only: *"Start with just the exterior shots and give me the top 10 before we go further"*
- You can ask Claude to display the shortlisted images side by side for comparison
- The session stays active — you can have a back-and-forth with Claude about specific images before confirming the hero
- Paste the completed `TASTE_REFERENCE_TEMPLATE.md` at the start of the session for best results

---

## MODE 3 — Automated (Make.com + Claude API)
### Full pipeline. Requires API access and Make.com setup. ~2–3 hours to configure.

See the separate document: **`MAKE_AUTOMATION_SETUP.md`**

This document covers the complete step-by-step Make.com scenario configuration, including the Dropbox trigger, image aggregation, Claude API payload, Google Drive output, and Slack notification.

### Prerequisites (check these before starting):
- [ ] Anthropic API key (create at console.anthropic.com — Trent's account)
- [ ] Make.com account (create at make.com — free tier covers ~10 properties/month)
- [ ] Dropbox account with WCM folder structure in place
- [ ] Slack workspace with `#photo-curation` channel created
- [ ] Google Drive folder structure set up (see Folder Structure below)

---

## Folder Structure (Dropbox)

Set this up before configuring any automated mode:

```
/WCM/
  /[PropertyName]/
    /photography/
      /raw/           ← Photographer uploads here (Make.com watches this)
      /curated/       ← Agent outputs hero report here
      /final/         ← Mica/Trent place approved selects here
      /sets/
        /mls/
        /email/
        /instagram/
        /website/
```

---

## Who Does What

| Person | Role in this workflow |
|---|---|
| **Trent** | Completes TASTE_REFERENCE_TEMPLATE.md; runs Cowork sessions; final hero sign-off |
| **Mica** | Runs the skill (manual or automated); reviews reports; confirms selects before Trent |
| **James (Photographer)** | Uploads to Dropbox `/raw/` folder by deadline |
| **Philippe** | Receives confirmed hero list for copy pairing |
| **Jacob** | Receives confirmed hero list for B-roll pairing |

---

## Files in This Repo

```
/
├── SKILL.md                      ← Core skill instructions (v2.0)
├── AGENT.md                      ← Agent identity and capabilities
├── TASTE_REFERENCE_TEMPLATE.md   ← Trent fills this out (10 good + 10 not-hero)
├── WCM_STYLE_PROFILE.md          ← Brand aesthetic extraction
├── INSTALL.md                    ← This file
├── MAKE_AUTOMATION_SETUP.md      ← Detailed Make.com configuration guide
└── README.md                     ← Git repo overview
```

---

## Support

If Claude's selections feel off, the fastest fix is more taste reference examples from Trent.
Each new example in `TASTE_REFERENCE_TEMPLATE.md` meaningfully improves output quality.