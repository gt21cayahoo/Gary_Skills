# Gmail triage classification rules

## Decision order

1. A narrow exact-address or special content rule overrides a broad domain rule.
2. A registry keep rule leaves the message unchanged.
3. A registry bulk rule moves the message to Gmail Spam.
4. Strongly supported obvious spam may move automatically and create a durable bulk rule.
5. Everything ambiguous stays in the Inbox for the consolidated review.

## Sender matching

- Normalize email addresses and domains to lowercase.
- Match legitimate subdomains when the registry explicitly records a parent-domain rule; otherwise prefer the observed exact domain.
- Do not classify from display name alone.
- Do not turn a one-message content decision into a domain-wide rule when the sender also sends legitimate transactional mail. Record a special rule instead.

## Obvious spam threshold

Automatic action requires multiple aligned indicators, such as a randomized or deceptive domain, sender/address mismatch, impersonation, obfuscated Unicode, implausible claims, generic promotion with no credible relationship, or a repeated known-spam pattern. Do not auto-move merely because Gmail categorizes a message as Promotions or because it is a newsletter.

Treat suspected phishing as Spam only when the evidence is strong. Otherwise leave it untouched and flag it in the review. Never follow links or inspect attachments to decide.

## Consolidated review

Group by the narrowest sender identity that supports a durable decision. Number each item and show:

- sender and visible address/domain;
- representative subject;
- count of matching Inbox messages;
- concise reason for review.

Ask for `keep` or `bulk`. Explain that `bulk` moves the currently mapped messages to Gmail Spam and saves the sender rule for future runs.

## Registry updates

After an authorized or strongly supported automatic decision, update `sender-registry.md`: preserve existing entries, avoid duplicates, record exact addresses when domain-wide treatment is unsafe, add content-specific exceptions where needed, and update the date. Never import Yahoo decisions automatically; the user may choose to transfer selected rules later.

## Verification

Confirm every requested message-label action succeeded, then search the Inbox again and verify changed IDs are absent. Report missing IDs or partial failures without guessing. Keep initial and final counts separate because new mail may arrive during the run.
