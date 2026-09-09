# Cloud run contract

## Runtime boundary

The production Gazette runs as a standalone scheduled task in ChatGPT on the web at 6:00 AM America/New_York. It must continue when Gary's Mac is asleep or powered off. GitHub is the portable skill and durable-state repository only; do not create a GitHub Actions workflow or treat a repository schedule as the runtime.

Web scheduled tasks do not retain a local Mac folder between runs. At the start of each run, obtain the skill, story history, carryover ledger, Porsche queue, builder, and site template from the connected repository. Work in the task's temporary cloud workspace. At the end, write back only approved durable updates.

## Required connections

- GitHub: read the package and durable state; write successful history/queue/source updates.
- Live web: research sources, load and verify The Weather Channel, and obtain a reusable licensed daily photograph.
- PDF capability: generate, extract, inspect links, render, and visually verify the one-page edition.
- Sites building and hosting: update and publish the responsive public site, then verify its displayed date.

If any required connection is missing, expired, read-only when a write is required, or unavailable, stop and report the intended edition date and exact missing capability. Never fall back to a local Mac silently.

## Transaction rule

Preserve the previous live edition until the new edition passes research, weather, PDF, and site-build checks. Publish the new site only after those checks pass. Commit durable state only after the live page shows the intended date. If publication fails, retain any verified temporary PDF if accessible, do not mark the edition complete in history, and report the failed gate.

## Scheduling rule

Create one standalone cloud scheduled task using `SCHEDULED_TASK_PROMPT.md`. Set the schedule to 6:00 AM America/New_York. The skill defines the workflow; the scheduled task defines the clock. A local heartbeat may exist only as an optional manually chosen fallback and is not required for production.
