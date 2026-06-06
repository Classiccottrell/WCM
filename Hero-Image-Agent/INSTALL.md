# Installation Instructions
## WCM Hero Image Selector Skill

---

## Overview

There are two ways to use the hero skill:

| Mode | What it is | Best for |
|---|---|---|
| **Manual (Claude.ai)** | Upload photos directly to claude.ai, paste the SKILL.md, run | Trent or Mica doing ad-hoc selections |
| **Automated (Make.com + Claude API)** | Triggered by Dropbox upload, runs headlessly, posts result to Slack | Production pipeline without manual steps |

Start with Manual Mode. Add Automated Mode once the workflow is validated.

---

## MODE 1 — Manual (Claude.ai)
### No setup required. Ready in 5 minutes.

### Step 1: Get Claude access
- Mica needs a claude.ai account (Pro plan recommended for larger image batches)
- Trent to share the API key or add Mica to the Anthropic workspace
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

### Step 4: Load the style profile (first time only)
Paste `WCM_STYLE_PROFILE.md` on the first session. You don't need to re-paste it every time — just mention "use the WCM style profile" on subsequent runs.

### Step 5: Upload photos and run
```
Property: [House Name]
Hook: [One sentence about what makes this property unique]
Target: [MLS | Instagram | Email | Feature Story | All]

[UPLOAD PHOTOS — drag and drop up to 20 at a time]

Run the hero selection.
```

### Step 6: Review and confirm
Claude will output the Hero Report. Mica reviews it, confirms the hero pick, and flags anything for Trent. Trent does final sign-off.

### Tips for Manual Mode
- Upload 20–30 photos at a time for best results (Claude handles more, but outputs are richer in smaller batches)
- If you have 200+ photos, do a first pass to pull the top 40–50 exteriors, then run the skill on those
- Always include the property name — it improves the output formatting and file references
- Save the Hero Report as a Google Doc in the property folder

---

## MODE 2 — Automated (Make.com + Claude API)
### Full pipeline. Requires API access and Make.com setup. ~2 hours to configure.

### Prerequisites
- [ ] Anthropic API key (Trent to provide / create at console.anthropic.com)
- [ ] Make.com account (create at make.com)
- [ ] Dropbox account with WCM photography folders
- [ ] Slack workspace with #photo-curation channel
- [ ] Google Drive folder structure set up

---

### Architecture

```
Dropbox (new folder trigger)
        ↓
Make.com Scenario
        ↓
List files in folder → Download images → Send to Claude API (vision)
        ↓
Claude runs SKILL.md logic → Returns Hero Report (JSON + markdown)
        ↓
Save hero_report.md to Google Drive → property folder
        ↓
Post summary to Slack #photo-curation
        ↓
Mica reviews → confirms hero → Trent signs off
```

---

### Step-by-Step Make.com Setup

#### Scenario 1: Trigger on new Dropbox folder

1. Open Make.com → Create new scenario
2. **Module 1: Dropbox — Watch for new folder**
   - Connection: Connect your Dropbox account
   - Folder to watch: `/WCM/[season]/photography/`
   - Trigger: New subfolder created
   - This fires when a photographer uploads a new property folder

3. **Module 2: Dropbox — List files in folder**
   - Folder: Use the path from Module 1 output
   - Filter: image files only (`.jpg`, `.jpeg`, `.png`, `.tiff`)
   - Max results: 50 (adjust as needed)

4. **Module 3: Dropbox — Download files**
   - For each file from Module 2
   - Set up as an iterator

5. **Module 4: HTTP — POST to Claude API**
   - URL: `https://api.anthropic.com/v1/messages`
   - Method: POST
   - Headers:
     ```
     x-api-key: [YOUR_ANTHROPIC_API_KEY]
     anthropic-version: 2023-06-01
     content-type: application/json
     ```
   - Body: See API payload below

#### Claude API Payload (paste into Make.com HTTP module body)

```json
{
  "model": "claude-opus-4-5",
  "max_tokens": 4096,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "You are the WCM Photo Curator. Run a full hero image selection using the WCM Hero Image Selector Skill v2.0. Property: {{1.folder_name}}. Analyze all images below and output a complete Hero Report in the standard format."
        },
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "{{3.data}}"
          }
        }
      ]
    }
  ],
  "system": "[PASTE FULL CONTENTS OF SKILL.md HERE AS THE SYSTEM PROMPT]"
}
```

> **Note:** For multiple images, Make.com needs to loop and build the content array. Use an aggregator module before the HTTP call to bundle all image data into one API request.

6. **Module 5: Google Drive — Create file**
   - Destination: `/WCM/[PropertyName]/photography/curated/`
   - Filename: `hero_report_[PropertyName]_[date].md`
   - Content: Claude's response text

7. **Module 6: Slack — Post message**
   - Channel: `#photo-curation`
   - Message:
     ```
     :camera: Hero report ready for *{{folder_name}}*
     
     Hero pick: {{extracted_hero_filename}}
     Score: {{extracted_score}}/60
     
     Review the full report: {{google_drive_link}}
     
     @mica — please review and confirm before sending to Trent
     ```

---

### Folder Structure (Dropbox)

Set this up before configuring Make.com:

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

### Testing the Automation

1. Drop a test folder of 10–15 images into Dropbox raw folder
2. Watch Make.com scenario execute (run manually first)
3. Confirm hero_report.md appears in Google Drive
4. Confirm Slack message posts to #photo-curation
5. Review report quality — compare to what Trent would have picked
6. Iterate on the system prompt (SKILL.md) if results are off

---

### Cost Estimates

| Item | Cost |
|---|---|
| Claude API (claude-opus-4-5, ~50 images per property) | ~$0.50–2.00 per property run |
| Make.com (100 operations per scenario) | Free tier covers ~10 properties/month; paid plan $9/mo covers more |
| Dropbox | Existing subscription |
| Anthropic API | Pay as you go; no subscription needed |

---

## Files in This Repo

```
/
├── SKILL.md                      ← Core skill instructions (v2.0)
├── AGENT.md                      ← Agent identity and capabilities
├── TASTE_REFERENCE_TEMPLATE.md   ← Trent fills this out (10 good + 10 bad)
├── WCM_STYLE_PROFILE.md          ← Brand aesthetic extraction
├── INSTALL.md                    ← This file
└── README.md                     ← Git repo overview
```

---

## Who Does What

| Person | Role in this workflow |
|---|---|
| **Trent** | Completes TASTE_REFERENCE_TEMPLATE.md; final hero sign-off |
| **Mica** | Runs the skill (manual or automated); reviews reports; confirms selects |
| **Phillipe** | Receives confirmed hero list for copy pairing |
| **Jacob** | Receives confirmed hero list for B-roll pairing |
| **Photographer** | Uploads to Dropbox `/raw/` folder by deadline |

---

## Support

If Claude's selections feel off, the fastest fix is more taste reference examples from Trent.
Each new example in `TASTE_REFERENCE_TEMPLATE.md` meaningfully improves output quality.
