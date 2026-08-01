# Navigation and Screen Flow Patterns

Navigation in embedded UIs should ideally mirror the familiar paradigms of mobile applications. Because embedded screens are often small and user interactions are brief, clarity and predictability are paramount.

## Navigation Models

These models define how users move between different views or functions in your application.

### 1. Hub-and-Spoke
- **Description:** A central "Home" screen links out to several distinct detail screens. Users navigate to a detail screen and must return to Home to access other areas.
- **When to Use:** This is the **most common embedded pattern**. Best practice: Use this when the application has a primary dashboard or status view that users should frequently return to.
- **Mobile Equivalent:** iOS Home Screen → App → Home Screen.
- **SLS Implementation:** Use `CHANGE SCREEN` event to navigate to the detail view, and `CHANGE SCREEN` on a back button to return.
- **Transitions:** Use `FADE_ON` for moving forward, and `FADE_ON` or `MOVE_RIGHT` to return.

### 2. Tab Navigation
- **Description:** Persistent tabs allow users to switch between peer sections without navigating up a hierarchy.
- **When to Use:** When you have 2-5 top-level sections of equal importance that the user needs to switch between quickly.
- **Mobile Equivalent:** iOS or Android bottom tab bar.
- **SLS Implementation:** Best practice: Use the `TABVIEW` widget for a built-in solution, or create multiple `SCREEN`s with an identical tab bar `PANEL` at the bottom of each to simulate tabs.

### 3. Carousel/Pager
- **Description:** Horizontal swiping between a sequence of peer screens.
- **When to Use:** For browsing similar items (like multiple sensor readouts) or for sequential onboarding.
- **Mobile Equivalent:** Phone home screen pages.
- **SLS Implementation:** Create multiple `SCREEN`s and use `CHANGE SCREEN` with `MOVE_LEFT` or `MOVE_RIGHT` transitions on swipe events. With a rotary encoder, rotating left/right can trigger the screen change.

### 4. Hierarchical/Drill-Down
- **Description:** Navigating progressively deeper into categories (list → detail → sub-detail).
- **When to Use:** For complex settings menus or deep data structures. Flag if: your hierarchy goes deeper than 3 levels, as it becomes disorienting on small screens.
- **Mobile Equivalent:** iOS Settings → Wi-Fi → Network Details.
- **SLS Implementation:** Use `CHANGE SCREEN` with a `MOVE_LEFT` transition moving forward, and `MOVE_RIGHT` when navigating back. This directional consistency builds a strong mental model.

### 5. Modal/Dialog
- **Description:** A temporary overlay that demands user attention for confirmation, alerts, or localized input before they can continue.
- **When to Use:** Destructive actions (e.g., "Factory Reset"), critical errors, or quick contextual settings.
- **Mobile Equivalent:** iOS Alert, Android Dialog.
- **SLS Implementation:** Create a separate `SCREEN` acting as a modal. Give it a transparent or semi-transparent background (if supported) or a dark background. Use `FADE_ON` to display it, and `CHANGE SCREEN` back to the previous screen to dismiss.

### 6. Wizard/Stepper
- **Description:** A linear, multi-step flow that guides the user through a process.
- **When to Use:** Initial device setup, Wi-Fi configuration, or complex calibration routines.
- **Mobile Equivalent:** App onboarding or checkout flow.
- **SLS Implementation:** Sequential `CHANGE SCREEN` events. Best practice: Include a progress indicator (like a `BAR` widget or series of small `IMAGE` dots) so users know where they are.

## Transition Best Practices

Transitions provide spatial context. When used correctly, they help the user understand the relationship between screens.

- **Speed:** Best practice: 300-500ms feels natural, mirroring mobile standards. The SLS default of 500ms is usually a safe bet.
- **Direction Consistency:** Always pair forward movement (e.g., `MOVE_LEFT` or `FADE_ON`) with its logical inverse for backward movement (`MOVE_RIGHT` or `FADE_ON`).
- **Spatial Navigation:** Use `MOVE_LEFT` / `MOVE_RIGHT` for spatial paradigms like carousels or drill-down menus.
- **Non-Spatial Navigation:** Use `FADE_ON` for non-spatial changes like jumping from Home to a totally distinct module, or showing a modal.
- **Avoid Instant:** Flag if: you are using `NONE` (instant) transitions. They feel abrupt and broken. Even a fast 200ms `FADE_ON` is significantly better. Override OK: When changing tabs within a `TABVIEW` where instant switching is expected.

## Rotary Encoder Navigation

When designing for hardware with a rotary encoder (knob), adapt the flow to suit physical rotation.

- **Rotate:** Navigate between items in a list, select next/previous UI elements, or turn the page in a Carousel.
- **Press:** Select or confirm (enter a detail screen, toggle a switch, confirm a modal).
- **Long-Press:** Best practice: Map long-press to a global "Back" or "Cancel" action if the hardware supports it.
- **Current Focus:** Always ensure the screen has a clear "current focus" indicator (like a highlighted border or contrasting background) so the user knows what the encoder is currently targeting.

## Anti-Patterns

Avoid these common pitfalls in embedded navigation:

- **Dead-end screens:** Screens with no obvious way to go back or return home. Always include a visible "Back" or "Home" button if not relying on hardware buttons.
- **Inconsistent back navigation:** Using a back arrow in the top-left on one screen, and a "Cancel" button at the bottom-right on another.
- **Too many levels deep:** Flag if: navigating >3 levels deep. It is confusing and tiring on small displays. Flatten the hierarchy.
- **Mixing paradigms:** Using tabs, hub-and-spoke, and a drill-down list randomly across the same device. Stick to one primary model.

## Decision Tree

| If your app has... | Use this pattern | Recommended Transition |
|--------------------|------------------|------------------------|
| 2-5 peer sections | Tab Navigation | Instant tab switch |
| A main dashboard + distinct detail views | Hub-and-Spoke | `FADE_ON` forward, `FADE_ON` back |
| A list of settings opening into details | Drill-Down | `MOVE_LEFT` forward, `MOVE_RIGHT` back |
| Sequential setup steps | Wizard | `MOVE_LEFT` forward, `MOVE_RIGHT` back |
| Multiple similar sensor readouts | Carousel | `MOVE_LEFT` / `MOVE_RIGHT` on swipe |
| Critical confirmation needed | Modal/Dialog | `FADE_ON` in, `FADE_ON` out |
