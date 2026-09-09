# Operations

## Working layout

Use `great-waters-gazette/` for the builder, assets, archive, history and queues; `great-waters-gazette-site/` for the responsive site; and `output/pdf/` for direct-open dated PDFs. In cloud runs, create these as an ephemeral checkout/workspace from the connected repository and commit only durable, non-secret state. Derive paths from the workspace or script location. Never hardcode a username, home folder, Codex runtime path, hosting project ID, or secret.

## Daily run

1. Determine the America/New_York date and check archive, history, and live site for today's edition.
2. Review recent history and queues, research candidates, verify dates/access, and select distinct stories under the editorial rules.
3. Open the Weather Channel 10-day page; confirm Eatonton, Georgia and ZIP 31024; record the visible as-of time and next five calendar dates, conditions, relevant precipitation wording, highs, and lows.
4. Select yesterday's licensed photograph and record caption, creator, license, and source URL.
5. Update the PDF builder's edition data while preserving the approved layout and relative paths. Generate output and archive copies.
6. Extract PDF text and annotations. Compare all five weather rows, require exactly one page, verify expected links, and verify output/archive byte equality.
7. Render and inspect clipping, wrapping, spacing, balance, photograph/caption, and one-line desktop summaries.
8. Add used stories to history, update carryover and the rolling three-month Porsche queue, and remove used or expired Porsche candidates.
9. Update the site with identical content and the licensed photograph. Preserve responsive behavior and icons.
10. Build, save, publish, and open the live URL. Confirm the displayed date is today's date.
11. Begin the completion confirmation with the full edition date written as month, day, and year, followed by clickable site/PDF links. On partial failure, state the intended edition date, successful artifact, and failed gate.

## Automation

Schedule a standalone ChatGPT web task at 6:00 AM America/New_York. The task must run in the cloud, attach this skill, and use connected GitHub and Sites capabilities. GitHub is the durable source/state repository, not the scheduler. Do not configure the production task against a local project, local worktree, or Mac path.

Every trigger uses the three-marker completion check. If today's edition is complete and live, remain quiet; if missing, run it immediately. Commit updated history, queues, carryover, and portable source changes only after all publication gates pass. Do not commit credentials, deployment identifiers, licensed image binaries, generated dependency folders, or temporary build output.

Use a local Codex heartbeat only as an explicitly requested fallback. Local scheduling is not computer-independent.

Notification text must include the edition date whenever work ran or failed. Quiet no-op checks may state that today's dated edition is already complete and live.

## Site initialization

The template omits `.openai/hosting.json`. Use Sites building and hosting in the target environment to initialize a new project or deliberately connect an authorized existing one. Install from the lockfile, build, publish, and verify the public page. Do not hand-edit deployment metadata or reuse another environment's identifier.
