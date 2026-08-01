# Embedded Display UI Design Guidelines

These guidelines adapt familiar mobile UX patterns (Material Design, iOS HIG) to the constraints of embedded displays using LVGL and SquareLine Studio. Treat these as advisory best practices.

## Touch & Input

### Guideline: Touch Target Sizing
**Best practice:** Size interactive widgets (BUTTON, IMGBUTTON, CHECKBOX, SWITCH) to a minimum of 44-48px (assuming ~1px per dp/pt equivalent on typical embedded displays).
**Why:** Matches mobile ergonomic standards (Material: 48dp, iOS HIG: 44pt) to ensure reliable finger taps and reduce frustration.
**Flag if:** Interactive widgets are smaller than 40x40px.
**Override OK:** Dense expert interfaces where a stylus is assumed, or secondary actions placed at the edge of large screens.

### Guideline: Spacing Between Interactive Elements
**Best practice:** Maintain at least 8-16px of clear space between tappable targets.
**Why:** Prevents mis-taps (the "fat finger" problem), especially on low-cost touch panels common in embedded devices.
**Flag if:** Buttons or interactive controls have 0-4px spacing between them.
**Override OK:** Grouped controls within a single conceptual container (like a customized segmented control) where the boundaries are visually distinct.

### Guideline: Rotary Encoder Design
**Best practice:** Design linear focus paths. Arrange focusable elements sequentially. Ensure list-like scrolling works intuitively.
**Why:** Rotary dials navigate linearly. Layouts requiring complex grid jumps are confusing without a mouse or touch.
**Flag if:** A screen relies heavily on absolute positioned elements scattered non-linearly while rotary is the primary input mode.
**Override OK:** The display is touch-only and has no rotary encoder hardware.

### Guideline: Combined Input Modes
**Best practice:** Ensure the UI is navigable by both touch and physical inputs without altering the core visual hierarchy.
**Why:** Users expect hybrid interactions (like modern infotainment systems).
**Flag if:** Touch targets are large but lack defined focus states for rotary navigation.
**Override OK:** Hardware only supports a single input paradigm.

## Visual Hierarchy

### Guideline: Typography Scale
**Best practice:** Limit text to 2-3 specific sizes (e.g., Title: 24px, Body: 16px, Caption: 12px).
**Why:** Mimics mobile type ramps to establish clear information hierarchy without overwhelming the limited screen estate.
**Flag if:** A single SCREEN uses 4+ different font sizes.
**Override OK:** Complex dashboards displaying varied telemetry data requiring extreme hierarchical distinction.

### Guideline: Colour Palette
**Best practice:** Restrict to a primary brand colour, 2-3 neutral tones (background, text), and semantic colours (red for error, green for success).
**Why:** Excessive colours cause visual noise. Semantic colours instantly communicate system state.
**Flag if:** UI elements use more than 5 distinct non-semantic colours.
**Override OK:** Image-heavy UIs or data-viz (CHART) that require categorical colour coding.

### Guideline: Contrast Ratios
**Best practice:** Ensure high contrast for text (aim for WCAG AA ~4.5:1). Avoid dark grey text on black backgrounds.
**Why:** Embedded displays are often viewed off-axis or in challenging lighting (bright sunlight or dark rooms).
**Flag if:** Foreground text and background colours are too similar (e.g., `#555555` text on `#222222` background).
**Override OK:** Subtle decorative elements or disabled states.

### Guideline: Information Density
**Best practice:** Limit a SCREEN to one primary action or ≤5 interactive elements for small displays (<4 inches).
**Why:** Cognitive overload is detrimental on small screens. Follows the mobile pattern of focused, single-purpose views.
**Flag if:** A single screen packs more than 7 distinct control widgets.
**Override OK:** Desktop-sized embedded screens or highly specialized industrial control panels.

### Guideline: Whitespace and Padding
**Best practice:** Apply generous internal padding (minimum 8px) within PANELs and CONTAINERs.
**Why:** Whitespace defines groupings and improves legibility, heavily relied upon in iOS design.
**Flag if:** Text or widgets touch the boundaries of their parent container.
**Override OK:** Full-bleed background IMAGEs or intentionally flush dividers.

## Layout Principles

### Guideline: Visual Weight and Balance
**Best practice:** Place the most important information or primary BUTTON at the top or center.
**Why:** Draws the eye to critical data immediately.
**Flag if:** Primary actions are hidden in small corners while secondary data dominates the center.
**Override OK:** Ergonomic placement where a primary action is intentionally placed near a hardware bezel button.

