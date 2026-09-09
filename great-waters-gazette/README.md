# Great Waters Gazette portable cloud skill

This repository is the portable source of truth for the complete Gazette workflow. It can be installed in another ChatGPT/Codex environment without copying machine-specific paths, secrets, build caches, deployment identifiers, or prior generated PDFs. GitHub stores and distributes the skill; it does not run the Gazette.

## Included

- Editorial, sourcing, design, weather, no-repeat, Porsche queue, PDF QA, site publication, catch-up, and dated-confirmation rules.
- A working ReportLab PDF builder as the current layout reference.
- Durable `story-history.md`, `porsche-story-queue.md`, and `carryover.md` state.
- The responsive Sites application source and mobile icons.
- A non-destructive project installer.

The embedded history, carryover ledger, and Porsche queue are a current migration snapshot. The target environment should continue those files in durable repository state so repeat prevention survives each run and any future move.

## Preferred runtime: ChatGPT cloud

- A ChatGPT workspace with web scheduled tasks enabled.
- This skill installed or attached to the scheduled chat.
- The GitHub connection with read/write access to the repository used for durable history, queues, and generated source changes.
- Sites building/hosting access for the public Gazette site.
- Live web/browser access, including The Weather Channel and story/photo sources.
- A cloud execution environment with Python 3 plus `reportlab`, `Pillow`, `pdfplumber`, and `pypdf`.
- Poppler PDF rendering tools (`pdftoppm` or equivalent).
- Node.js 22.13 or newer and pnpm.
- The Codex PDF skill plus Sites building and hosting skills.
- A configured Sites deployment available to the cloud task. The portable template intentionally has no deployment ID or secret.

The scheduled task should run at 6:00 AM America/New_York. It must use repository-backed state because web scheduled tasks do not retain access to a Mac folder between runs. The Mac may be asleep or powered off. See [references/cloud-run.md](references/cloud-run.md) and [SCHEDULED_TASK_PROMPT.md](SCHEDULED_TASK_PROMPT.md).

## Optional local fallback

The same package can be installed into a local Codex environment for manual runs or emergency recovery. Local automations require the computer and Codex to be available and therefore are not the primary production scheduler.

## Install

Install this entire folder as the `great-waters-gazette` skill in the target environment. For a local working copy, run `python3 scripts/install_project.py /path/to/new/gazette-workspace`.

The installer refuses to overwrite an existing destination. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) to verify dependencies and create the 6:00 AM America/New_York cloud scheduled task.

The history and Porsche queue preserve the current no-repeat record. Original archive PDFs and daily photographs are excluded because they are generated evidence, not required runtime code. Copy them separately only if a complete historical archive is desired.

Before the first test build, acquire that edition's licensed photograph and place it in the installed `great-waters-gazette/assets/` folder using the filename referenced by the builder. A normal daily run performs this research and asset step before PDF generation.
