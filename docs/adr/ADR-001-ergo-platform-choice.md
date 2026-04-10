# ADR-001: Ergo Platform Choice
**Date:** 2026-04-09
**Status:** Proposed

## Context

Ergo needs to trigger hourly ergonomic break reminders and display visual stretch/exercise content. The solution must:
- Work reliably for a single user first (personal v1)
- Scale to the full company with minimal friction and no per-user technical setup
- Support rich visual content (images or GIFs of exercises)
- Be maintainable and ideally aligned with Architech's existing Microsoft/Azure tooling

The key tension is between speed of personal iteration and designing for company-wide distribution from the start. The platform choice determines both the delivery mechanism (how people get notified) and the visual content format (how exercises are displayed).

---

## Options Considered

### Option 1: Desktop Notification Script + Local Web Page
A scheduled script (Python or PowerShell) runs on the user's machine via Task Scheduler (Windows) or cron (Mac/Linux). At each interval it fires an OS-level notification; clicking it opens a locally hosted or static HTML page showing the exercises.

- **Pros:** Fastest personal v1 — can be running in under an hour. Works fully offline. Rich visual content via a web page (images, GIFs, animations). No dependency on company tools or admin approval.
- **Cons:** Requires installation on every machine — not scalable as-is. No central management or configurability for the company. Visual content lives locally unless hosted. Cross-OS inconsistencies in notification behaviour.
- **Azure compatibility:** None natively — would need a separate hosting strategy for company rollout.
- **Enterprise distribution:** Poor without packaging into an installer or MDM deployment.

### Option 2: Microsoft Teams Bot / Power Automate
A Power Automate flow triggers on a recurring schedule and posts an Adaptive Card to each user's Teams chat (or a dedicated channel). The card contains the exercise content — text, images, and action buttons (e.g., "Done", "Snooze 15 min").

- **Pros:** Architech already uses Microsoft 365 — no new tooling to approve. Company-wide rollout requires one Power Automate flow and no per-user installation. Adaptive Cards support images and interactive buttons. Centrally managed; interval and content can be changed in one place. Azure-native and aligns with Architech's stack.
- **Cons:** Teams notifications can be noisy and are often dismissed without engaging. Requires M365 admin consent for sending proactive messages to users. Visual richness is limited compared to a full web page (Adaptive Cards have image size constraints). Depends on Teams being open/active.
- **Azure compatibility:** Excellent — Power Automate is part of the M365/Azure ecosystem.
- **Enterprise distribution:** Excellent — one flow serves the whole company.

### Option 3: Slack Bot
A Slack app posts a scheduled reminder to each user's DM or a shared channel, with exercise content in the message body (images, GIFs via Block Kit).

- **Pros:** Interactive (buttons for snooze/done), rich Block Kit visuals, widely familiar.
- **Cons:** Architech's primary collaboration platform is Microsoft Teams (based on existing tooling). Requires Slack workspace admin setup. Adds a dependency on a non-primary platform. Splits attention between two messaging tools.
- **Azure compatibility:** None natively.
- **Enterprise distribution:** Moderate — requires Slack workspace and per-user opt-in.

### Option 4: Browser Extension
A Chrome/Edge extension runs a background timer and shows a browser-based popup with exercise content at each interval.

- **Pros:** Rich visual content, cross-platform, works in the browser.
- **Cons:** Requires manual installation (or MDM push) on every machine. Extension approval from IT security is often required in enterprise environments. Users can disable it. Not suitable for users who aren't always in a browser.
- **Azure compatibility:** None.
- **Enterprise distribution:** Poor without MDM management.

---

## Decision

**Two-phase approach:**

**Phase 1 (Personal v1) — Desktop Notification Script + Hosted Exercise Page**
Build a lightweight Python or PowerShell script that runs on a schedule and fires an OS notification. The exercise content lives as a simple hosted web page (GitHub Pages or Azure Static Web Apps — free tier), so the content is accessible via a URL in the notification. This gives a fast, rich personal solution that can be iterated on quickly.

**Phase 2 (Company-wide) — Microsoft Teams via Power Automate**
Once the exercise content and interval logic are validated personally, migrate the delivery to a Power Automate flow posting Adaptive Cards in Teams. The exercise content URL from Phase 1 is reused in the card — no content rebuild required. The flow can be extended to any number of users by adding them to the target list or posting to a company channel.

**Why this combination:**
The two phases share a single piece of infrastructure — the hosted exercise content page — which means Phase 1 work is not thrown away. The platform shift from desktop script to Teams is purely a delivery change; the content and cadence logic are already validated. Teams is the right company-wide delivery mechanism for Architech given M365 alignment, zero per-user installation, and central management.

---

## Consequences

- **Good:** Personal v1 is fast to build and run — no admin approval, no external dependencies. Company-wide rollout via Teams requires no per-user installation. Content is built once and reused across both phases. Azure Static Web Apps gives free, scalable hosting for the exercise content.
- **Bad:** Teams Adaptive Cards have visual constraints — large GIF animations may not render well; the exercise page will need a fallback-friendly design. Power Automate proactive messaging requires M365 admin consent, which may add lead time for the company rollout.
- **Neutral:** The desktop script is intentionally temporary — it will be retired once Teams delivery is in place. Users will need to be opted in (or opt in themselves) to the Teams flow for company-wide use.

---

## Next Decisions Required
- ADR-002: Exercise content format and hosting (images vs GIFs vs video; GitHub Pages vs Azure Static Web Apps)
- ADR-003: Break interval configuration — fixed, user-configurable, or centrally managed
