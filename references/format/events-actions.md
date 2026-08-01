# Events and Actions

This document describes the event structure, trigger types, action types, and screen transition fade modes used in SquareLine Studio.

## Event Structure

Events are inline children of widget properties:

```json
{
  "disabled": false,
  "nid": 1000343,
  "strtype": "_event/EventHandler",
  "strval": "CLICKED",
  "InheritedType": 10,
  "childs": [
    { "strtype": "_event/name", "strval": "Event1", "InheritedType": 10 },
    { "strtype": "_event/condition_C", "strval": "", "InheritedType": 10 },
    { "strtype": "_event/condition_P", "strval": "", "InheritedType": 10 },
    {
      "strtype": "_event/action",
      "strval": "CHANGE SCREEN",
      "InheritedType": 10,
      "childs": [ /* action parameters */ ]
    }
  ]
}
```

## Event Trigger Types

| Trigger | Description | Confirmed |
|---------|-------------|:---:|
| `CLICKED` | Short press and release | ✅ |
| `PRESSED` | Immediately on press | ✅ |
| `RELEASED` | On release | ✅ |
| `PRESS_LOST` | Press followed by pointer leaving widget | ✅ |
| `LONG_PRESSED` | After long press threshold | LVGL |
| `LONG_PRESSED_REPEAT` | Repeated after long press | LVGL |
| `SHORT_CLICKED` | Short click detected | LVGL |
| `VALUE_CHANGED` | Widget value changed | ✅ |
| `CHECKED(VALUE_CHANGED)` | Checkbox/switch set to checked | ✅ |
| `UNCHECKED(VALUE_CHANGED)` | Checkbox/switch set to unchecked | ✅ |
| `SCREEN_LOADED` | Screen fully loaded | ✅ |
| `SCREEN_UNLOADED` | Screen fully unloaded | ✅ |
| `SCREEN_LOAD_START` | Screen load begins | ✅ |
| `SCREEN_UNLOAD_START` | Screen unload begins | ✅ |
| `GESTURE_LEFT(GESTURE)` | Left swipe gesture | ✅ |
| `GESTURE_RIGHT(GESTURE)` | Right swipe gesture | ✅ |
| `GESTURE_UP(GESTURE)` | Up swipe gesture | ✅ |
| `GESTURE_DOWN(GESTURE)` | Down swipe gesture | ✅ |
| `FOCUSED` | Widget gains focus | LVGL |
| `DEFOCUSED` | Widget loses focus | LVGL |
| `READY` | Process completed | LVGL |
| `CANCEL` | Process cancelled | LVGL |
| `KEY` | Key input received | LVGL |
| `EDITED` | Text content modified | LVGL |
| `INSERT` | Text inserted | LVGL |

> [!NOTE]
> ✅ = confirmed in SLS example projects. LVGL = valid LVGL event type, not yet seen in SLS projects.
> Compound triggers like `CHECKED(VALUE_CHANGED)` and `GESTURE_LEFT(GESTURE)` use SLS-specific
> naming. The parenthesized suffix indicates the underlying LVGL event type.

## Event Action Types

#### CHANGE SCREEN ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "CHANGE SCREEN",
  "childs": [
    { "strtype": "CHANGE SCREEN/Name", "strval": "CHANGE SCREEN" },
    { "strtype": "CHANGE SCREEN/Call", "strval": "ChangeScreen( <{Screen_to}>, lv.SCR_LOAD_ANIM.<{Fade_mode}>, <{Speed}>, <{Delay}>)" },
    { "strtype": "CHANGE SCREEN/CallC", "strval": "_ui_screen_change( &<{Screen_to}>, LV_SCR_LOAD_ANIM_<{Fade_mode}>, <{Speed}>, <{Delay}>, &<{Screen_to}>_screen_init);" },
    { "strtype": "CHANGE SCREEN/Screen_to", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "CHANGE SCREEN/Fade_mode", "strval": "MOVE_LEFT", "InheritedType": 3 },
    { "strtype": "CHANGE SCREEN/Speed", "strval": "500", "InheritedType": 6 },
    { "strtype": "CHANGE SCREEN/Delay", "InheritedType": 6 }
  ]
}
```

#### CALL FUNCTION ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "CALL FUNCTION",
  "childs": [
    { "strtype": "CALL FUNCTION/Name", "strval": "CALL FUNCTION" },
    { "strtype": "CALL FUNCTION/Call", "strval": "<{Function_name}>( event_struct )" },
    { "strtype": "CALL FUNCTION/CallC", "strval": "<{Function_name}>( e );" },
    { "strtype": "CALL FUNCTION/Function_name", "strval": "on_slide_changed", "InheritedType": 10 },
    { "strtype": "CALL FUNCTION/Dont_export_function", "strval": "False", "InheritedType": 2 }
  ]
}
```

#### PLAY ANIMATION ✅ confirmed (v1.5 project)
```json
{
  "strtype": "_event/action", "strval": "PLAY ANIMATION",
  "childs": [
    { "strtype": "PLAY ANIMATION/Name", "strval": "PLAY ANIMATION" },
    { "strtype": "PLAY ANIMATION/Call", "strval": "<{FunctionName}>(<{Target}>, <{Delay}>)" },
    { "strtype": "PLAY ANIMATION/CallC", "strval": "<{FunctionName}>(<{Target}>, <{Delay}>);" },
    { "strtype": "PLAY ANIMATION/FunctionName", "strval": "progress_Animation" },
    { "strtype": "PLAY ANIMATION/Animation", "strval": "progress", "InheritedType": 8 },
    { "strtype": "PLAY ANIMATION/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "PLAY ANIMATION/Delay", "InheritedType": 6 }
  ]
}
```

