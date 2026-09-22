# Architectural Lighting Weekly Report

Reusable Codex skill for researching, writing, validating, and publishing the weekly **Architectural Lighting Weekly** website.

## What it produces

- A public, responsive weekly website with ten market-intelligence sections.
- One lead story and at least two verified briefs in every section.
- Direct source links and attributable product imagery.
- A Markdown report, candidate ledger, research audit, and report index for the local archive.
- Publication to the existing Architectural Lighting Weekly Site after all evidence and quality gates pass.

The recurring workflow is website-only. It does not generate or publish a PDF.

## Editorial safeguards

- **No source, no story.** Every published item must be opened and verified.
- Products must match the section in which they appear.
- A development may appear in only one section.
- Prior reports are used for duplication control, never as evidence.
- The design-firm section uses at least three distinct firms when three firm stories are published.
- Thin sections expand from the current week to the rolling 30-day watch and then to verified active signals, with honest labels.
- Internal research notes, category checks, blocked-source messages, and other QA copy never appear in reader-facing story cards.
- If any section cannot reach three credible stories, the previous live edition remains published.

## Skill contents

```text
architectural-lighting-weekly-report/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── references/
    ├── editorial-format.md
    ├── master-research-prompt.md
    └── site-publishing.md
```

`SKILL.md` is the agent entry point. The three references contain the detailed research method, editorial specification, and website publishing runbook.

## Required project context

The skill expects the working project to provide:

- `Coverage_Charter.md`
- `Weekly_Report_Instructions.md`
- prior reports, candidate ledgers, and research audits
- the existing `architectural-lighting-site/` checkout and its `.openai/hosting.json`

These project-specific files are intentionally not bundled into the public skill. They may include changing coverage decisions or internal working context.

## Installation

Copy the `architectural-lighting-weekly-report` folder into the agent's skills directory. For Codex, the normal location is:

```text
~/.codex/skills/architectural-lighting-weekly-report/
```

Restart or refresh the agent environment so the skill catalog is reloaded.

## Invocation

Example:

```text
Use $architectural-lighting-weekly-report to produce and publish this week's verified Architectural Lighting Weekly report and website.
```

The skill is also eligible for automatic selection when a request clearly asks to run, update, verify, or publish the recurring report.

## Schedule and hosting

The skill defines the workflow, but it is not the scheduler. The recurring task is configured separately to run each Sunday at 7:00 AM America/New_York.

The existing public destination is:

<https://architectural-lighting-week.gt21ca.chatgpt.site>

Publication must reuse the existing Site project and public access policy. Never create a replacement Site during a weekly run.
