# Runtime contract and service adapters

## Platform-neutral runtime contract

The production Gazette runs remotely at 6:00 AM America/New_York and must continue when the user's computer is asleep or powered off. The runtime must be able to:

- load this complete skill and its durable state;
- browse and verify live sources, including the Weather Channel page;
- execute the included Python PDF builder and inspect/render its output;
- build and publish the responsive website;
- preserve the prior live edition until every new-edition gate passes;
- write successful history, queue, carryover, and approved source updates to durable storage; and
- return clickable links to the live site and dated PDF.

At the start of each run, obtain the skill, story history, carryover ledger, Porsche queue, builder, and site template from durable storage. Work in the runtime's temporary workspace. At the end, write back only approved durable updates. If a required capability is unavailable, stop and report the intended edition date and exact missing capability; never silently switch to a local computer.

## Transaction rule

Preserve the previous live edition until the new edition passes research, weather, PDF, and site-build checks. Publish only after those checks pass. Mark durable state complete only after the live page shows the intended date. Never store credentials, tokens, machine paths, provider deployment identifiers, dependency folders, temporary output, or licensed daily photograph binaries in the portable repository.

## ChatGPT and Codex adapter

- Install or attach the skill to a ChatGPT workspace with scheduled tasks enabled.
- Connect GitHub with read/write access to the durable repository.
- Make the required web, PDF, and Sites building/hosting capabilities available to the task.
- Create a standalone ChatGPT web scheduled task using `RUN_PROMPT.md`, daily at 6:00 AM America/New_York.
- Do not target a local project or worktree for the production task. Local Codex automation requires the computer and app to remain available and is only a fallback.
- `agents/openai.yaml` is optional UI metadata for this adapter; other platforms may ignore it.

## Claude Cowork adapter

- Install the skill or package it through the Cowork customization/plugin mechanism while preserving `SKILL.md` and all referenced resources.
- Configure the GitHub connector or another durable remote store, plus the web, file/PDF, and website-publishing tools required by the runtime contract.
- In Cowork, open **Scheduled**, create a new task, and use `RUN_PROMPT.md` as its instructions. Set it to daily at 6:00 AM America/New_York.
- Choose the remote/cloud form of the scheduled task. Do not attach the production schedule to a folder on the user's computer; a folder-dependent task runs locally.
- Review the first completed run and confirm that connectors, remote files, and publishing remain available to future sessions.

## Perplexity Computer adapter

- In Computer, open **Skills**, choose **Create skill**, then **Upload a skill**. Upload a ZIP whose root contains `SKILL.md` and the complete package; keep the ZIP below the service's current upload-size limit.
- Enable the GitHub connector or another durable remote store and any publishing connectors required by the runtime contract.
- In Computer, ask it to schedule `RUN_PROMPT.md` daily at 6:00 AM America/New_York and approve the proposed schedule. Manage it under **Computer -> Tasks**.
- A PDF/site-producing run may be treated as an attended task by the service. Verify in the first run that the necessary artifact-generation and publishing tools remain available without the user's laptop.

## Other compatible agent or automation platform

1. Install the complete folder with `SKILL.md` as the entry point.
2. Map each item in the platform-neutral runtime contract to an available tool, connector, API, or script runner.
3. Store provider-specific credentials outside the skill and repository.
4. Use `RUN_PROMPT.md` in a once-daily remote schedule at 6:00 AM America/New_York.
5. Run the deployment checklist and a controlled computer-off test before treating the migration as complete.

If the platform lacks any mandatory capability, treat the package as manual-only there or supply an external service for that capability. Do not weaken the Gazette's verification gates to make an environment appear compatible.
