# Great Waters Gazette portable agent skill

This repository is the portable source of truth for the complete Gazette workflow. The core package is intentionally vendor-neutral and can be installed in any capable AI-agent or automation environment, including ChatGPT/Codex, Claude Cowork, Perplexity Computer, or a future compatible tool. GitHub stores and distributes the skill; it does not run the Gazette.

## Included

- Editorial, sourcing, design, weather, no-repeat, Porsche queue, PDF QA, site publication, catch-up, and dated-confirmation rules.
- A working ReportLab PDF builder as the current layout reference.
- Durable `story-history.md`, `porsche-story-queue.md`, and `carryover.md` state.
- The responsive website source and mobile icons.
- A non-destructive project installer.

The embedded history, carryover ledger, and Porsche queue are a current migration snapshot. The target environment should continue those files in durable repository state so repeat prevention survives each run and any future move.

## Portable capability contract

- A remote scheduler capable of running once daily at 6:00 AM America/New_York without a personal computer being online.
- The complete skill folder available to the agent, with `SKILL.md` at its root.
- Read/write access to durable repository or object-store state for history, queues, and approved source changes.
- A hosting/deployment capability for the public Gazette site.
- Live web/browser access, including The Weather Channel and story/photo sources.
- A writable execution environment with Python 3 plus `reportlab`, `Pillow`, `pdfplumber`, and `pypdf`.
- Poppler PDF rendering tools (`pdftoppm` or equivalent).
- Node.js 22.13 or newer and pnpm.
- Equivalent PDF inspection and website build/deployment capabilities.
- A configured hosting target available to the scheduled agent. The portable template intentionally has no deployment ID or secret.

The scheduled task should run at 6:00 AM America/New_York and use durable remote state rather than assuming that a local folder persists. The user's computer may be asleep or powered off. See [references/runtime-and-adapters.md](references/runtime-and-adapters.md) and [RUN_PROMPT.md](RUN_PROMPT.md).

## Known-service adapters

The core instructions do not depend on a particular vendor. Verified setup notes are maintained separately for:

- ChatGPT web scheduled tasks and Codex local fallback.
- Claude Cowork scheduled tasks.
- Perplexity Computer scheduled tasks and skill upload.
- Any other agent or automation platform that satisfies the capability contract.

Use only the adapter for the chosen environment. Provider names, UI paths, plugins, connectors, and hosting products belong in the adapter—not in the core workflow.

## Optional local fallback

The same package can be installed into a local agent environment for manual runs or emergency recovery. Local automations require the computer and agent application to be available and therefore are not the primary production scheduler.

## Install

Install or upload this entire folder as the `great-waters-gazette` skill in the target environment. If the service accepts ZIP uploads, preserve `SKILL.md` at the ZIP root. For a local working copy, run `python3 scripts/install_project.py /path/to/new/gazette-workspace`.

The installer refuses to overwrite an existing destination. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md), choose the correct service adapter, and create the 6:00 AM America/New_York remote scheduled task.

The history and Porsche queue preserve the current no-repeat record. Original archive PDFs and daily photographs are excluded because they are generated evidence, not required runtime code. Copy them separately only if a complete historical archive is desired.

Before the first test build, acquire that edition's licensed photograph and place it in the installed `great-waters-gazette/assets/` folder using the filename referenced by the builder. A normal daily run performs this research and asset step before PDF generation.
