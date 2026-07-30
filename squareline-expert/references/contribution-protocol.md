<!--
  SquareLine Studio Skill
  Skill Reference — Contribution Protocol
  Loaded by: squareline-expert skill agents
-->

# Contribution Protocol

This document covers how to contribute changes to the SquareLine Studio Expert
skill — the counterpart to [`issue-management.md`](./issue-management.md)
(which covers reporting defects).

---

## Route Selection Table

Use this table to determine the appropriate workflow for your change:

| Situation | Route |
|---|---|
| Defect you cannot or should not fix | File an issue → [`issue-management.md`](./issue-management.md) |
| Defect you can fix | Follow this protocol (contribution) |
| New widget reference, obvious and small | Follow this protocol, proposal step optional |
| New capability, shape needs agreement | Proposal step first, then contribution |
| Change to reference format conventions | Proposal required before implementation |
| New board target or display profile | Follow this protocol with target-authoring criteria |

---

## Enhancement / Proposal Process

### When a Proposal is Required vs. Optional

- **Required:** Any change to the project generation scripts (`scripts/`), any
  new reference format convention, any change to `SKILL.md` structure or routing,
  or any new widget type addition to the catalog.
- **Optional:** Obvious reference doc fixes, typo corrections, small isolated
  corrections to widget property defaults, or documentation clarifications.

### How to File a Proposal

File a GitHub issue on `matthewmcneill/squareline-studio-skill` with the
`P4-enhancement` label.

### Lightweight Proposal Format

Use the following structure for proposal issues:

```markdown
## Problem
<!-- What limitation, missing feature, or friction does this proposal address? -->

## Proposed Shape
<!-- Design summary, proposed changes to references/scripts/SKILL.md. -->

## Alternatives Considered
<!-- What other options were considered and why were they rejected? -->

## Affected Surface
<!-- List of files, references, scripts, or SKILL.md sections affected. -->
```

---

## PR Mechanics

- **Branch Naming:** Use Conventional Commits formatting for branch names and
  PR titles (`feat(...)`, `fix(...)`, `chore(...)`, `docs(...)`).
- **Issue Linking:** The PR description body must include `Fixes #N` referencing
  the parent issue so GitHub auto-closes it upon merge.
- **Pre-Submission Validation:** Run `scripts/validate_project.py` against any
  generated test projects to confirm output validity before submitting a PR.
- **Reference Cross-Checks:** When modifying widget properties or event
  structures, cross-check against a real SLS project export to ensure accuracy.
- **Test Coverage:** If modifying `scripts/generate_project.py`, include test
  cases that exercise the changed code paths.

---

## Authority & Contribution Origins

- **PR & Proposal Authorization:** Filing PRs and proposal issues is authorized
  for PA-tier agents and above. Tier-3 worker agents must surface findings and
  recommendations to their PA.
- **Consumer-Originated Contributions:** Skill contributions originating from
  consumer app projects must be branched in-tree within the skill repository
  (not forks), utilizing `found-by:<consumer>` attribution labels.

---

## Docs & Skill Co-Update Duty

To prevent documentation drift, any PR modifying skill capabilities must update
corresponding documentation in lockstep:

- **Reference Changes:** Any PR modifying or adding widget properties, event
  structures, or style properties must update the corresponding reference
  document under `references/`.
- **SKILL.md Updates:** If a reference file is added, removed, or renamed,
  update the Reference Lookup Table in `SKILL.md`.
- **Anti-Pitfall Checklist:** If a new common mistake is discovered during
  contribution, add it to the Anti-Pitfall Checklist in `SKILL.md`.
- **Widget Catalog Sync:** Any new widget type or property must be reflected in
  both `references/format/widget-catalog.md` and the appropriate widget group
  file under `references/widgets/`.

---

## Related

- **Reporting a defect →** [`issue-management.md`](./issue-management.md)
- **File an issue when you cannot or should not act; follow this protocol when you can.**
