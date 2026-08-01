# Rectangular Display Layout Patterns

This document provides advisory best practices for designing UI layouts on rectangular displays using SquareLine Studio and LVGL. Draw heavily from mobile design patterns (Material Design 3, iOS Human Interface Guidelines) as users are familiar with these interaction models.

## Common Resolutions

*   **480×320 (3.5" landscape or portrait):** Compact. Think of older smartphones (like the original iPhone). Requires tight packing and hierarchical navigation.
*   **800×480 (5"-7" landscape):** Comfortable. Similar to car infotainment systems or dedicated smart home control panels. Good for side-by-side content.
*   **1024×600 (7"-10" landscape):** Spacious. Tablet-class interface. Supports complex multi-pane layouts.
*   Portrait orientations are also supported and map well to standard smartphone layouts.

---

## Layout Patterns

### 1. Tab Bar Navigation
A classic pattern for app-level navigation, similar to iOS tab bars (bottom) or Android tabs (top).

*   **When to use:** Apps with 3-5 distinct, equally important sections. Best for multi-section apps.
*   **Minimum Recommended Size:** 480×320
*   **Layout Mode:** TabView manages its own layout. Use FLEX or absolute within TabPages.
*   **Touch vs Rotary:** Excellent for touch. Rotary requires tabbing through headers or assigning hard keys to tabs.
*   **Widget Composition:**
```text
Screen
  └─ TabView (Full screen, tabs at top or bottom)
     ├─ TabPage (Tab 1: Home)
     │  └─ [Home Content]
     ├─ TabPage (Tab 2: Settings)
     │  └─ [Settings Content]
     └─ TabPage (Tab 3: Status)
        └─ [Status Content]
```

### 2. Dashboard Grid
A grid of cards or widgets. Inspired by iOS widget grids or Material Design dashboards.

*   **When to use:** Overview screens, home hubs, or providing quick access to multiple features.
*   **Minimum Recommended Size:** 480×320 (2x2 grid), 800×480 (3x2 or 4x2 grid).
*   **Layout Mode:** GRID layout on the container Panel, or FLEX row wrapping.
*   **Touch vs Rotary:** Good for both. Grids map logically to directional rotary encoder inputs.
*   **Widget Composition:**
```text
Screen
  └─ Panel (Full screen, GRID layout 2x2 or 3x2)
     ├─ Panel (Card 1: Icon + Value + Label)
     ├─ Panel (Card 2: Icon + Value + Label)
     ├─ Panel (Card 3: Icon + Value + Label)
     └─ Panel (Card 4: Icon + Value + Label)
```

### 3. Master-Detail
A split-screen approach: a narrow list on one side, and detailed content on the other. Like iPad Split View.

*   **When to use:** Settings menus with previews, data exploration, browsing deep hierarchical data.
*   **Minimum Recommended Size:** 800×480 (Too cramped on 480×320).
*   **Layout Mode:** FLEX row on the parent, FLEX column on the master list.
*   **Touch vs Rotary:** Great for touch. Rotary needs clear visual indication of which pane has focus.
*   **Widget Composition:**
```text
Screen
  └─ Panel (Full screen, FLEX layout Row)
     ├─ Panel (Left Column, Width 30%, FLEX Column)
     │  ├─ Button (Item 1)
     │  └─ Button (Item 2)
     └─ Panel (Right Area, Width 70%)
        └─ [Detail View Content]
```

### 4. Full-Width Cards (List View)
Stacked rows extending across the screen, typical of mobile settings menus.

*   **When to use:** Settings, configuration menus, or structured lists.
*   **Minimum Recommended Size:** 480×320.
*   **Layout Mode:** FLEX Column on the parent container. FLEX Row on each individual card.
*   **Touch vs Rotary:** Excellent for both. Very linear navigation for rotary encoders.
*   **Widget Composition:**
```text
Screen
  └─ Panel (Scrollable, FLEX layout Column)
     ├─ Panel (Row 1, Full width, FLEX Row)
     │  ├─ Label (Left aligned)
     │  └─ Switch (Right aligned, aligned end)
     ├─ Panel (Row 2, Full width, FLEX Row)
     │  ├─ Label (Left aligned)
     │  └─ Dropdown (Right aligned, aligned end)
```

### 5. Hero + Controls
A large visual element dominating the upper portion of the screen, with actionable controls below. Like a music player.

*   **When to use:** Primary display + actions. Media players, detailed single-device control (e.g., a thermostat main screen).
*   **Minimum Recommended Size:** 480×320.
*   **Layout Mode:** FLEX Column or Absolute.
*   **Touch vs Rotary:** Intuitive for both.
*   **Widget Composition:**
```text
Screen
  └─ Panel (Full screen, FLEX layout Column)
     ├─ Image/Chart/Arc (Hero element, Height 60%, Width 100%)
     └─ Panel (Control bar, Height 40%, Width 100%, FLEX Row)
        ├─ Button (Action 1)
        ├─ Button (Action 2)
        └─ Button (Action 3)
```

### 6. Toolbar + Content
A universal mobile pattern featuring a top app bar for context and actions, with content filling the rest of the screen.

*   **When to use:** Almost any screen needing a title, a back button, or global actions.
*   **Minimum Recommended Size:** 480×320.
*   **Layout Mode:** FLEX Column on main screen. FLEX Row on the Toolbar.
*   **Touch vs Rotary:** Good for touch. Rotary may require special focus handling to reach toolbar buttons.
*   **Widget Composition:**
```text
Screen
  └─ Panel (Full screen, FLEX layout Column)
     ├─ Panel (Toolbar, Height ~40-50px, Full width, FLEX Row)
     │  ├─ Button (Back icon)
     │  └─ Label (Screen Title)
     └─ Panel (Content Area, FLEX grow 1)
        └─ [Main Content]
```

### 7. Form / Input
A dedicated layout for data entry, ensuring inputs remain visible when the keyboard is active. Like a mobile form.

*   **When to use:** Entering text, configuring network settings, passwords, configuration screens.
*   **Minimum Recommended Size:** 480×320 (challenging with keyboard), better on 800×480+.
*   **Layout Mode:** FLEX Column.
*   **Touch vs Rotary:** Keyboards require touch unless you implement complex rotary-text-entry logic.
*   **Widget Composition:**
```text
Screen
  └─ Panel (Full screen, FLEX Column)
     ├─ Panel (Form Area, Scrollable)
     │  ├─ Label (Input 1 Title)
     │  ├─ TextArea (Input 1)
     │  ├─ Label (Input 2 Title)
     │  └─ Dropdown (Input 2)
     └─ Keyboard (Docked at bottom, only visible when input focused)
```

### 8. Carousel / Swipeable Screens
Navigating laterally between distinct screens or major views. Like a phone home screen.

*   **When to use:** Multi-page dashboards, peer-level content.
*   **Minimum Recommended Size:** 480×320.
*   **Layout Mode:** Not a specific container layout, but an interaction pattern using gestures.
*   **Touch vs Rotary:** Native swipe gestures for touch. Rotary encoder can map left/right turns to screen changes when not interacting with a widget.
*   **Widget Composition:**
```text
Screen 1 (Has Event: Gesture Left -> Change Screen to Screen 2)
  └─ [Content A]
Screen 2 (Has Event: Gesture Right -> Change Screen to Screen 1)
  └─ [Content B]
```