#### LABEL_PROPERTY (Set Label Text) ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "LABEL_PROPERTY",
  "childs": [
    { "strtype": "LABEL_PROPERTY/Name", "strval": "LABEL_PROPERTY", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/Call", "strval": "SetLabelProperty(<{Target}>, '<{Property}>', '<{Value}>')", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/CallC", "strval": "_ui_label_set_property(<{Target}>, _UI_LABEL_PROPERTY_<{Property}>, \"<{Value}>\");", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "LABEL_PROPERTY/Property", "strval": "Text", "InheritedType": 3 },
    { "strtype": "LABEL_PROPERTY/Value", "strval": "Test", "InheritedType": 10 }
  ]
}
```

#### INCREMENT ARC ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "INCREMENT ARC",
  "childs": [
    { "strtype": "INCREMENT ARC/Name", "strval": "INCREMENT ARC", "InheritedType": 10 },
    { "strtype": "INCREMENT ARC/Call", "strval": "IncrementArc( <{Target}>, <{Value}> )", "InheritedType": 10 },
    { "strtype": "INCREMENT ARC/CallC", "strval": "_ui_arc_increment( <{Target}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "INCREMENT ARC/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "INCREMENT ARC/Value", "integer": 30, "InheritedType": 6 }
  ]
}
```

#### INCREMENT BAR
Same structure as INCREMENT ARC. Uses `_ui_bar_increment()`.

#### INCREMENT SLIDER
Same structure as INCREMENT ARC. Uses `_ui_slider_increment()`.

#### DELETE SCREEN
Removes a screen from memory.

#### MODIFY FLAG
Sets or clears a widget flag (e.g., Hidden, Clickable).
Parameters: Target (IT=9), Flag name (IT=3), Set/Clear (IT=3).

#### MODIFY STATE
Sets or clears a widget state (e.g., Checked, Disabled).
Parameters: Target (IT=9), State (IT=3), Set/Clear (IT=3).

#### SET OPACITY (opacityAnimation)
Sets widget opacity with optional animation.
Parameters: Target (IT=9), Opacity (IT=6), Animation duration (IT=6).

#### KEYBOARD SET TARGET
Links a KEYBOARD widget to a TEXTAREA.
Parameters: Target keyboard (IT=9), Target textarea (IT=9).

#### MOVE CURSOR
Moves a text cursor in a TEXTAREA.
Parameters: Target (IT=9), Direction (IT=3).

#### STEP SPINBOX
Increments or decrements a SPINBOX.
Parameters: Target (IT=9), Direction (IT=3: "INCREMENT"/"DECREMENT").

#### SWITCH THEME
Changes the active theme.
Parameters: Theme name (IT=10).

#### SET TEXT VALUE FROM ARC ✅ confirmed
Sets a label's text to an arc's current value.
Parameters: Target label (IT=9), Source arc (IT=9).

#### SET TEXT VALUE FROM SLIDER ✅ confirmed
Sets a label's text to a slider's current value.
Parameters: Target label (IT=9), Source slider (IT=9).

#### SET TEXT VALUE WHEN CHECKED
Sets a label's text based on whether the source widget is in checked state.
Parameters: Target label (IT=9), Checked text (IT=10), Unchecked text (IT=10).

#### Property-Setting Actions

These follow the same pattern as LABEL_PROPERTY but for other widget types:

| Action | Widget | Sets |
|--------|--------|------|
| `BAR_PROPERTY` | BAR | Value |
| `BASIC_PROPERTY` | Any | Generic property |
| `DROPDOWN_PROPERTY` | DROPDOWN | Selected index, Options |
| `IMAGE_PROPERTY` | IMAGE | Asset, Rotation, Scale |
| `LABEL_PROPERTY` | LABEL | Text ✅ confirmed |
| `ROLLER_PROPERTY` | ROLLER | Selected index |
| `SLIDER_PROPERTY` | SLIDER | Value |

#### Complete Action Summary (24 user-facing actions)

| Category | Actions | Confirmed |
|----------|--------|:---:|
| Navigation | CHANGE SCREEN, DELETE SCREEN | ✅, — |
| Code | CALL FUNCTION | ✅ |
| Animation | PLAY ANIMATION, SET OPACITY | ✅, ✅ |
| Value Increment | INCREMENT ARC, INCREMENT BAR, INCREMENT SLIDER | ✅, —, — |
| Property Setting | LABEL_PROPERTY, SLIDER_PROPERTY, BAR_PROPERTY, DROPDOWN_PROPERTY, IMAGE_PROPERTY, ROLLER_PROPERTY, BASIC_PROPERTY | ✅, ✅, — |
| Text Display | SET TEXT VALUE FROM ARC, SET TEXT VALUE FROM SLIDER, SET TEXT VALUE WHEN CHECKED | ✅, ✅, ✅ |
| State/Flag | MODIFY FLAG, MODIFY STATE | ✅, ✅ |
| Keyboard | KEYBOARD SET TARGET, MOVE CURSOR | —, — |
| Other | STEP SPINBOX, SWITCH THEME | —, — |

## Screen Transition Fade Modes

| Mode | Description |
|------|-------------|
| `NONE` | Instant switch |
| `FADE_ON` | New screen fades in ✅ confirmed |
| `FADE_IN` | Alias for FADE_ON |
| `MOVE_LEFT` | Both screens push left ✅ confirmed |
| `MOVE_RIGHT` | Both screens push right ✅ confirmed |
| `MOVE_TOP` | Both screens push up |
| `MOVE_BOTTOM` | Both screens push down |
| `OVER_LEFT` | New screen slides over from left |
| `OVER_RIGHT` | New screen slides over from right |
| `OVER_TOP` | New screen slides over from top |
| `OVER_BOTTOM` | New screen slides over from bottom |
