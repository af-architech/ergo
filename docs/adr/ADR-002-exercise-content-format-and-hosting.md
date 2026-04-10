# ADR-002: Exercise Content Format and Hosting
**Date:** 2026-04-09
**Status:** Proposed

## Context

Ergo needs a library of ergonomic stretches and exercises to display at break time. The content must work in two delivery contexts established in ADR-001:
- **Phase 1:** A web page opened via an OS notification link
- **Phase 2:** An Adaptive Card posted in Microsoft Teams

This creates a constraint: the content format must render correctly in both a full browser environment and inside a Teams Adaptive Card, which has size and format limitations. The hosting solution must be low-cost, fast to set up, and compatible with Azure infrastructure for the eventual company-wide rollout.

---

## Options Considered

### Option 1: Static Images (PNG/JPG) + Text Descriptions
Each exercise is represented by a single static image showing the correct posture or position, with a written description of the movement.

- **Pros:** Fastest to produce. Works everywhere — browser, Teams cards, email. Lightweight and accessible.
- **Cons:** A static image of the end position doesn't show the movement. Users may perform exercises incorrectly without seeing the motion. Less engaging, lower likelihood of actually doing the stretch.
- **Teams Adaptive Card compatibility:** Excellent.
- **Browser compatibility:** Excellent.

### Option 2: Animated GIFs
Each exercise is an animated GIF showing the full movement loop (e.g., neck rolls, wrist circles, shoulder shrugs). A static fallback image is included for environments that don't support animation.

- **Pros:** Shows movement clearly — users can mirror the GIF in real time. Works natively in browsers and in Teams Adaptive Cards (Teams supports GIF in image elements). No video player required. Widely supported across all platforms and email clients.
- **Cons:** GIFs can be large if not optimised (target <500 KB per exercise). Requires a source for quality ergonomic exercise GIFs or a brief production effort to create them. Loop animation can be distracting if left running.
- **Teams Adaptive Card compatibility:** Good — Teams renders GIFs in image elements.
- **Browser compatibility:** Excellent.

### Option 3: Short Video Clips (MP4)
Each exercise is a short looping video (5–15 seconds) demonstrating the movement.

- **Pros:** Best visual quality. Clear movement demonstration. Can include audio instruction.
- **Cons:** Teams Adaptive Cards do not support inline video playback — videos would require a link-out, breaking the in-Teams experience. Requires video hosting (additional cost or complexity). Overkill for simple ergonomic stretches.
- **Teams Adaptive Card compatibility:** Poor — no inline video support.
- **Browser compatibility:** Excellent, but adds streaming infrastructure.

### Option 4: SVG/CSS Animations (HTML-only)
Exercises are demonstrated through CSS-animated SVG illustrations embedded in the web page.

- **Pros:** Infinitely scalable, lightweight, no external media files.
- **Cons:** Significant design and development effort to produce quality animations. Does not work inside Teams Adaptive Cards (HTML not rendered). Only relevant for the Phase 1 web page.
- **Teams Adaptive Card compatibility:** None.
- **Browser compatibility:** Excellent, but Phase 2 incompatible.

---

### Option A: Azure Static Web Apps (Free Tier)
Host the exercise web page on Azure Static Web Apps with CI/CD from a GitHub repository.

- **Pros:** Free tier supports the full use case (100 GB bandwidth/month, custom domain, SSL). Azure-native — aligns with Architech's stack. GitHub Actions CI/CD means content updates deploy automatically on push. Scales to company-wide use without a tier change.
- **Cons:** Requires an Azure subscription and a GitHub repo. Slightly more setup than GitHub Pages.

### Option B: GitHub Pages
Host directly from a GitHub repository on the `gh-pages` branch or `/docs` folder.

- **Pros:** Zero cost, zero infrastructure setup. Automatic HTTPS. Fastest to get running.
- **Cons:** Not Azure-aligned — adds a non-Azure dependency for what is ultimately an Azure/M365 solution. Custom domain requires manual DNS configuration. No built-in Azure DevOps integration.

---

## Decision

**Content format: Animated GIFs with static image fallbacks**
GIFs are the only format that satisfies both delivery contexts (browser and Teams Adaptive Card) without requiring a separate content version for each phase. They clearly demonstrate movement, require no video player, and are universally supported. GIFs must be optimised to under 500 KB per exercise. A curated set of free-licence ergonomic exercise GIFs will be sourced first; original production only if quality sources are unavailable.

**Hosting: Azure Static Web Apps (Free Tier)**
The exercise content page is a simple static site — HTML, CSS, and GIF assets. Azure Static Web Apps free tier covers the full use case with zero cost, CI/CD from GitHub, and Azure alignment. This keeps all infrastructure in one ecosystem and makes the Phase 2 company-wide rollout straightforward. A GitHub repository (`architech-ergo` or similar) will hold the content and deploy automatically on push.

**Content structure:** Each exercise is a card with: the GIF, the exercise name, duration (e.g., "30 seconds"), a one-line description, and the target body area (neck, wrists, back, etc.). The page displays a randomised selection of 3–5 exercises per break to keep it fresh.

---

## Consequences

- **Good:** A single hosted URL serves both Phase 1 (OS notification link) and Phase 2 (Teams Adaptive Card image + link). Content updates deploy automatically — no need to redistribute the script when exercises change. Azure Static Web Apps free tier handles the full company-wide load without cost increase.
- **Bad:** GIF sourcing requires an upfront content effort — finding or producing 10–15 quality ergonomic exercise GIFs. File size optimisation is required to avoid slow load times on corporate networks.
- **Neutral:** The web page will be publicly accessible by URL (no auth required for Phase 1 simplicity). For Phase 2, if the company requires internal-only access, Azure Static Web Apps supports password protection or Azure AD integration as a future upgrade.

---

## Next Decisions Required
- ADR-003: Break interval configuration (already planned)
- Content sourcing: identify a free-licence GIF library or commission simple animations