### Guideline: Consistent Margins
**Best practice:** Maintain uniform horizontal margins across screens (e.g., 16px on left and right).
**Why:** Creates a cohesive flow between screens, inspired by Material Design's standardized screen padding.
**Flag if:** Margins fluctuate wildly between different TABPAGEs or SCREENs.
**Override OK:** Immersive views like full-screen camera feeds or maps.

### Guideline: Safe Zones for Round Displays
**Best practice:** Constrain crucial interactive elements and text within the inscribed rectangle of a circular display.
**Why:** Prevents clipping of text and controls by the physical bezel.
**Flag if:** Important LABELs or BUTTONs are placed in the extreme corners of a rectangular canvas targeting a round display.
**Override OK:** Decorative background elements or ARC widgets designed to hug the bezel.

### Guideline: Layout Modes (FLEX over Absolute)
**Best practice:** Use FLEX layout for lists and aligned groups instead of absolute positioning.
**Why:** FLEX ensures responsive adjustments when text length changes (e.g., translations) or dynamic content is added.
**Flag if:** Numerous elements are manually positioned (x/y coordinates) to form a list or grid.
**Override OK:** Highly custom gauge clusters or designs requiring overlapping elements not supported by FLEX.

## Feedback & States

### Guideline: Pressed/Active States
**Best practice:** Define a visibly distinct PRESSED state for BUTTON and IMGBUTTON (e.g., background colour change or slight scale down).
**Why:** Provides immediate visual acknowledgment of input, acting as the embedded equivalent of the Material ripple effect.
**Flag if:** Buttons have identical DEFAULT and PRESSED styles.
**Override OK:** Hardware with extremely low refresh rates (e-ink) where rapid visual updates are impossible.

### Guideline: Disabled State
**Best practice:** Visually dim or grey out controls when unavailable, using the DISABLED state.
**Why:** Clearly communicates non-functional elements without confusing the user.
**Flag if:** Unavailable controls look exactly like active ones but do nothing when tapped.
**Override OK:** Hiding the control entirely is preferred in dynamically adapting interfaces.

### Guideline: Loading Indicators
**Best practice:** Use a SPINNER widget during asynchronous operations (e.g., fetching network data).
**Why:** Prevents the user from assuming the device has frozen.
**Flag if:** Operations taking >500ms block the UI without visual indication.
**Override OK:** Instantaneous local operations.

### Guideline: State Persistence
**Best practice:** Ensure SWITCH, CHECKBOX, and DROPDOWN widgets accurately reflect the current underlying system state.
**Why:** The UI must be the source of truth for the user.
**Flag if:** Toggling a setting doesn't visually update a state-holding widget.
**Override OK:** Momentary triggers like starting a motor (use a BUTTON instead).

## Familiar Mobile Patterns to Adopt

### Guideline: Bottom Navigation Analogy
**Best practice:** Use a TABVIEW with tabs placed at the bottom or top for top-level navigation.
**Why:** Users instinctively understand tabbed navigation from mobile apps.

### Guideline: Card-Based Layouts
**Best practice:** Group related data inside a PANEL with a slight border or shadow.
**Why:** Visually chunks information, reducing cognitive load (Material Design card pattern).

### Guideline: Settings List Pattern
**Best practice:** Construct settings using a FLEX column of CONTAINER rows, each containing a LABEL and a control (SWITCH, ROLLER).
**Why:** Replicates the familiar iOS/Android settings menus.

### Guideline: Modal/Confirmation Pattern
**Best practice:** Use a transparent overlay SCREEN or a centralized PANEL to confirm destructive actions.
**Why:** Forces user focus on a critical decision before proceeding.

## Anti-Patterns to Flag

- **Text-heavy screens:** Avoid long paragraphs in a TEXTAREA; embedded screens are for glancing, not reading.
- **Too many colours:** Visual noise dilutes the importance of semantic alerts.
- **Invisible touch targets:** Don't use unstyled containers as primary interaction points without visual affordance.
- **Fixed pixel sizing for responsive needs:** Avoid absolute layouts if the UI will be ported to multiple resolutions.

## Summary Quick Reference

| Guideline | Flag Threshold |
| :--- | :--- |
| Touch Target Sizing | Widgets < 40x40px |
| Spacing | < 4px between targets |
| Typography Scale | > 4 font sizes per screen |
| Colour Palette | > 5 non-semantic colours |
| Contrast | Low contrast text/bg pairs |
| Information Density | > 7 distinct controls per view |
| Padding | Widgets touching boundaries |
| Pressed States | Missing PRESSED style on buttons |
| Loading Indication | No visual feedback for async actions|
