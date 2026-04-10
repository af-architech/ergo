# ADR-003: Break Interval Configuration
**Date:** 2026-04-09
**Status:** Proposed

## Context

Ergo needs to trigger ergonomic break reminders at a regular interval. The design must work for two phases:
- **Phase 1 (personal):** A single user running a local script
- **Phase 2 (company-wide):** Many users receiving reminders via Teams

The core question is: who controls the interval, and how? The answer affects both the technical implementation and the likelihood of adoption. A reminder that fires too frequently will be dismissed; one that fires too infrequently won't prevent injury. People also have different work rhythms — a 60-minute interval may suit one person but feel intrusive to another.

There is also a tension between central control (useful for IT/admin visibility and consistency) and personal agency (useful for adoption, since people are more likely to engage with something they configured themselves).

---

## Options Considered

### Option 1: Fixed Interval (Hardcoded)
The interval is hardcoded at 60 minutes. No configuration is possible — everyone gets the same timing.

- **Pros:** Simplest to build and maintain. No configuration UI needed. No risk of users setting intervals so long they defeat the purpose (e.g., 4 hours).
- **Cons:** 60 minutes may not suit everyone. Users in deep focus sessions may want 90 minutes; users with known RSI risk may want 45. No flexibility = lower adoption. Complaints will be raised immediately when rolling out company-wide.
- **Phase 1 fit:** Acceptable for a first build.
- **Phase 2 fit:** Poor — a single hardcoded value across a company will generate friction.

### Option 2: User-Configurable via Config File
The interval is set in a simple JSON or YAML config file (e.g., `ergo-config.json`) that the user edits manually. Default: 60 minutes. Users can change it to any value within a sensible range (e.g., 30–120 minutes).

- **Pros:** Simple to implement. Gives users agency, which increases adoption. The default of 60 minutes covers most users out of the box. No UI required in Phase 1 — just a text file.
- **Cons:** Requires users to know where the config file is and be comfortable editing it. Not visible or manageable at a company level in Phase 1. Users could set it to an extreme value.
- **Phase 1 fit:** Excellent.
- **Phase 2 fit:** Good as a user-level override when combined with a central default.

### Option 3: Centrally Managed (Admin Sets for Everyone)
An admin sets the interval for all users from a central location. In Phase 1 this would be an environment variable or deployment parameter; in Phase 2 it would be a Power Automate flow setting.

- **Pros:** Consistent experience across the company. Admin can adjust based on health/safety guidance. No per-user configuration needed.
- **Cons:** Removes personal agency — a known driver of low adoption for wellness tools. Requires admin involvement for any change. Doesn't account for individual work patterns or known health needs. Overkill for Phase 1.
- **Phase 1 fit:** Poor — no admin infrastructure exists yet.
- **Phase 2 fit:** Good as a default, but should not be the only control.

### Option 4: User-Configurable with Central Default and Admin Override
A central default is set by an admin (e.g., 60 minutes). Each user can override this within an allowed range (e.g., 30–90 minutes) via a config file or a simple settings prompt. The admin can enforce a maximum interval if required for health policy compliance.

- **Pros:** Balances personal agency with company-level consistency. Increases adoption by giving users ownership. Allows health/safety policy to be enforced without being unnecessarily rigid.
- **Cons:** Slightly more complex to implement. Requires defining the allowed range and communicating it to users.
- **Phase 1 fit:** Slightly over-engineered for a single-user script, but the config file part is trivial to add.
- **Phase 2 fit:** Excellent.

---

## Decision

**Option 4: User-configurable with a central default and admin override capability**

**Phase 1 implementation:** A `ergo-config.json` file in the same directory as the script contains the interval in minutes. If the file is absent or the value is invalid, the script defaults to 60 minutes. No UI required — users edit the file directly.

```json
{
  "break_interval_minutes": 60,
  "break_duration_seconds": 30,
  "start_hour": 9,
  "end_hour": 18
}
```

`start_hour` and `end_hour` define the active window — reminders only fire during working hours, preventing after-hours notifications. This is a Phase 1 addition that costs nothing to implement and avoids immediate complaints.

**Phase 2 implementation:** The Power Automate flow uses a configurable parameter for the default interval (set by the flow owner). A future enhancement can add a Teams-based "settings" interaction where users type `/ergo set 45` to personalise their interval. For the initial company rollout, a single central default of 60 minutes is sufficient.

**Allowed range:** 30–90 minutes. Values outside this range are silently corrected to the nearest boundary on startup.

---

## Consequences

- **Good:** Users feel ownership over the tool, which increases engagement. The config file approach requires no UI investment in Phase 1. Working-hours enforcement (start/end hour) prevents the most common early complaint about wellness tools. The JSON schema is simple enough that the Phase 2 Power Automate flow can consume the same defaults.
- **Bad:** Users who don't know about the config file will never customise it — the default must be good. "30 minutes" is a valid config but may feel disruptive for some roles; documentation should recommend 45–60 minutes as the ergonomic sweet spot.
- **Neutral:** The allowed range of 30–90 minutes is a judgment call. It can be revisited after Phase 1 personal testing.

---

## Summary: Configuration Schema (Phase 1)

| Field | Default | Range | Description |
|---|---|---|---|
| `break_interval_minutes` | 60 | 30–90 | How often the break reminder fires |
| `break_duration_seconds` | 30 | 20–120 | How long the exercise page stays open (optional auto-close) |
| `start_hour` | 9 | 0–23 | Hour of day reminders begin (24h clock) |
| `end_hour` | 18 | 0–23 | Hour of day reminders stop |
