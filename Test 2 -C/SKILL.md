---
name: hero-image-selector
description: >
  Select the single best hero image from a batch of real estate property photos for West Coast Modern.
  Use this skill whenever someone uploads multiple property photos and wants to identify the hero shot,
  narrow down a large photo set, score images for editorial quality, or sequence photos for a listing.
  Trigger even if the user just says "pick the best one", "which photo leads?", "help me cut these down",
  or drops a folder of images without explanation. No external tools or connections required — works
  entirely from images uploaded directly to the conversation.
---

# Hero Image Selector — West Coast Modern

## Purpose
Given a batch of uploaded property photos, identify the single best **hero image** and a ranked shortlist.
A hero image is the first image a buyer sees — it sets the emotional tone for the entire listing.

This skill runs entirely from images uploaded to the conversation. No integrations, no external tools, no connections.

---

## How to Run This Skill

**What the user provides:**
- A batch of images uploaded directly to the conversation (20–50 at a time is ideal)
- Optionally: property name and any context ("clifftop home", "client wants moody", "this is a tight set")

**What Claude does:**
1. Reviews every uploaded image
2. Scores each against the rubric below
3. Outputs a structured report: hero pick, shortlist, gallery sequence, and cuts

No setup needed. Upload images and ask.

---

## West Coast Modern Taste Profile

These are the editorial values WCM selects for. Score every image against these.

### What makes a strong hero
- **Architecture is the subject** — the building reads clearly, not cropped or obscured
- **Natural light** — golden hour, overcast diffused, or crisp morning light preferred
- **West Coast materiality visible** — wood, concrete, glass, stone, natural landscaping
- **Breathing room** — sky, treeline, or landscape gives the property context and scale
- **Emotional mood** — warmth, calm, aspiration; not clinical or transactional
- **Clean foreground** — no cars, bins, clutter, or construction unless intentional
- **Horizontal format** — wide compositions read better as hero and thumbnail

### What disqualifies a hero
- Interior shots (supporting content only, never hero)
- Overexposed or underexposed
- Heavy lens distortion without artistic intent
- Cluttered or distracting foreground
- Poor weather that reads bleak rather than moody
- Detail shots (fixtures, finishes) — these are supporting content

---

## Scoring Rubric

Score each image 1–10 per dimension:

| Dimension | What to assess |
|---|---|
| **Architecture clarity** | Is the building the clear subject? Does it read well at thumbnail size? |
| **Light quality** | Is the lighting flattering, natural, directional? |
| **Composition** | Rule of thirds, leading lines, breathing room, horizon placement |
| **Emotional resonance** | Does this make someone stop scrolling? |
| **Brand fit** | Does it feel like West Coast Modern — warm, editorial, luxury? |
| **Technical quality** | Sharp focus, correct exposure, no blown highlights |

**Total score = sum of 6 dimensions (max 60)**

---

## Output Format

Always produce output in this exact structure:

```
PROPERTY: [Name if provided, otherwise "Untitled"]
IMAGES REVIEWED: [count]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERO RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image: [filename or number]
Score: XX/60
Why it's the hero:
[2–3 sentences using WCM taste language — light, materiality, mood, composition]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHORTLIST (top 5 for gallery/carousel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [filename] — Score: XX/60 — [one-line reason]
2. [filename] — Score: XX/60 — [one-line reason]
3. [filename] — Score: XX/60 — [one-line reason]
4. [filename] — Score: XX/60 — [one-line reason]
5. [filename] — Score: XX/60 — [one-line reason]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUGGESTED GALLERY SEQUENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Ordered list with one-line note on narrative flow]
e.g. "Start wide exterior → approach/entry → living spaces → outdoor/view → detail"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUTS — Do Not Use
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[filename] — [one-line reason]
[filename] — [one-line reason]
...
```

---

## Scoring Process

**Step 1 — Full scan first**
Review every uploaded image before scoring anything. Calibrate to the range — what's the ceiling and floor of this set?

**Step 2 — Score individually**
Apply the rubric to each. Be honest about weaknesses. Exceptional emotional resonance can outweigh a lower technical score.

**Step 3 — Compare the top candidates**
When 2–3 images are close, ask: *which one would make someone stop scrolling on Instagram?* That's the hero.

**Step 4 — Output the report**
Hero first with full reasoning, then shortlist, sequence, cuts.

---

## Edge Cases

- **All interiors**: Flag it — a hero needs an exterior. Ask if exterior shots exist.
- **Drone vs ground level**: Drone works for strong site context (ocean, acreage). Ground-level works for architectural detail homes.
- **Night / dusk shots**: Can be heroes if mood is exceptional — score high on emotional resonance, but note tradeoffs for email/thumbnail use.
- **Multiple structures**: Pick the image that best represents the *experience* of the property, not necessarily the main building.
- **No clear winner**: Say so. Flag the top 2 as a toss-up and explain what each prioritizes.

---

## Taste Calibration (Optional but Recommended)

For highest accuracy, paste Trent's reference examples before uploading photos:

```
TASTE REFERENCE
Property: [Name]
Hero selected: [description of image]
Why: [Trent's reasoning]
What was passed over: [brief note]
```

10 examples = well-calibrated output. Even 3–4 helps significantly.
Without examples, the skill defaults to the WCM taste profile above.
