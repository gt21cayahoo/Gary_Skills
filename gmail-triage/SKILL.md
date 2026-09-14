---
name: gmail-triage
description: Triage the user's Gmail inbox through the Gmail connector. Use when the user says “run Gmail triage,” “triage my Gmail,” invokes `$gmail-triage`, asks to review Gmail senders, or supplies keep/bulk decisions from a prior Gmail review. Applies durable sender rules, moves authorized junk to Gmail Spam, and presents unresolved senders in one numbered review.
---

# Gmail Triage

Use only the authenticated Gmail connector. Do not substitute Apple Mail, browser automation, another mail app, or the Yahoo registry.

## Load the durable rules

1. Read [references/workflow.md](references/workflow.md) completely.
2. Read [references/sender-registry.md](references/sender-registry.md) completely.
3. Treat this Gmail registry as authoritative. Update it after each durable user decision or strongly supported automatic spam decision.
4. Preserve one normal checkpoint: complete scanning, classification, authorized actions, verification, and report preparation before asking about unresolved senders.

## Connector workflow

1. Verify the authenticated account with the Gmail profile tool. Stop if the account cannot be identified.
2. Record the initial Inbox count with Gmail labels, then scan the complete Inbox with paginated Gmail searches. Exclude Spam and Trash. Search metadata first; read full messages only when an unresolved classification genuinely requires it.
3. Classify messages using the registry, sender address/domain, subject, snippet, and Gmail labels. Group repeated messages from the same sender when one durable decision safely covers them.
4. Leave keep matches unchanged. Move registry Bulk matches and strongly supported obvious spam to Gmail Spam by adding `SPAM` and removing `INBOX` with the Gmail message-label action. Never use permanent deletion.
5. Present all genuinely unresolved or conflicting senders in one numbered review. Include sender, address/domain, representative subject, message count, and why a decision is needed.
6. Treat the user's numbered `keep` or `bulk` response as authorization. Apply it, update the registry, and verify without another confirmation.
7. Verify changed message IDs and obtain the final Inbox count. If live arrivals cause drift, repeat search/classification/action at most three passes, then report remaining churn.

Prefer server-side search and batch label operations. Use exact Gmail message IDs returned by the connector; never invent IDs or substitute thread IDs.

## Safety boundaries

- Scope is the authenticated Gmail Inbox only unless the user explicitly expands it.
- In user-facing review language, `bulk` means move to Gmail Spam. Explain this mapping on the first run or whenever ambiguity is possible.
- Never send, reply, draft, forward, archive, mark read/unread, click links, open attachments, unsubscribe, move to Trash, or permanently delete during triage.
- Keep authentic financial, legal, medical, government, travel, reservation, billing, account-security, and personal mail unless a specific durable rule says otherwise.
- Obvious spam requires multiple mutually supporting signals; unusual typography or a promotional subject alone is insufficient.
- Do not expose passwords, authentication codes, recovery codes, or unnecessary message-body content.
- Stop for authentication/connector errors, an ambiguous Gmail account, or an action result that cannot be verified.

## Continue a prior review

Use the most recent numbered review mapping when it remains available. If required message IDs or mappings are unavailable, rescan rather than guessing. A `keep` decision updates the registry and leaves matching Inbox messages in place; a `bulk` decision updates the registry and moves the mapped messages to Spam.

## Report

Report the authenticated account, initial and final Inbox counts, messages scanned, kept/no action, moved to Spam, unresolved, registry changes, skipped IDs, errors, and any time-sensitive high-risk mail noticed. Do not quote private message bodies unless necessary.

Every chat message stating that Gmail triage completed, already completed, or needs no catch-up must include the actual completion date in America/New_York, written with the month, day, and year. Never use only relative wording such as “today” for completion status. Also summarize the work actually performed: account, initial and final Inbox counts, messages scanned, kept unchanged, moved to Spam, unresolved, registry changes, skipped IDs, and errors. For an already-completed or no-catch-up status, repeat the latest completed run's available counts instead of reporting only that no work was needed.
