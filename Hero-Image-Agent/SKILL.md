---
name: hero-image-selector
version: 2.1
author: West Coast Modern
description: >
  Select the best hero image(s) from a batch of real estate property photos for West Coast Modern.
  Use this skill whenever someone uploads multiple property photos and wants to identify the hero shot,
  narrow down a large photo set, score images for editorial quality, or sequence photos for a listing.
  Trigger even if the user just says "pick the best one", "which photo leads?", "help me cut these down",
  or drops a folder of images without explanation.
---

# Hero Image Selector Skill
## West Coast Modern — Property Photography Curation

---

## Purpose

Given a batch of property photos (uploaded directly or referenced by path), identify:
1. **The Hero** — single best image to lead the listing, email, and Instagram
2. **Hero Vertical Alternative** — best vertical crop or vertical-native photo for Instagram/email
3. **Hero 2** — second-best thumbnail option (backup)
4. **Shortlist** — top 5–8 for gallery and tour sequence
5. **Cuts** — images to discard with brief reason

This skill is designed to take Trent from 200+ photos → 50 reviewed → 5 hero candidates in one pass.

---

## Inputs

**Required:**
- A folder of images, OR images uploaded directly to the conversation

**Optional but recommended:**
- Property name (e.g. "Floating House", "Totem House")
- Property hook or story angle (e.g. "the totems are the story — try to hero one that shows them")
- Trent's taste reference document (paste contents of `TASTE_REFERENCE_TEMPLATE.md` if available)
- Delivery target: `MLS` | `Instagram` | `Email` | `Feature Story` | `All`

**If taste reference is not provided:** the skill defaults to the WCM Taste Profile below.

---

## WCM Taste Profile

These editorial values define what West Coast Modern selects for. This is the default calibration.

### What makes a strong EXTERIOR hero

1. **Architecture is the subject** — the building reads clearly, not cropped or obscured; full personality visible
2. **Natural, directional light** — golden hour, crisp morning, or atmospheric overcast; not flat midday
3. **West Coast materiality** — wood, concrete, glass, stone, and natural landscaping are visible
4. **Breathing room** — sky, treeline, ocean, or hillside gives context and scale
5. **Cinematic or atmospheric mood** — warmth, calm, aspiration; not clinical or transactional
6. **Clean foreground** — no cars, bins, construction, or clutter unless architecturally intentional
7. **Horizontal format preferred** — wide compositions read best as hero and thumbnail
8. **Tells the hook** — if the property has a defining story (totems, cantilevered over ocean, etc.), the hero should show it
9. **Reads at thumbnail** — test mentally: does this image work as a 400x300px thumbnail on a phone screen?

### What makes a strong INTERIOR hero

> Note: Interior heroes are only selected when no strong exterior exists. Flag this if it happens.

1. Great room or principal space — the most architectural room in the house
2. Natural light flooding in — interior shots live or die by window light
3. A clear sense of spatial depth and scale
4. Furniture and styling must be immaculate — any clutter disqualifies

### Automatic disqualifiers for hero role

- Overexposed or underexposed beyond recovery
- Heavy lens distortion without artistic intent
- Cluttered or busy foreground (cars, bins, staging props)
- Closed doors or blocked entries
- Bleak weather that reads depressing (not the same as moody — moody is intentional)
- Close-in detail shots (fixtures, handles, tile) — these are supporting content
- Interior-only shots when exterior exists
- Drone shots that are so high the house is a speck

---

## Scoring Rubric

Score each candidate image 1–10 per dimension:

| Dimension | What to assess |
|---|---|
| **Architecture clarity** | Does the building read clearly as the subject? Does it work at thumbnail size? |
| **Light quality** | Is the lighting flattering, natural, directional? No flat midday light? |
| **Composition** | Rule of thirds, leading lines, breathing room, horizon placement, clean foreground |
| **Emotional resonance** | Does this make someone stop scrolling? Does it create aspiration? |
| **Brand fit** | Does it feel like WCM — warm, editorial, design-forward, luxury without pretension? |
| **Technical quality** | Sharp focus, correct exposure, no blown highlights, clean color |

**Total score = sum of 6 dimensions (max 60)**

