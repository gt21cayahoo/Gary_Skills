# Architectural Lighting Weekly Website Publishing Runbook

Use this runbook only after the weekly website edition has passed every evidence, link, image, content, and visual check.

## Fixed destination

- Site checkout: `architectural-lighting-site/`
- Hosting configuration: `architectural-lighting-site/.openai/hosting.json`
- Public URL: `https://architectural-lighting-week.gt21ca.chatgpt.site`
- Site and report title: `Architectural Lighting Weekly`
- Audience: public; anyone with the URL may view without signing in.

Reuse the existing Site project ID in `.openai/hosting.json`. Never create a replacement Site, change the slug, broaden the audience beyond public, or add authentication during a weekly run.

## Prepare the current edition

1. Treat the website as the current edition, not an accumulating archive. The Markdown reports, ledgers, and audits outside the Site checkout remain the historical research archive.
2. Update the ten sections in `architectural-lighting-site/app/report-data.ts` so their order, headlines, summaries, activity levels, links, credits, and images match the verified research.
3. Require one lead plus at least two genuine linked briefs in every section. Use correctly labeled rolling-watch or undated active signals when needed; never publish internal category checks, research notes, or other QA copy as stories.
4. Update the edition date, reporting range, week label, browser metadata, and footer. Keep the visible title exactly `Architectural Lighting Weekly`.
5. Copy only the image assets used by the new web edition into `architectural-lighting-site/public/report-assets/`. Remove obsolete site-only copies only after confirming the research archive retains the attributable originals.
6. Preserve the established scrollable magazine design and responsive behavior. Do not add an opening infographic or PDF download.

## Public-content gate

The user has authorized ongoing public publication of this report and has stated that its content is not proprietary. This authorization applies only to the verified weekly report and its directly supporting public-source images and links. Do not publish research holds, internal notes, candidate ledgers, audits, credentials, strategy, source-access details, or other workspace files.

Use only images whose source and use are appropriate for the public report. Preserve credits and direct story links.

## Validate and publish

1. Build the Site from the existing checkout and fix any build failure before continuing.
2. Confirm the page contains all ten sections, at least three linked stories per section, the correct date range, direct links for every displayed story, and no stale prior-edition or internal-process copy.
3. Commit the exact validated Site source in the Site repository.
4. Obtain a short-lived source credential for the existing Site, push the current branch, and verify the remote branch points to the local commit.
5. Package the validated build with the Sites hosting helper, save one Site version with the exact pushed commit SHA, and deploy that saved version to the Site's existing public audience.
6. Poll deployment status until it succeeds or fails. On success, confirm the returned live URL is `https://architectural-lighting-week.gt21ca.chatgpt.site` and report it with the edition date.

## Failure rule

Never deploy when research QA, story-count/category-fit checks, site build, source push, archive packaging, or version saving is incomplete. If deployment fails or never reaches success, do not change access or create another Site. Keep the previous live edition available and report the failed stage and actionable error.
