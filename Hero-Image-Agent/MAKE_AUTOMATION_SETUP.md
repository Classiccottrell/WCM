# Make.com Automation Setup Guide
## WCM Hero Image Selector — Automated Pipeline
### For Matthew (Implementation Reference)

---

## What This Builds

A fully automated scenario in Make.com that:

1. Detects when a photographer drops a new folder of photos into Dropbox
2. Downloads all images from that folder
3. Bundles them and sends to the Claude API for hero selection
4. Saves the Hero Report as a Markdown file in Google Drive
5. Posts a Slack notification to `#photo-curation` with a link to the report

End result: Mica gets a Slack ping, opens the report in Drive, confirms the hero, sends to Trent. Neither of them touched a folder or uploaded a file.

---

## Before You Start — Prerequisites Checklist

Complete all of these before opening Make.com:

- [ ] **Anthropic API key** — log in at console.anthropic.com (Trent's account), go to API Keys, create a new key. Copy it and store it securely — you won't see it again.
- [ ] **Make.com account** — sign up at make.com. The free tier is fine for initial testing; upgrade to Core ($9/mo) once you go live if you exceed 1,000 operations/month.
- [ ] **Dropbox** — confirm the folder structure exists: `/WCM/[PropertyName]/photography/raw/` is where photographers upload. Make.com needs to watch the parent folder `/WCM/`.
- [ ] **Google Drive folder** — create `/WCM Production/Hero Reports/` — this is where hero_report.md files will be saved.
- [ ] **Slack** — confirm the `#photo-curation` channel exists and you have a Slack account to connect.
- [ ] **SKILL.md content** — have the full text of `SKILL.md` ready to paste. You'll use it as the system prompt in the Claude API call.

---

## Architecture Overview

```
Dropbox: New folder in /WCM/
         ↓
[Module 1] Watch Folder — detect new folder
         ↓
[Module 2] List Files — get all image files in the folder
         ↓
[Module 3] Download — download each image as binary data
         ↓
[Module 4] Aggregator — bundle all image data into one array
         ↓
[Module 5] Claude API (HTTP POST) — send images + SKILL.md prompt
         ↓
[Module 6] Parse response — extract the Hero Report text
         ↓
[Module 7] Google Drive — save hero_report.md to Drive
         ↓
[Module 8] Slack — post notification to #photo-curation
```

Total modules: 8
Estimated Make.com operations per run: ~60–120 (depending on photo count)
At 200 properties/year: well within Core plan limits.

---

## Step-by-Step Configuration

---

### SCENARIO SETUP

1. Log in to make.com
2. Click **Create a new scenario**
3. Name it: `WCM — Hero Image Selector`
4. Save immediately. Come back and save after each module.

---

### MODULE 1 — Dropbox: Watch Folders

This module fires whenever a new subfolder appears inside `/WCM/`.

**Add module:** Search for `Dropbox`, select **Watch Folders**

**Configuration:**
```
Connection:         [Connect your Dropbox account — click Add, follow OAuth flow]
Folder to watch:    /WCM
Watch for:          New folders only
Maximum results:    1
```

**Important notes:**
- Make.com polls Dropbox on a schedule (every 15 minutes on Core plan). This is not instant — there's up to a 15-minute lag between upload and trigger.
- The folder name that triggers this module becomes your `{{1.name}}` variable — use it as the property name throughout the scenario.
- If your Dropbox structure uses seasons or years (e.g. `/WCM/2026/[PropertyName]/`), adjust the watched folder accordingly and update all downstream folder paths.

---

### MODULE 2 — Dropbox: List All Files in a Folder

Lists every file in the newly created property folder.

**Add module:** Dropbox → **List All Files in a Folder**

**Configuration:**
```
Connection:         [Same Dropbox connection]
Folder:             {{1.path_lower}}/photography/raw
File Extensions:    jpg, jpeg, png, tiff, tif
Maximum results:    50
```

**Notes:**
- `{{1.path_lower}}` is the full path of the new folder from Module 1. Make.com fills this in automatically.
- The 50-image limit is intentional — the Claude API has a per-request size limit. If a shoot has more than 50 images, see the **Handling Large Batches** section at the bottom of this document.
- TIFF files are listed here but the API call below will need them sent as JPEG. See Module 3 note.

---

### MODULE 3 — Dropbox: Download a File

Downloads each image file as binary data so it can be base64-encoded and sent to Claude.

**Add module:** Dropbox → **Download a File**

**Configuration:**
```
Connection:         [Same Dropbox connection]
Choose a file:      By path
File path:          {{2.path_lower}}
```

This module runs once per file — Make.com automatically iterates it through every result from Module 2.

**Note on file format:** Claude's API accepts JPEG, PNG, GIF, and WebP. TIFF files must be converted before sending. For now, assume all source files are JPEG. If TIFF becomes an issue, a conversion step can be added using Make.com's built-in image tools or an intermediary service.

---

### MODULE 4 — Array Aggregator

This is the critical step that Make.com beginners most often miss. The Claude API needs all images in a single request — not one request per image. The aggregator collects all the downloaded files from Module 3 and bundles them into one array.

**Add module:** Tools → **Array Aggregator**

**Configuration:**
```
Source module:              Module 3 (Download a File)
Aggregated fields:
  - data:     {{3.data}}          ← The binary image data
  - name:     {{3.name}}          ← The filename (used for reporting)
Target structure type:      Custom
```

After the aggregator runs, you'll have a single array called `{{4.array}}` containing objects like:
```json
[
  { "data": "[base64 binary]", "name": "IMG_0001.jpg" },
  { "data": "[base64 binary]", "name": "IMG_0002.jpg" },
  ...
]
```

**This is what gets sent to Claude in Module 5.**

---

### MODULE 5 — HTTP: POST to Claude API

This is the core AI call. It sends all the images plus the skill instructions to Claude and gets back the Hero Report.

**Add module:** HTTP → **Make a Request**

**Configuration:**

```
URL:            https://api.anthropic.com/v1/messages
Method:         POST
Headers:
  x-api-key:              [YOUR ANTHROPIC API KEY]
  anthropic-version:      2023-06-01
  content-type:           application/json
Body type:      Raw
Content type:   application/json
```

**Request Body:**

This is the most complex part. Use the following JSON structure, pasting it into the Body field. The `{{...}}` variables are filled in by Make.com at runtime.

```json
{
  "model": "claude-opus-4-5",
  "max_tokens": 4096,
  "system": "[PASTE FULL CONTENTS OF SKILL.md HERE — replace this entire string with the SKILL.md text, keeping it inside the quotes]",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Property: {{1.name}}\n\nRun a full hero image selection using the WCM Hero Image Selector Skill. Analyze all images provided and output a complete Hero Report in the standard format. Include scores, reasoning, shortlist, suggested tour sequence, cuts, and flags for Trent."
        }
      ]
    }
  ]
}
```

**Wait — where are the images?**

The images need to be injected into the `content` array alongside the text block. Make.com doesn't natively support building a dynamic JSON array of arbitrary length in a single HTTP module body. You have two options:

**Option A (Recommended for simplicity): Use Make.com's JSON module to build the payload first**

Before Module 5, add a **Tools → Set Variable** module that uses Make.com's `map()` function to build the content array:

1. Add module: **Tools → Set Variable**
   - Variable name: `image_content_array`
   - Variable value: Use the formula builder to map `{{4.array}}` into the Claude content format

This requires Make.com's formula syntax — reach out if you want this built out as a tested formula. The alternative is Option B.

**Option B (Simpler to implement): Send images as a text manifest + separate API call**

Send the first API call with the image filenames as text, then a second HTTP call with the actual image data for the top candidates. This works well when you're doing a two-pass selection (first narrow to 10, then deep score the top 10).

For the POC, **Option B is recommended** as it's more reliable to build and debug. Here's the adjusted body for Option B:

```json
{
  "model": "claude-opus-4-5",
  "max_tokens": 4096,
  "system": "[PASTE SKILL.md CONTENTS HERE]",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Property: {{1.name}}\n\nI am sending you a batch of property photos for hero selection. The filenames are:\n\n{{map(4.array, 'name')}}\n\nPlease confirm receipt and I will send the images now."
        }
      ]
    }
  ]
}
```

Then add a second HTTP module that sends the actual images. Message Matthew directly to build out the multi-turn API call pattern — it's straightforward but requires building a conversation history array.

**For now, configure Module 5 with Option B and flag it for refinement in Phase 3 testing.**

---

### MODULE 6 — Parse the Claude Response

Extract the Hero Report text from the API response.

**Add module:** Tools → **Set Variable**

```
Variable name:   hero_report_text
Variable value:  {{5.data.content[].text}}
```

Make.com will parse the JSON response from Claude. The `content` array contains text blocks — this expression extracts the text from the first (and usually only) text block.

If the response has multiple content blocks (can happen with longer outputs), use:
```
{{join(map(5.data.content; "text"); "\n")}}
```

---

### MODULE 7 — Google Drive: Upload a File

Saves the Hero Report to Google Drive.

**Add module:** Google Drive → **Upload a File**

**Configuration:**
```
Connection:         [Connect your Google account — OAuth flow]
Folder:             /WCM Production/Hero Reports/{{1.name}}/
File name:          hero_report_{{1.name}}_{{formatDate(now; "YYYY-MM-DD")}}.md
File content:       {{6.hero_report_text}}
Convert to Google   No (save as .md file, not Google Doc)
Docs format:
```

**Note:** If the property subfolder doesn't exist yet, toggle **Create a folder if it doesn't exist** to ON.

The file will be named something like: `hero_report_Floating_House_2026-06-15.md`

---

### MODULE 8 — Slack: Create a Message

Posts a notification to `#photo-curation` when the report is ready.

**Add module:** Slack → **Create a Message**

**Configuration:**
```
Connection:     [Connect your Slack workspace — OAuth flow]
Channel:        #photo-curation
Text:
```

Paste this as the message text:
```
:camera: *Hero report ready — {{1.name}}*

The AI has completed its first pass on the photo set.

:link: View full report: {{7.webViewLink}}

@mica — please review the shortlist and confirm the hero before sending to Trent for final sign-off.
```

`{{7.webViewLink}}` is the Google Drive share link returned by Module 7. Make sure the Drive folder has sharing set to "Anyone with the link can view" so Mica can open it without a permissions prompt.

---

## Error Handling

Set up these error handlers before going live:

### On Dropbox timeout or empty folder
Add a **Router** after Module 2. Route 1: files exist (continue). Route 2: no files (send Slack message "No images found in {{1.name}} — check Dropbox upload" to `#photo-curation`).

### On Claude API error
Wrap Module 5 in an error handler (right-click the module → Add error handler → Resume). If the API call fails, post to Slack: "Claude API error on {{1.name}} — run manually via claude.ai."

### On rate limiting
The Claude API has rate limits. If you're processing multiple properties simultaneously, add a **Tools → Sleep** module (5 seconds) before Module 5. This prevents 429 errors during high-volume periods.

---

## Testing the Scenario

**Do this before enabling the trigger:**

1. Temporarily set Module 1 to manual trigger (disable the Dropbox watch)
2. Hardcode a test folder path in Module 2
3. Drop 5–10 test images into that Dropbox folder
4. Click **Run once** in Make.com
5. Watch each module execute — check for green checkmarks
6. Confirm the Hero Report appears in Google Drive
7. Confirm the Slack message posts to `#photo-curation`
8. Review the report quality — compare Claude's pick to what Trent would have chosen
9. Once satisfied, re-enable the Dropbox watch trigger

**Common issues on first run:**
- Module 3 fails: usually a Dropbox permissions issue — re-authenticate the connection
- Module 5 returns an error 400: usually a malformed JSON body — check that SKILL.md content is properly escaped (no unescaped quotes or backslashes)
- Module 7 fails: Google Drive folder path doesn't exist — create it manually first or enable auto-create
- Slack message doesn't post: check that the bot has been invited to the `#photo-curation` channel

---

## Handling Large Batches (50+ Images)

The base configuration limits to 50 images per run. For shoots with 200–400 photos:

**Option 1 — Pre-filter in Dropbox**
Ask James (photographer) to put his 30–40 best selects in a `/selects/` subfolder alongside `/raw/`. Watch `/selects/` instead of `/raw/`. This keeps the automated batch manageable without any additional Make.com complexity.

**Option 2 — Paginate in Make.com**
Set Module 2 to return 50 images, run the scenario, then add a second scenario that continues from image 51. This requires storing a cursor value between runs and is more complex to build.

**Option 3 — Two-pass approach**
Run a fast first pass on all filenames (no images, just a list), have Claude identify which image numbers are likely exterior shots based on filename patterns, then run the full image pass on just those. Requires two API calls but dramatically reduces API cost and processing time.

**Recommendation for Phase 3:** Start with Option 1. Coordinate with James to establish a `/selects/` delivery convention — this is good workflow hygiene regardless of the AI system.

---

## Cost Reference

| Item | Rate | Estimated cost per property |
|---|---|---|
| Claude API (claude-opus-4-5, ~50 images) | ~$0.015/image analyzed | $0.50–$1.50 |
| Make.com operations | ~100 ops per scenario run | Free tier: 10 runs/month; Core $9/mo: unlimited |
| Dropbox | Existing subscription | $0 incremental |
| Google Drive | Existing Google Workspace | $0 incremental |
| Slack | Existing subscription | $0 incremental |

At 20 properties/month: approximately $10–30/month total AI cost.

---

## Scenario Settings (Before Going Live)

In Make.com, click the clock icon to set the schedule:

```
Scheduling:         Every 15 minutes
Max execution time: 10 minutes
Sequential:         ON (prevents two scenarios running simultaneously on the same folder)
```

Enable the scenario only after completing a successful manual test run.

---

## Folder Structure Reference

Confirm this exists in Dropbox before enabling automation:

```
/WCM/
  /[PropertyName]/
    /photography/
      /raw/        ← Make.com reads from here
      /selects/    ← Optional: photographer pre-selects (recommended)
      /curated/    ← Hero report saves here (via Google Drive link)
      /final/      ← Mica/Trent place approved images here
```

---

## Version History

| Version | Date | Notes |
|---|---|---|
| 1.0 | Jun 2026 | Initial Make.com setup guide — covers Phases 3–4 of POC |