Tiebreaker question: *Which image would make someone stop scrolling on Instagram at 7am on a Tuesday?* That's the hero.

---

## Selection Process (Step by Step)

**Step 1 — Full scan, no scoring yet**
Review every image in the batch. Calibrate to the range. What's the ceiling? What's the floor? Note obvious disqualifiers.

**Step 2 — Identify exterior candidates**
Pull all exterior shots. These are the hero pool. Note any with unique architectural features or story hooks.

**Step 3 — Score each exterior candidate**
Apply the rubric. Be honest about weaknesses. Exceptional emotional resonance can outweigh a lower technical score.

**Step 4 — Compare top 3**
When 2–3 images are close, use the tiebreaker. The hero is the one that performs best as a single image with no context.

**Step 5 — Select vertical hero**
From the same exterior pool, find the best vertical composition. Can be a vertical-native shot or a vertical crop of the hero. Must work for Instagram Stories and email.

**Step 6 — Select Hero 2**
Second-best thumbnail option. Should feel distinct from Hero 1 — different angle or moment, not just a slight variation.

**Step 7 — Build shortlist**
Top 5–8 for gallery/tour sequence use. These feed the MLS and Instagram carousel.

**Step 8 — Output the report (in-chat)**
Produce the ASCII report in the structure under "## Output Format" below.

**Step 9 — Write the styled HTML artifact (always)**
Write `hero_report.html` into the property folder using the template in "## Required Artifact — Styled HTML Report". Mandatory — never skip, even on a Rush run.

---

## Output Format

Always produce output in this exact structure:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERO IMAGE SELECTION REPORT
Property: [Name or "Untitled"]
Images reviewed: [count]
Date: [today]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HERO (Primary — Horizontal)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image: [filename or number]
Score: XX/60
Breakdown: Architecture X | Light X | Composition X | Resonance X | Brand X | Technical X
Why it's the hero:
[2–4 sentences in WCM voice — light, materiality, mood, composition, story hook]
Use for: Website hero, Email header, MLS image 1, Instagram feed (cropped), Feature Story

HERO VERTICAL ALTERNATIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image: [filename or number]
Score: XX/60
Notes: [One sentence on what makes this the best vertical option]
Use for: Instagram Stories, Email verticals, Instagram carousel cover

HERO 2 (Backup / Second Lead)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image: [filename or number]
Score: XX/60
Notes: [One sentence — what angle or moment this offers that's different from Hero 1]
Use for: Second email campaign, Instagram second post, A/B test option

SHORTLIST (Gallery & Tour Sequence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [filename] — XX/60 — [one-line reason + suggested sequence position]
2. [filename] — XX/60 — [one-line reason + suggested sequence position]
3. [filename] — XX/60 — [one-line reason + suggested sequence position]
4. [filename] — XX/60 — [one-line reason + suggested sequence position]
5. [filename] — XX/60 — [one-line reason + suggested sequence position]

SUGGESTED TOUR SEQUENCE (MLS / Website)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Ordered list following WCM sequence: Setting → Arrival → Entry → Great Room → Dining → Kitchen → ...]
e.g.
1. [filename] — Setting / establishing exterior
2. [filename] — Sense of arrival / street appeal
3. [filename] — Entry / threshold
...

CUTS — Do Not Use for Hero or Gallery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[filename] — [one-line reason — be specific]
[filename] — [one-line reason]
...

FLAGS / NOTES FOR TRENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Any edge cases, close calls, or questions that warrant Trent's eye]
```

---

## Required Artifact — Styled HTML Report (always produce)

After producing the in-chat report, you **MUST** write a file named `hero_report.html` into the property folder — the same folder the photos came from. If the photos were uploaded rather than read from a folder, write it into the session working directory. This makes the report show up in Cowork as a file the user can open. Never skip this, even on a Rush run.

Fill the template below with the report content, then end your turn by telling the user:

> Styled report written to `hero_report.html` — open it in your browser and use File → Print → Save as PDF for a shareable PDF.

### Mapping the in-chat report into the template

- **Masthead** — property name → `{{PROPERTY}}`, today's date → `{{DATE}}`, image count → `{{IMAGE_COUNT}}`.
- **HERO / HERO VERTICAL / HERO 2** — each becomes a `<section class="section-block">` with the big `.score-display` (score `{{HERO_SCORE}}` etc.) and the 6-dimension `.breakdown` bars (one `.dim` per dimension; set each `.dim-fill` width to `score/10*100%` and the `.dim-val` to the 1–10 value). Put the filename in an `.image-ref`, the "Why / Notes" copy in `.body-text`, and the "Use for" line in `.use-for`.
- **SHORTLIST** and **SUGGESTED TOUR SEQUENCE** — render as `.report-list` ordered lists (`<ol>`), one `<li>` per entry.
- **CUTS** — render as a `.report-list` list.
- **FLAGS / NOTES FOR TRENT** — render each as a `.flag-item` block.
- **Triage** — there is no triage `<section>` in this template. If a full per-image triage isn't available in a manual run, that's expected — omit it entirely (it's optional for Mode 2).

### Template (self-contained — copy, fill, write to `hero_report.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Hero Report — {{PROPERTY}}</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --primary: oklch(0.508 0.118 165.612);
  --primary-foreground: oklch(0.979 0.021 166.113);
  --secondary: oklch(0.967 0.001 286.375);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --radius: 0;
  /* WCM additions */
  --score-high: oklch(0.65 0.15 145);
  --score-mid: var(--primary);
  --score-low: var(--muted-foreground);
  --serif: 'Palatino Linotype','Book Antiqua',Palatino,Georgia,serif;
  --mono: 'SF Mono','Fira Code',monospace;
}

