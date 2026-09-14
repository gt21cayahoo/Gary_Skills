# Gmail Sender Registry

**Purpose:** Local authoritative sender decisions for Gmail triage.

**Last updated:** Not yet configured

> Privacy note: This repository contains a blank starter registry. Keep the populated registry in the installed local skill unless the user explicitly authorizes publishing its addresses and relationship details.

## Maintenance rules

- Do not ask about the same sender twice unless a current message conflicts with its rule.
- Normalize email addresses and domains to lowercase.
- Prefer an exact address when only one sender at a domain is covered.
- Use a domain rule only when it safely covers that domain and its legitimate subdomains.
- Preserve narrow content-specific exceptions.
- Remove duplicates without changing meaning.
- A user reversal replaces the old rule; note the change in the run report.

## Keep — leave in Inbox

Add user-confirmed exact addresses, domains, and any narrow explanatory notes here.

## Bulk — move to Gmail Spam

Add user-confirmed exact addresses or safe domain-wide rules here.

## Special rules

Add content-specific exceptions here when one sender handles both important mail and promotions.
