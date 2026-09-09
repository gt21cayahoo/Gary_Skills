---
name: great-waters-gazette
description: Research, create, verify, archive, and publish the daily Great Waters Gazette as a one-page linked PDF and responsive public site. Use for Gazette runs, scheduling, catch-up checks, editorial changes, repeat prevention, weather verification, or migration between capable AI-agent environments.
---

# Great Waters Gazette

Produce the current day's edition in America/New_York. Read [references/editorial-and-design.md](references/editorial-and-design.md) before every run. Read [references/operations.md](references/operations.md) when generating, publishing, scheduling, catching up, or migrating the Gazette. Read [references/runtime-and-adapters.md](references/runtime-and-adapters.md) before installing, configuring, scheduling, or diagnosing a run on a particular service.

## Required outcome

- Research a fresh, source-backed edition using the maintained history and queues.
- Verify ZIP 31024 weather from the live Weather Channel page before publication and again against the generated PDF.
- Create one US Letter page with working source links, archive it, render it, and visually inspect it.
- Update the responsive site with the exact same content; build and publish it when an authorized hosting target is configured.
- Confirm the live page shows today's date before reporting success.
- Whenever an actual Gazette run finishes, begin the confirmation chat with the full edition date written as month, day, and year, then provide clickable links to the live site and dated PDF. Example: `The Great Waters Gazette for September 8, 2026 is complete and live.` If a run fails a publication gate, name that same intended edition date in the failure notice.

## Catch-up behavior

At the scheduled trigger and every later catch-up check, determine today's date in America/New_York and inspect a dated archive PDF, a dated `story-history.md` entry, and today's date on the live site. If all three exist, exit quietly. If today's edition is missing, immediately run today's edition. Never create separate editions for missed historical dates.

## Stop conditions

- If the live Weather Channel page cannot be loaded and confirmed as Eatonton, Georgia, ZIP 31024, do not publish.
- Never invent or carry forward weather, dates, publication dates, reuse rights, or story facts.
- Do not claim completion unless PDF verification passed and the live site was checked. If the site fails, retain the verified PDF and report the site failure with the edition date.

## Capabilities and resources

This workflow is platform-neutral. It requires an AI agent or compatible automation environment with live web research and page access, a writable working filesystem, Python PDF generation, PDF text/link/render inspection, access to durable repository state, and a way to build and publish the responsive site. Image sources must permit reuse and include attribution. The preferred scheduler is a remote task running at 6:00 AM America/New_York that does not depend on a powered-on personal computer. A local scheduler is an optional fallback only.

- `assets/project-seed/` contains the PDF builder and durable editorial state.
- `assets/site-template/` contains the responsive site without a deployment ID, dependency folder, or generated daily photo.
- `scripts/install_project.py` installs a fresh working copy without overwriting existing files.
- [README.md](README.md) explains dependencies and package layout.
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) is the migration checklist.
- [references/runtime-and-adapters.md](references/runtime-and-adapters.md) defines the neutral runtime contract and verified provider-specific setup adapters.
- [RUN_PROMPT.md](RUN_PROMPT.md) contains the platform-neutral recurring-task prompt.
- `SCHEDULED_TASK_PROMPT.md` remains as a compatibility pointer for existing installations.

Do not embed passwords, tokens, account identifiers, absolute home-directory paths, hosting project IDs, or machine-specific runtime paths. Discover runtime paths and hosting configuration in the target environment.