body{background:var(--background);color:var(--foreground);
  font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;
  font-size:15px;line-height:1.7}
.masthead{background:var(--card);border-bottom:1px solid var(--border);padding:48px 64px 36px}
.wordmark{font-size:10px;letter-spacing:.28em;text-transform:uppercase;
  color:var(--primary);margin-bottom:18px}
.masthead h1{font-family:var(--serif);font-size:34px;font-weight:normal;
  letter-spacing:-.01em;line-height:1.2;margin-bottom:10px}
.masthead-meta{font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted-foreground)}
.masthead-meta span{margin-right:24px}
.report-body{max-width:860px;margin:0 auto;padding:48px 64px}
.sep{border-top:1px solid var(--border);margin:28px 0}
h2.section-head{font-size:10px;font-weight:600;letter-spacing:.22em;
  text-transform:uppercase;color:var(--primary);margin:36px 0 12px}
.score-display{margin:8px 0 12px}
.score-num{font-family:var(--serif);font-size:50px;font-weight:normal;line-height:1}
.score-denom{font-family:var(--serif);font-size:20px;color:var(--muted-foreground)}
.breakdown{display:flex;flex-wrap:wrap;gap:10px 20px;margin:12px 0 20px;
  padding:16px 20px;background:var(--card);border:1px solid var(--border)}
.dim{display:flex;align-items:center;gap:8px;font-size:12px;min-width:170px}
.dim-lbl{color:var(--muted-foreground);width:120px;flex-shrink:0}
.dim-bar{flex:1;height:3px;background:var(--border);min-width:60px}
.dim-fill{height:100%;background:var(--primary)}
.dim-val{color:var(--foreground);width:14px;text-align:right}
.image-ref{font-family:var(--mono);font-size:13px;color:var(--primary);
  background:var(--card);display:inline-block;padding:4px 10px;
  border:1px solid var(--border);margin:4px 0 0}
.use-for{font-size:13px;color:var(--muted-foreground);margin:8px 0 16px}
.use-for em{font-style:normal;color:var(--foreground)}
.body-text{color:var(--foreground);margin:10px 0;max-width:680px}
.report-list{margin:10px 0 10px 20px}
.report-list li{margin:6px 0}
.flag-item{margin:12px 0;padding:12px 16px;border-left:2px solid var(--primary);
  background:color-mix(in oklch,var(--primary) 8%,transparent);
  font-size:14px;max-width:680px}
.report-footer{margin-top:80px;padding-top:20px;border-top:1px solid var(--border);
  font-size:11px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted-foreground);opacity:0.4}

