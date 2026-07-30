<!--
  SquareLine Studio Skill
  Skill Reference — Issue Management Process
  Loaded by: squareline-expert skill agents
-->

# Issue Management Process

GitHub Issues on **`matthewmcneill/squareline-studio-skill`** are the canonical
system of record for all skill defects — broken project generation, incorrect
widget properties, validation failures, and documentation gaps. This document
tells you everything you need to raise, track, link, and close a skill issue.

---

## When to raise an issue

Raise a GitHub issue whenever you find a defect in the skill that:

- Produces invalid `.spj`, `.sll`, or `.slt` files that fail to open in SLS (P1/P2), or
- Generates incorrect widget properties, missing events, or wrong style values (P2), or
- Produces confusing output, misleading reference docs, or DX friction (P3).

Raise it against the **skill repo** even if you discovered it while working
in a consumer project that uses this skill. The skill repo is the right place
for skill bugs.

---

## Label taxonomy

Apply labels at filing time. Every issue gets one severity label, plus any
applicable attribution/meta labels.

### Severity (choose one)

| Label | When to use |
|-------|-------------|
| `P1-blocker` | Generated project files crash SLS or fail to open entirely |
| `P2-correctness` | Produces silently wrong output — wrong properties, broken events, invalid GUIDs |
| `P3-docs-dx` | Confusing reference docs, misleading widget catalog entries, cosmetic issues |
| `P4-enhancement` | New capability or improvement — not a defect |

### Attribution / meta (apply all that fit)

| Label | When to use |
|-------|-------------|
| `upstream-issue` | Issue was surfaced by a downstream consumer (not found internally) |
| `found-by:<your-project-name>` | Replace `<your-project-name>` with the slug of the consumer project you are working in (e.g. `found-by:smart-thermostat`, `found-by:crowpanel-demo`). Create the label on the repo if it does not exist yet. |
| `backfill` | Historical issue filed after the fix was already merged; close immediately |

> **Important for agents:** The `found-by:` label must match the consumer project
> you are currently working in. Do not copy a label from an example or from a
> previous issue without checking it matches your context.

---

## How to file an issue

### Identity rule

File under whatever GitHub identity your `gh` CLI is currently authenticated
as — that is your true author identity for this action. Before filing, confirm
which account that is:

```bash
gh auth status
# Shows which account you will file as. Make sure it is correct.
```

Do not attempt to impersonate another user (e.g. do not set `--author` to
a different person's handle). File as yourself.

### Issue title format

```
[Area] One-line description of the defect
```

Examples:
- `[Widget Catalog] SLIDER/Range min/max defaults swapped in reference`
- `[Generation] v1.6 .spj info block missing nidcnt field`
- `[Validation] validate_project.py false positive on TABPAGE flag prefixes`

### Issue body template

```markdown
## Symptom
<!-- What goes wrong. What the user sees when opening in SLS, or what the
     generation script produces incorrectly. -->

## Evidence
<!-- File paths, line numbers, JSON snippets, SLS error messages. -->
<!-- Format: `references/format/widget-catalog.md:L42` -->

## Found against commit
<!-- The skill repo commit SHA where the bug was confirmed. -->
`<SHA>`

## Suggested fix
<!-- Optional but helpful. Concrete enough to act on. -->

## Consumer context
<!-- Which consumer project found this, if applicable. -->
Found by: <your-project-name>, <PR or session context>
```

### Filing command

```bash
gh issue create \
  --repo matthewmcneill/squareline-studio-skill \
  --title "[Area] Description" \
  --body-file issue-body.md \
  --label "P2-correctness,upstream-issue,found-by:<your-project-name>"
```

Replace `found-by:<your-project-name>` with the label for your consumer project.
If the label does not exist on the repo yet, create it first:

```bash
gh label create "found-by:<your-project-name>" \
  --repo matthewmcneill/squareline-studio-skill \
  --color "a855f7" \
  --description "Reported by the <Your Project> consumer"
```

---

## How fixes close issues

The fixing PR's description must include:

```
Fixes #N
```

GitHub auto-closes the issue when the PR merges to `main`. No manual closing
is needed for issues resolved this way.

---

## Consumer-pointer convention

Once a skill issue is filed, the consumer-side audit entry is **replaced**
with a thin pointer. Never maintain a full copy of the bug description on the
consumer side — the skill issue is the source of truth.

### Format (open issue)

```markdown
## [Area] One-line title [OPEN]
- **Skill issue:** [#N](https://github.com/matthewmcneill/squareline-studio-skill/issues/N)
- **Workaround:** <describe any local workaround in use, or "none">
```

### Format (resolved issue)

```markdown
## [Area] One-line title [CLOSED]
- **Skill issue:** [#N](https://github.com/matthewmcneill/squareline-studio-skill/issues/N)
- **Resolved:** skill commit `<SHA>`, merged in PR #M
```

---

## Backfill convention

When a defect was fixed before a GitHub issue was created (e.g. discovered
retrospectively from a PR or audit):

1. File the issue using the standard body template.
2. Add the `backfill` label alongside the severity and attribution labels.
3. In the body, include: `**Resolved in:** commit \`<SHA>\`` (or PR #M).
4. **Immediately close** the issue with reason "completed".

This preserves history and lets consumers link their audit pointers to a real
issue number without leaving a ghost open issue on the board.

```bash
# Create a backfill issue and immediately close it
NUM=$(gh issue create \
  --repo matthewmcneill/squareline-studio-skill \
  --title "[Area] Description" \
  --body-file body.md \
  --label "P1-blocker,upstream-issue,found-by:<your-project-name>,backfill" | grep -oE '[0-9]+$')

gh issue close "$NUM" \
  --repo matthewmcneill/squareline-studio-skill \
  --reason completed \
  --comment "Resolved in commit \`<SHA>\` (merged in PR #M, <date>)."
```

---

## Related

- **Contributing a fix or proposing a new capability →** [`contribution-protocol.md`](./contribution-protocol.md)
- **File an issue when you cannot or should not act; follow the contribution protocol when you can.**
