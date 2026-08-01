# Round Display Layout Patterns

This document outlines advisory best practices for designing UI layouts on circular or round displays (e.g., 240×240, 390×390) using SquareLine Studio and LVGL. Draw inspiration from smartwatch OS (watchOS, Wear OS) interfaces.

## Safe Content Zone

The visible area on a round display is a circle inscribed within the square resolution of the display driver. The corners of the bounding square are completely invisible.

**Best practice:** Confine critical UI elements and interactive widgets to a "Safe Zone" circle, slightly smaller than the full resolution.
**Why:** Prevents clipping of text or touch targets at the curved edges.
**Flag if:** Widgets are placed in the absolute corners of the screen.
**Override OK:** If the widget is an ARC meant to follow the physical bezel, or a background IMAGE designed to bleed off the edge.

### Safe Zone Calculation

For a display with resolution $R \times R$:
*   **Diameter:** $R$
*   **Safe Zone Diameter:** $\approx 0.85 \times R$
*   **Center Point:** $(R/2, R/2)$

| Resolution | Center (x, y) | Approx. Safe Zone Diameter |
| :--- | :--- | :--- |
| 240×240 | (120, 120) | 200px |
| 390×390 | (195, 195) | 330px |
| 480×480 | (240, 240) | 400px |

---

## Layout Patterns

### 1. Gauge / Value Display
A prominent, single-value focus. Similar to a smartwatch complication or a thermostat screen.

*   **When to use:** Showing a single primary metric like temperature, humidity, progress, or speed.
*   **Approximate Sizing (240×240):** Arc takes up full 240px width/height, Value label uses a large font (e.g., 48px), Unit label smaller (e.g., 14px).
*   **Widget Composition:**
```text
Screen (No layout)
  └─ Arc (Background/Indicator gauge, centered, full size)
  └─ Panel (Container, centered, transparent)
     ├─ Label (Primary value, centered, 48px font)
     └─ Label (Unit, below value, 14px font)
```

### 2. Radial Menu
A circular arrangement of interactive elements. Very friendly for rotary encoders (rotate to highlight, press to select). Like watchOS app launcher.

*   **When to use:** Home screens, mode selection, or top-level navigation.
*   **Approximate Sizing (240×240):** Central element ~80x80px. Surrounding buttons ~40x40px placed on a ~160px diameter ring.
*   **Widget Composition:**
```text
Screen (No layout)
  ├─ Image/Label (Central focus/status element, centered)
  ├─ Button (Item 1, positioned on radial path)
  ├─ Button (Item 2, positioned on radial path)
  ├─ Button (Item 3, positioned on radial path)
  └─ Button (Item 4, positioned on radial path)
```

### 3. Value + Controls
A central value readout with adjustment controls positioned in the safe area. Like a thermostat setpoint.

*   **When to use:** Adjustable setpoints, volume control, dimmer switches.
*   **Approximate Sizing (240×240):** Central label ~100x40px. Buttons ~40x40px below the label.
*   **Widget Composition:**
```text
Screen (No layout)
  └─ Panel (Container, centered, transparent)
     ├─ Label (Value readout, top-centered)
     ├─ Slider (Optional continuous control)
     ├─ Button (Minus/Down control, bottom-left)
     └─ Button (Plus/Up control, bottom-right)
```

### 4. Status Dashboard
A grid-like arrangement adapted for a circle, providing a multi-sensor overview. Like smartwatch complications grid.

*   **When to use:** Monitoring multiple data points simultaneously (e.g., weather station, multi-room status).
*   **Approximate Sizing (240×240):** 4 Panels of ~80x80px arranged in quadrants, clustered near the center.
*   **Widget Composition:**
```text
Screen (No layout)
  └─ Panel (Container, centered, ~180x180, Grid layout 2x2)
     ├─ Panel (Quadrant 1: Icon + Value Label)
     ├─ Panel (Quadrant 2: Icon + Value Label)
     ├─ Panel (Quadrant 3: Icon + Value Label)
     └─ Panel (Quadrant 4: Icon + Value Label)
```

### 5. Full-Screen Indicator
A simple, bold visual state indicator. Like a phone lock screen notification.

*   **When to use:** Alerts, warnings, binary on/off states, or simple notifications.
*   **Approximate Sizing (240×240):** Icon ~100x100px centered, Status label below it.
*   **Widget Composition:**
```text
Screen (No layout)
  └─ Panel (Container, centered, full safe zone)
     ├─ Image (Large status icon, top-centered)
     ├─ Label (Status text, below icon)
     └─ Button (Optional action/dismiss, bottom-centered)
```

### 6. Scrollable List
A vertical list of items, constrained horizontally to fit within the safe zone. Like a smartwatch settings list.

*   **When to use:** Settings menus, option selections, lists of devices.
*   **Approximate Sizing (240×240):** Panel width max 160px to avoid edge clipping during scroll. List items ~160x40px.
*   **Widget Composition:**
```text
Screen (No layout)
  └─ Panel (Scrollable container, centered, ~160x200, Flex layout Column)
     ├─ Button (List Item 1)
     ├─ Button (List Item 2)
     ├─ Button (List Item 3)
     └─ Button (List Item 4)
```

### 7. Clock / Dial
A classic analog clock or decorative dial interface. Decorative but common for smart home displays.

*   **When to use:** Smart home idle screens, timers, or aesthetic dashboards.
*   **Approximate Sizing (240×240):** Background Arc 240x240px. Hand images pivot from the center (120, 120).
*   **Widget Composition:**
```text
Screen (No layout)
  ├─ Arc/Image (Clock face background)
  ├─ Label (Numbers 12, 3, 6, 9 positioned radially)
  ├─ Image (Hour hand, centered, rotated dynamically)
  └─ Image (Minute hand, centered, rotated dynamically)
```