@page{margin:18mm}
@media print{body{font-size:12px}.masthead{padding:32px 0 24px}.report-body{padding:24px 0}.section-block{break-inside:avoid}.breakdown{break-inside:avoid}}
</style>
</head>
<body>
<header class="masthead">
  <div class="wordmark">West Coast Modern</div>
  <h1>Hero Image Report</h1>
  <div class="masthead-meta">
    <span>{{PROPERTY}}</span>
    <span>{{DATE}}</span>
    <span>{{IMAGE_COUNT}} images reviewed</span>
  </div>
</header>
<main class="report-body">

  <section class="section-block">
    <h2 class="section-head">Hero — Primary (Horizontal)</h2>
    <div class="image-ref">{{HERO_IMAGE}}</div>
    <div class="score-display"><span class="score-num">{{HERO_SCORE}}</span><span class="score-denom">/60</span></div>
    <div class="breakdown">
      <div class="dim"><span class="dim-lbl">Architecture</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO_ARCH_PCT}}%"></span></span><span class="dim-val">{{HERO_ARCH}}</span></div>
      <div class="dim"><span class="dim-lbl">Light</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO_LIGHT_PCT}}%"></span></span><span class="dim-val">{{HERO_LIGHT}}</span></div>
      <div class="dim"><span class="dim-lbl">Composition</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO_COMP_PCT}}%"></span></span><span class="dim-val">{{HERO_COMP}}</span></div>
      <div class="dim"><span class="dim-lbl">Resonance</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO_RES_PCT}}%"></span></span><span class="dim-val">{{HERO_RES}}</span></div>
      <div class="dim"><span class="dim-lbl">Brand fit</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO_BRAND_PCT}}%"></span></span><span class="dim-val">{{HERO_BRAND}}</span></div>
      <div class="dim"><span class="dim-lbl">Technical</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO_TECH_PCT}}%"></span></span><span class="dim-val">{{HERO_TECH}}</span></div>
    </div>
    <p class="body-text">{{HERO_WHY}}</p>
    <p class="use-for">Use for: <em>{{HERO_USE_FOR}}</em></p>
  </section>

  <div class="sep"></div>

  <section class="section-block">
    <h2 class="section-head">Hero Vertical Alternative</h2>
    <div class="image-ref">{{VERT_IMAGE}}</div>
    <div class="score-display"><span class="score-num">{{VERT_SCORE}}</span><span class="score-denom">/60</span></div>
    <div class="breakdown">
      <div class="dim"><span class="dim-lbl">Architecture</span><span class="dim-bar"><span class="dim-fill" style="width:{{VERT_ARCH_PCT}}%"></span></span><span class="dim-val">{{VERT_ARCH}}</span></div>
      <div class="dim"><span class="dim-lbl">Light</span><span class="dim-bar"><span class="dim-fill" style="width:{{VERT_LIGHT_PCT}}%"></span></span><span class="dim-val">{{VERT_LIGHT}}</span></div>
      <div class="dim"><span class="dim-lbl">Composition</span><span class="dim-bar"><span class="dim-fill" style="width:{{VERT_COMP_PCT}}%"></span></span><span class="dim-val">{{VERT_COMP}}</span></div>
      <div class="dim"><span class="dim-lbl">Resonance</span><span class="dim-bar"><span class="dim-fill" style="width:{{VERT_RES_PCT}}%"></span></span><span class="dim-val">{{VERT_RES}}</span></div>
      <div class="dim"><span class="dim-lbl">Brand fit</span><span class="dim-bar"><span class="dim-fill" style="width:{{VERT_BRAND_PCT}}%"></span></span><span class="dim-val">{{VERT_BRAND}}</span></div>
      <div class="dim"><span class="dim-lbl">Technical</span><span class="dim-bar"><span class="dim-fill" style="width:{{VERT_TECH_PCT}}%"></span></span><span class="dim-val">{{VERT_TECH}}</span></div>
    </div>
    <p class="body-text">{{VERT_NOTES}}</p>
    <p class="use-for">Use for: <em>{{VERT_USE_FOR}}</em></p>
  </section>

  <div class="sep"></div>

  <section class="section-block">
    <h2 class="section-head">Hero 2 — Backup / Second Lead</h2>
    <div class="image-ref">{{HERO2_IMAGE}}</div>
    <div class="score-display"><span class="score-num">{{HERO2_SCORE}}</span><span class="score-denom">/60</span></div>
    <div class="breakdown">
      <div class="dim"><span class="dim-lbl">Architecture</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO2_ARCH_PCT}}%"></span></span><span class="dim-val">{{HERO2_ARCH}}</span></div>
      <div class="dim"><span class="dim-lbl">Light</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO2_LIGHT_PCT}}%"></span></span><span class="dim-val">{{HERO2_LIGHT}}</span></div>
      <div class="dim"><span class="dim-lbl">Composition</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO2_COMP_PCT}}%"></span></span><span class="dim-val">{{HERO2_COMP}}</span></div>
      <div class="dim"><span class="dim-lbl">Resonance</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO2_RES_PCT}}%"></span></span><span class="dim-val">{{HERO2_RES}}</span></div>
      <div class="dim"><span class="dim-lbl">Brand fit</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO2_BRAND_PCT}}%"></span></span><span class="dim-val">{{HERO2_BRAND}}</span></div>
      <div class="dim"><span class="dim-lbl">Technical</span><span class="dim-bar"><span class="dim-fill" style="width:{{HERO2_TECH_PCT}}%"></span></span><span class="dim-val">{{HERO2_TECH}}</span></div>
    </div>
    <p class="body-text">{{HERO2_NOTES}}</p>
    <p class="use-for">Use for: <em>{{HERO2_USE_FOR}}</em></p>
  </section>

  <div class="sep"></div>

  <h2 class="section-head">Shortlist — Gallery &amp; Tour Sequence</h2>
  <ol class="report-list">
    {{SHORTLIST_ITEMS}}
  </ol>

  <h2 class="section-head">Suggested Tour Sequence</h2>
  <ol class="report-list">
    {{TOUR_ITEMS}}
  </ol>

  <h2 class="section-head">Cuts — Do Not Use for Hero or Gallery</h2>
  <ul class="report-list">
    {{CUTS_ITEMS}}
  </ul>

  <h2 class="section-head">Flags / Notes for Trent</h2>
  {{FLAG_ITEMS}}

  <footer class="report-footer">West Coast Modern — Architecture, not real estate.</footer>
