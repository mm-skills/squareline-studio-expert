# SquareLine Studio Licensing & Free-Tier Limitations

This document describes the limitations of the SquareLine Studio **Personal (Free) License**
and provides actionable guidance for constraining AI-generated project files to stay within
those limits.

---

## License Tiers Overview

| Feature | Personal (Free) | Small Business | Business | Enterprise |
|---|---|---|---|---|
| Commercial use | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Max screens | 10 | 25 | Unlimited | Unlimited |
| Max widgets | 150 | 300 | Unlimited | Unlimited |
| Max components | 1 | 15 | Unlimited | Unlimited |
| Max global colors | 5 | 15 | Unlimited | Unlimited |
| Max themes | 2 | 5 | Unlimited | Unlimited |
| Official support | ❌ No | Limited | ✅ Yes | ✅ Priority |

> [!NOTE]
> Older versions of the free tier were more restricted (5 screens, 50 widgets).
> The current limits of 10 screens / 150 widgets apply to SLS v1.5+.

---

## Free-Tier Limits in Detail

### 1. Non-Commercial Use Only

The Personal license is strictly for **non-commercial and personal use**. Projects whose
UI was created (fully or partly) with the free version **cannot** be:
- Sold as a product
- Used in a product that is sold
- Used in a project that runs advertisements

If the user intends any commercial use, they **must** upgrade to a paid license.

**Agent behaviour:** When a user describes a project that sounds commercial (product for
sale, client work, revenue-generating), note the licensing requirement:
> ⚠️ **Licensing note:** The SquareLine Studio Personal license is non-commercial only.
> If this project is intended for sale or commercial distribution, you'll need a Small
> Business or Business license. The project files themselves will work the same way —
> this is a legal/licensing consideration.

### 2. Project Size Limits

These hard limits are enforced by SLS when opening or saving a project:

| Resource | Free-Tier Limit |
|---|---|
| Screens | **10** |
| Widgets (total across all screens) | **150** |
| Components (reusable widget templates) | **1** |
| Global colors | **5** |
| Themes | **2** |

**Agent behaviour — design-time constraints:**

- **Screens:** Design navigation flows with ≤ 10 screens. If a use case naturally
  requires more, suggest consolidation strategies:
  - Use tab views to combine related screens
  - Use dropdown/roller selection to switch content within a single screen
  - Use visibility toggling (show/hide panels) instead of separate screens

- **Widgets:** Budget 150 widgets across the entire project. A typical screen with
  moderate complexity uses 12-20 widgets. Plan widget budgets per screen:
  - Simple status screen: ~8-12 widgets
  - Form/settings screen: ~15-25 widgets
  - Complex dashboard: ~25-40 widgets
  - Leave headroom — aim for ~120 widgets max to allow for iteration

- **Components:** Only 1 reusable component is allowed. Reserve it for the most
  frequently repeated pattern (e.g., a status card used on multiple screens).

- **Global colors:** Only 5 global color slots. Use them for the primary palette:
  1. Primary brand color
  2. Secondary/accent color
  3. Background color
  4. Text/foreground color
  5. Alert/warning color
  
  All other colors should be set as inline style values on individual widgets.

- **Themes:** Only 2 themes allowed. Typically used for:
  - Light theme + Dark theme, OR
  - Default theme + High-contrast/accessibility theme

### 3. Device and Account Restrictions

- **Single device:** The free license is bound to one computer at a time.
- **Limited revocations:** The license can only be transferred (revoked) **3 times per year**.
- **Internet required:** An active internet connection is needed to log in, authenticate,
  or revoke the license. Offline work is possible once authenticated.

### 4. Support Limitations

- No access to official support channels
- No custom features or priority updates
- Community forums and documentation are still accessible

---

## Validation Rules for Free-Tier Projects

When generating projects for free-tier users, the validation script and/or manual
review should check:

```
✅ Total screens ≤ 10
✅ Total widgets (sum across all screens) ≤ 150
✅ Components ≤ 1
✅ Global colors defined in theme ≤ 5
✅ Themes ≤ 2
```

### Counting Widgets

When counting widgets against the 150 limit:
- Every widget instance counts (including children of panels, tab pages, etc.)
- SCREEN objects themselves do **not** count as widgets
- TABPAGE objects **do** count as widgets
- Children of components count once per instance of the component

### Widget Budget Planning Template

For a 10-screen project under the free tier, here is a suggested budget:

| Screen | Purpose | Widget Budget |
|---|---|---|
| Screen 1 | Home/Dashboard | 25 |
| Screen 2 | Detail View | 20 |
| Screen 3 | Settings | 20 |
| Screen 4 | Status | 15 |
| Screen 5 | Controls | 20 |
| Screen 6-10 | (reserved) | 10 each |
| **Total** | | **150** |

Adjust the budget based on actual screen complexity. Not all 10 screens need to be used.

---

## Strategies for Working Within Free-Tier Limits

### Maximise Screen Efficiency
- **Tab views** let you pack multiple "pages" of content into a single screen object
- **Show/hide panels** can simulate screen transitions without using screen slots
- **Dropdowns and rollers** can replace multiple screens of options with a single widget

### Minimise Widget Count
- Use **labels with formatted text** instead of multiple separate labels
- Use **arcs** to display multiple values in a compact form
- Prefer **sliders** over custom +/- button combos (1 widget vs 3)
- Avoid decorative-only widgets when possible

### Theme and Color Strategy
- Define the 5 most important colors as global colors for easy project-wide changes
- Apply all other colors as direct style overrides on individual widgets
- Use the 2 theme slots strategically (light/dark is the most common pattern)
