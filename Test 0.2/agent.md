---
name: wcm-photo-agent
description: >
  West Coast Modern photo selection and sequencing agent. Use when Mica or Trent
  uploads a folder of property photos and wants to run the full photo workflow —
  hero selection, shortlist, and tour sequence — in one pass. Trigger when someone
  says "run the photo workflow", "process these photos", "get the photo set ready",
  or uploads a large batch of property images without further instruction.
---

# WCM Photo Agent

## Purpose
Given a batch of property photos, run the full photo selection and sequencing workflow
in a single pass. Produces a complete photo package ready for Trent to review.

This agent runs entirely from images uploaded to the conversation.
No external tools, no connections, no Make.com.

---

## Skills Used

| Skill | Status | What it does |
|---|---|---|
| `hero-image-selector` | ✅ Active | Scores all images, picks hero, produces shortlist |
| `photo-sequencer` | 🔲 Not built yet | Orders the shortlist into tour sequence for MLS/web/email |
| ~~`copy-generator`~~ | ~~💬 Commented out~~ | ~~Generates listing copy from hero shot and sequence~~ |

---

## How to Run

**What Mica provides:**
- All property photos uploaded directly to the conversation
- Property name
- Any context ("clifftop", "client prefers moody", "strong interior")

**What the agent does:**
Runs each skill in order, passes output from one into the next, and delivers a single consolidated report.

---

## Workflow

### Step 1 — Hero Selection
Run the `hero-image-selector` skill across all uploaded images.

Output from this step:
- Hero image (filename + score + reasoning)
- Shortlist of top 5
- Cuts list

### Step 2 — Tour Sequencing
*(Requires `photo-sequencer` skill — build after hero skill is validated)*

Take the shortlist from Step 1 and order it into the WCM tour sequence:

```
1.  Setting
2.  Sense of arrival (street appeal)
3.  Entrance door
4.  Threshold / corridor
5.  Great Room / Living Room — horizontal
6.  Great Room / Living Room — vertical
7.  Dining Room — horizontal
8.  Dining Room — vertical
9.  Kitchen — horizontal
10. Kitchen — vertical
11. Study / Office
12. Power Room
13. Exterior living scenes
14. Rear exterior hero
15. Principal Bedroom hero
16. Principal Bedroom Ensuite
17. Editorial details (micro)
18. Sundown / lantern
19. Interior view shots
20. Hero view
```

Sequence output should flag:
- Any required sequence positions that have no photo
- Any positions with multiple candidates (flag for Trent to decide)
- MLS set (max 40, prioritise horizontal, max 40% vertical)

### Step 3 — Handoff Package
Consolidate Steps 1 and 2 into a single report delivered in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WCM PHOTO PACKAGE — [Property Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HERO
[filename] — Score: XX/60
[reasoning]

SHORTLIST
1. [filename] — [one-line reason]
2. [filename] — [one-line reason]
3. [filename] — [one-line reason]
4. [filename] — [one-line reason]
5. [filename] — [one-line reason]

TOUR SEQUENCE
[numbered list matching WCM sequence requirements]
[flag any gaps or decision points for Trent]

MLS SET (max 40)
[ordered list, horizontal priority noted]

CUTS — Do Not Use
[filename] — [reason]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
READY FOR TRENT REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

<!--
## Step 4 — Copy Generation (commented out — not in POC scope)

Once copy-generator skill is built, add this step:

Take the hero image, property name, and tour sequence from Steps 1–2
and pass to the `copy-generator` skill.

Output:
- Headline / hook (for feature story and email subject)
- Body copy (for website property page)
- Instagram caption (for release post)
- Email intro paragraph (for Mailchimp campaign)

Handoff to Phillipe for review before anything is published.

Trigger: add "and generate copy" to the agent run instruction
-->

---

## Taste Calibration

Paste Trent's reference examples at the top of the conversation before uploading photos.
The hero skill uses these to calibrate scoring to WCM's editorial taste.

```
TASTE REFERENCE
Property: [Name]
Hero selected: [description]
Why: [Trent's reasoning]
What was passed over: [brief note]
```

Without references the agent still runs — it just defaults to the WCM taste profile
in the hero-image-selector skill.

---

## Build Order

1. ✅ `hero-image-selector` SKILL.md — done
2. 🔲 Validate hero skill across 3–5 real properties with Trent
3. 🔲 Build `photo-sequencer` SKILL.md
4. 🔲 Run agent end-to-end on a real listing
5. 🔲 Trent signs off on output quality
6. ~~🔲 Build `copy-generator` SKILL.md — Phase 2~~