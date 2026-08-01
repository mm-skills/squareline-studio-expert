# Widget Composition Recipes

These ready-made widget composition recipes provide practical guides for building common embedded UI components in SquareLine Studio (SLS).

## 1. Thermostat / Setpoint Control
Ideal for smart home panels or HVAC controllers.

**Widget Tree:**
```text
SCREEN
  └─ PANEL (Transparent background)
       ├─ ARC (Temperature range scale)
       ├─ LABEL (Current temp, large font, centered)
       ├─ LABEL (Setpoint temp, smaller font, below current)
       ├─ BUTTON (Increase setpoint, right)
       └─ BUTTON (Decrease setpoint, left)
```
- **Alternative:** Use a `SLIDER` for the setpoint instead of buttons.
- **Sizes:**
  - Round (240x240): Arc covers outer edge. Buttons sit at 3 o'clock and 9 o'clock.
  - Rectangular (480x320): Panel takes up 50-70% of screen width, centered.
- **Styling:** Best practice: Color code the Arc (e.g., blue for cool, red for heat).

## 2. Toggle Control Row
A standard settings-style row for boolean options.

**Widget Tree:**
```text
PANEL (FLEX Layout: ROW, space-between alignment)
  ├─ LABEL (Setting name, left-aligned)
  └─ SWITCH (Right-aligned)
```
- **Mobile Equivalent:** iOS Settings toggle row.
- **Sizes:** Recommended panel height is 48-60px to ensure a comfortable touch target area.
- **Styling:** Add slight padding to the left and right of the Panel.

## 3. Sensor Dashboard
Displays multiple metrics simultaneously.

**Widget Tree (Rectangular 2x2 Grid):**
```text
PANEL (GRID or FLEX layout)
  ├─ PANEL (Card 1)
  │    ├─ IMAGE (Sensor icon)
  │    ├─ LABEL (Value, large)
  │    └─ LABEL (Metric name, small)
  ├─ PANEL (Card 2) ...
  ├─ PANEL (Card 3) ...
  └─ PANEL (Card 4) ...
```
- **Sizes:**
  - Round (240x240): Divide into 4 quadrants (top, bottom, left, right) without distinct card backgrounds to save space.
  - Rectangular (480x320): A 2x2 or 3x2 grid of distinct card Panels.
- **Styling:** Best practice: Give each card Panel a subtle background color or corner radius to separate data visually.

## 4. Navigation Bar
A persistent bottom bar for switching major sections.

**Widget Tree:**
```text
PANEL (FLEX Layout: ROW, space-evenly, pinned to bottom of SCREEN)
  ├─ IMGBUTTON / BUTTON (Tab 1)
  │    └─ LABEL (Optional text below icon)
  ├─ IMGBUTTON / BUTTON (Tab 2)
  └─ IMGBUTTON / BUTTON (Tab 3)
```
- **Mobile Equivalent:** iOS Tab Bar or Material Bottom Navigation.
- **Sizes:** Recommended height: 56-64px (Material design standard) or ~49px (iOS standard).
- **Wiring:** Each button should trigger a `CHANGE SCREEN` event to its respective section.

## 5. Settings List
A vertical scrolling list of options.

**Widget Tree:**
```text
PANEL (FLEX Layout: COLUMN, scrollable)
  ├─ PANEL (Row 1 - Toggle Control Recipe)
  ├─ PANEL (Separator - Height 1px, background color grey)
  ├─ PANEL (Row 2 - Label + DROPDOWN)
  ├─ PANEL (Separator)
  └─ PANEL (Row 3 - Label + SLIDER)
```
- **Mobile Equivalent:** iOS Settings app.
- **Styling:** Use 1px height Panels as separator lines between rows to create structure. Ensure the parent Panel has scrolling enabled.

## 6. Alert / Confirmation Dialog
A modal overlay for critical choices.

**Widget Tree:**
```text
SCREEN (Modal, dark transparent background if supported)
  └─ PANEL (Centered, opaque background, rounded corners)
       ├─ LABEL (Warning/Confirmation message)
       ├─ BUTTON (Cancel - Neutral color)
       └─ BUTTON (Confirm - Primary or Destructive color)
```
- **Transitions:** Use `FADE_ON` for both entering and exiting the modal.
- **Styling:** Best practice: Visually distinguish the primary action (Confirm) with a bold color, while keeping the secondary action (Cancel) neutral or outlined.

## 7. Loading / Splash Screen
Shown during startup or heavy processing.

**Widget Tree:**
```text
SCREEN
  ├─ IMAGE (Company Logo, centered)
  ├─ SPINNER (Positioned below logo)
  └─ LABEL (Status text, e.g., "Initializing...", below spinner)
```
- **Wiring:** Add a `SCREEN LOADED` event to the Screen that triggers a `CHANGE SCREEN` (to the main dashboard) after a set delay.

## 8. Data Chart View
Displaying historical or trending data.

**Widget Tree:**
```text
PANEL (FLEX Layout: COLUMN)
  ├─ CHART (Primary area, takes up most vertical space)
  ├─ PANEL (FLEX ROW - X-Axis labels)
  └─ PANEL (FLEX ROW - Time range selectors)
       ├─ BUTTON ("1H")
       ├─ BUTTON ("24H")
       └─ BUTTON ("7D")
```
- **Sizes:** Recommended minimum chart size: 300x200px for legibility. Flag if: attempting to put detailed charts on displays smaller than 3.5 inches.

## 9. Input Form
A structured view for data entry.

**Widget Tree:**
```text
SCREEN
  ├─ PANEL (FLEX COLUMN - Form content)
  │    ├─ LABEL ("Username")
  │    ├─ TEXTAREA (Input field 1)
  │    ├─ LABEL ("Password")
  │    └─ TEXTAREA (Input field 2)
  └─ KEYBOARD (Pinned to bottom, hidden by default)
```
- **Wiring:** When a `TEXTAREA` receives focus (Clicked event), show the `KEYBOARD` and set it as the Target.

## 10. Clock / Time Display
A decorative and functional time readout, common on standby screens.

**Widget Tree:**
```text
SCREEN
  ├─ ARC (Decorative outer ring, can indicate seconds)
  ├─ LABEL (Time, very large font, centered)
  └─ LABEL (Date/Day, smaller font, below time)
```
- **Alternative:** For a more complex analog look, use multiple thin `ARC` widgets or rotated `IMAGE` widgets for hours, minutes, and seconds.
- **Sizes:** Make the primary time Label the dominant element on the screen.