</main>
</body>
</html>
```

---

## Edge Cases

| Situation | How to handle |
|---|---|
| **No exterior shots** | Flag loudly. Ask if exteriors exist. If not, select best interior with full caveat. |
| **Drone vs ground level** | Drone works for site context (ocean, acreage, landscape). Ground works for architectural detail. Choose by which shows the hook better. |
| **Dusk / night shots** | Can hero if mood is exceptional. Flag that these may perform differently in email (dark thumbails). |
| **Multiple structures / complex sites** | Pick the image that best represents the *experience* of owning this property. |
| **No clear winner (two images tied)** | Say so explicitly. Present both as a toss-up and explain what each prioritizes. Let Trent decide. |
| **Property has a story hook** | Prioritize showing the hook in the hero. Note if no images capture it. |
| **Vertical-only set** | Select best vertical, flag the format gap, suggest it may need a crop to horizontal for web. |

---

## Taste Calibration (Paste Before Running)

For highest accuracy, paste Trent's completed `TASTE_REFERENCE_TEMPLATE.md` before uploading photos.

```
TASTE REFERENCE — [Property Name]
Hero selected: [description]
Why it worked: [Trent's words]
What was passed over: [brief note]
```

10 examples = well-calibrated. Even 3–4 helps significantly.
Without examples, defaults to the WCM Taste Profile above.

---

## Delivery Formats Served by This Skill

| Deliverable | Images needed | Hero role |
|---|---|---|
| Website listing page | 1 horizontal hero | Primary |
| MLS | Up to 40, hero first | Image 1 |
| Email 1 (House Release) | 6 verticals | First vertical |
| Email 2 (Tour Announcement) | 5 verticals + 1 horizontal | Horizontal header |
| Instagram Release Post | 10 verticals (carousel) | Cover image |
| Instagram Feed | 3-post grid plan | Lead post |
| Feature Story | 1 horizontal master | Full bleed cover |
