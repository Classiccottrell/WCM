# West Coast Modern — AI Workflow Skills

Modular AI skill files and agent configuration for automating the West Coast Modern creative production pipeline. Built to move a property from raw photography to published assets across Instagram, website, email, and MLS — faster and with consistent quality.

## What This Does

- **Hero Selection** — AI-assisted curation of hero exterior and interior shots from a full shoot
- **Photo Sequencing** — Orders selects against the Tour Sequence and MLS priority schema
- **Content Creation** — Generates copy and image sets per platform (Instagram, Mailchimp, web)
- **Asset Management** — Organizes deliverables by property and platform for handoff

## Stack

- Claude (Anthropic API) — skill execution and content generation
- Dropbox — source photography and creative assets
- Google Drive / Gmail — comms and document repository
- Mailchimp — email campaign deployment
- Squarespace — website and active listings
- Make.com — automation orchestration

## Workflows

| ID | Name | Description |
|----|------|-------------|
| WF1 | Content Consolidation | Pulls raw assets from Dropbox, organizes by property |
| WF2 | Content Creation | Generates platform-specific copy and image sets |
| WF3 | Publishing | Builds website pages and Mailchimp campaigns |

## People

| Name | Role |
|------|------|
| Trent | Creative direction, final review |
| Mica | Production manager, workflow operator |
| Charlie | Client services |
| Phillipe | Copywriting |
| Jacob | Video / B-roll |

## Status

Active POC — hero selection skill in development. See `/skills/hero-image-selector/` for current build.
