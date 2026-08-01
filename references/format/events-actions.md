# Events and Actions

This document describes the event structure, trigger types, action types, and screen transition fade modes used in SquareLine Studio.

All Call/CallC templates below are verified against decoded `.internal_ref` descriptors from SLS v1.6.1 (LVGL v9).

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

| Trigger | Description | Source |
|---------|-------------|:---:|
| `CLICKED` | Short press and release | ✅ |
| `PRESSED` | Immediately on press | ✅ |
| `RELEASED` | On release | ✅ |
| `PRESS_LOST` | Press followed by pointer leaving widget | ✅ |
| `LONG_PRESSED` | After long press threshold | internal_ref |
| `LONG_PRESSED_REPEAT` | Repeated after long press | internal_ref |
| `SHORT_CLICKED` | Short click detected | internal_ref |
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
| `FOCUSED` | Widget gains focus | internal_ref |
| `DEFOCUSED` | Widget loses focus | internal_ref |
| `READY` | Process completed | internal_ref |
| `CANCEL` | Process cancelled | internal_ref |
| `KEY` | Key input received | internal_ref |
| `KEY_RIGHT(KEY)` | Right key pressed | internal_ref |
| `KEY_LEFT(KEY)` | Left key pressed | internal_ref |
| `KEY_UP(KEY)` | Up key pressed | internal_ref |
| `KEY_DOWN(KEY)` | Down key pressed | internal_ref |
| `KEY_NEXT(KEY)` | Next key (tab) | internal_ref |
| `KEY_PREV(KEY)` | Previous key (shift+tab) | internal_ref |
| `KEY_ENTER(KEY)` | Enter key pressed | internal_ref |
| `KEY_ESC(KEY)` | Escape key pressed | internal_ref |
| `EDITED` | Text content modified | internal_ref |
| `INSERT` | Text inserted | internal_ref |

> [!NOTE]
> ✅ = confirmed in SLS example projects. internal_ref = confirmed from decoded `.internal_ref` descriptors.
> Compound triggers like `CHECKED(VALUE_CHANGED)` and `KEY_RIGHT(KEY)` use SLS-specific
> naming. The parenthesized suffix indicates the underlying LVGL event type.

## Event Action Types

### Navigation Actions

#### CHANGE SCREEN ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "CHANGE SCREEN",
  "childs": [
    { "strtype": "CHANGE SCREEN/Name", "strval": "CHANGE SCREEN" },
    { "strtype": "CHANGE SCREEN/Call", "strval": "ChangeScreen( <{Screen_to}>, lv.SCR_LOAD_ANIM.<{Fade_mode}>, <{Speed}>, <{Delay}>)" },
    { "strtype": "CHANGE SCREEN/CallC", "strval": "_ui_screen_change( &<{Screen_to}>, LV_SCR_LOAD_ANIM_<{Fade_mode}>, <{Speed}>, <{Delay}>, &<{Screen_to}>_screen_init);" },
    { "strtype": "CHANGE SCREEN/Screen_to", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "CHANGE SCREEN/Fade_mode", "strval": "FADE_ON", "InheritedType": 3 },
    { "strtype": "CHANGE SCREEN/Speed", "strval": "500", "InheritedType": 6 },
    { "strtype": "CHANGE SCREEN/Delay", "strval": "0", "InheritedType": 6 }
  ]
}
```
Fade_mode choices: `MOVE_LEFT`, `MOVE_RIGHT`, `MOVE_TOP`, `MOVE_BOTTOM`, `OVER_LEFT`, `OVER_RIGHT`, `OVER_TOP`, `OVER_BOTTOM`, `FADE_ON`, `FADE_OUT`, `OUT_LEFT`, `OUT_RIGHT`, `OUT_TOP`, `OUT_BOTTOM`, `NONE`

#### DELETE SCREEN — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "DELETE SCREEN",
  "childs": [
    { "strtype": "DELETE SCREEN/Name", "strval": "DELETE SCREEN" },
    { "strtype": "DELETE SCREEN/Call", "strval": "DeleteScreen(<{Screen}>)" },
    { "strtype": "DELETE SCREEN/CallC", "strval": "_ui_screen_delete( &<{Screen}>_screen_destroy);" },
    { "strtype": "DELETE SCREEN/Screen", "strval": "GUID...", "InheritedType": 9 }
  ]
}
```

### Code Actions

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

### Animation Actions

#### PLAY ANIMATION ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "PLAY ANIMATION",
  "childs": [
    { "strtype": "PLAY ANIMATION/Name", "strval": "PLAY ANIMATION" },
    { "strtype": "PLAY ANIMATION/Call", "strval": "<{FunctionName}>(<{Target}>, <{Delay}>)" },
    { "strtype": "PLAY ANIMATION/CallC", "strval": "<{FunctionName}>(<{Target}>, <{Delay}>);" },
    { "strtype": "PLAY ANIMATION/FunctionName", "strval": "AnimFuncOfSample" },
    { "strtype": "PLAY ANIMATION/Animation", "strval": "\"SampleEloAnimation\"", "InheritedType": 8 },
    { "strtype": "PLAY ANIMATION/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "PLAY ANIMATION/Delay", "strval": "0", "InheritedType": 6 }
  ]
}
```

#### SET OPACITY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "SET OPACITY",
  "childs": [
    { "strtype": "SET OPACITY/Name", "strval": "SET OPACITY" },
    { "strtype": "SET OPACITY/Call", "strval": "set_opacity( <{Target}>, <{Value}>)" },
    { "strtype": "SET OPACITY/CallC", "strval": "_ui_opacity_set( <{Target}>, <{Value}>);" },
    { "strtype": "SET OPACITY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET OPACITY/Value", "strval": "100", "InheritedType": 6 }
  ]
}
```

### Value Increment Actions

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

#### INCREMENT BAR — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "INCREMENT BAR",
  "childs": [
    { "strtype": "INCREMENT BAR/Name", "strval": "INCREMENT BAR", "InheritedType": 10 },
    { "strtype": "INCREMENT BAR/Call", "strval": "IncrementBar( <{Target}>, <{Value}>, LV_ANIM_<{Animate}> )", "InheritedType": 10 },
    { "strtype": "INCREMENT BAR/CallC", "strval": "_ui_bar_increment( <{Target}>, <{Value}>, LV_ANIM_<{Animate}>);", "InheritedType": 10 },
    { "strtype": "INCREMENT BAR/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "INCREMENT BAR/Value", "integer": 1, "InheritedType": 6 },
    { "strtype": "INCREMENT BAR/Animate", "strval": "ON", "InheritedType": 3 }
  ]
}
```
Animate choices: `ON`, `OFF`

> [!NOTE]
> INCREMENT BAR and INCREMENT SLIDER have an `Animate` parameter that INCREMENT ARC does not.
> This controls whether the value change is animated (`LV_ANIM_ON`) or instant (`LV_ANIM_OFF`).

#### INCREMENT SLIDER — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "INCREMENT SLIDER",
  "childs": [
    { "strtype": "INCREMENT SLIDER/Name", "strval": "INCREMENT SLIDER", "InheritedType": 10 },
    { "strtype": "INCREMENT SLIDER/Call", "strval": "IncrementSlider( <{Target}>, <{Value}>, LV_ANIM_<{Animate}> )", "InheritedType": 10 },
    { "strtype": "INCREMENT SLIDER/CallC", "strval": "_ui_slider_increment( <{Target}>, <{Value}>, LV_ANIM_<{Animate}>);", "InheritedType": 10 },
    { "strtype": "INCREMENT SLIDER/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "INCREMENT SLIDER/Value", "integer": 1, "InheritedType": 6 },
    { "strtype": "INCREMENT SLIDER/Animate", "strval": "ON", "InheritedType": 3 }
  ]
}
```
Animate choices: `ON`, `OFF`

### State/Flag Actions

#### MODIFY FLAG — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "MODIFY FLAG",
  "childs": [
    { "strtype": "MODIFY FLAG/Name", "strval": "MODIFY FLAG", "InheritedType": 10 },
    { "strtype": "MODIFY FLAG/Call", "strval": "ModifyFlag( <{Object}>, lv.obj.FLAG.<{Flag}>, \"<{Action}>\")", "InheritedType": 10 },
    { "strtype": "MODIFY FLAG/CallC", "strval": "_ui_flag_modify( <{Object}>, LV_OBJ_FLAG_<{Flag}>, _UI_MODIFY_FLAG_<{Action}>);", "InheritedType": 10 },
    { "strtype": "MODIFY FLAG/Object", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "MODIFY FLAG/Flag", "strval": "HIDDEN", "InheritedType": 3 },
    { "strtype": "MODIFY FLAG/Action", "strval": "ADD", "InheritedType": 3 }
  ]
}
```
Flag choices: `HIDDEN`, `CLICKABLE`, `CHECKABLE`, `PRESS_LOCK`, `CLICK_FOCUSABLE`, `ADV_HITTEST`, `IGNORE_LAYOUT`, `FLOATING`, `EVENT_BUBBLE`, `GESTURE_BUBBLE`, `SNAPPABLE`, `SCROLLABLE`, `SCROLL_ELASTIC`, `SCROLL_MOMENTUM`, `SCROLL_ON_FOCUS`, `SCROLL_CHAIN`, `SCROLL_ONE`

Action choices: `ADD`, `REMOVE`, `TOGGLE`

#### MODIFY STATE — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "MODIFY STATE",
  "childs": [
    { "strtype": "MODIFY STATE/Name", "strval": "MODIFY STATE", "InheritedType": 10 },
    { "strtype": "MODIFY STATE/Call", "strval": "ModifyState( <{Object}>, lv.STATE.<{State}>, \"<{Action}>\")", "InheritedType": 10 },
    { "strtype": "MODIFY STATE/CallC", "strval": "_ui_state_modify( <{Object}>, LV_STATE_<{State}>, _UI_MODIFY_STATE_<{Action}>);", "InheritedType": 10 },
    { "strtype": "MODIFY STATE/Object", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "MODIFY STATE/State", "strval": "CHECKED", "InheritedType": 3 },
    { "strtype": "MODIFY STATE/Action", "strval": "ADD", "InheritedType": 3 }
  ]
}
```
State choices: `CHECKED`, `DISABLED`, `PRESSED`, `FOCUSED`, `USER_1`, `USER_2`, `USER_3`, `USER_4`

Action choices: `ADD`, `REMOVE`, `TOGGLE`

### Text Display Actions

#### SET TEXT VALUE FROM ARC — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "SET TEXT VALUE FROM ARC",
  "childs": [
    { "strtype": "SET TEXT VALUE FROM ARC/Name", "strval": "SET TEXT VALUE FROM ARC", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/Call", "strval": "SetTextValueArc( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\")", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/CallC", "strval": "_ui_arc_set_text_value( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\");", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET TEXT VALUE FROM ARC/Prefix", "strval": "", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/Postfix", "strval": "", "InheritedType": 10 }
  ]
}
```

> [!NOTE]
> The `target` in the Call/CallC template refers to the **event source widget** (the arc/slider/switch
> that triggered the event), not a separate parameter. `Target` is the label to update.

#### SET TEXT VALUE FROM SLIDER — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "SET TEXT VALUE FROM SLIDER",
  "childs": [
    { "strtype": "SET TEXT VALUE FROM SLIDER/Name", "strval": "SET TEXT VALUE FROM SLIDER", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Call", "strval": "SetTextValueSlider( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\")", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/CallC", "strval": "_ui_slider_set_text_value( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\");", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Prefix", "strval": "", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Postfix", "strval": "", "InheritedType": 10 }
  ]
}
```

#### SET TEXT VALUE WHEN CHECKED — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "SET TEXT VALUE WHEN CHECKED",
  "childs": [
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Name", "strval": "SET TEXT VALUE WHEN CHECKED", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Call", "strval": "SetTextValueChecked( <{Target}>, target, \"<{On_text}>\", \"<{Off_text}>\")", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/CallC", "strval": "_ui_checked_set_text_value( <{Target}>, target, \"<{On_text}>\", \"<{Off_text}>\");", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/On_text", "strval": "", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Off_text", "strval": "", "InheritedType": 10 }
  ]
}
```

### Keyboard Actions

#### KEYBOARD SET TARGET — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "KEYBOARD SET TARGET",
  "childs": [
    { "strtype": "KEYBOARD SET TARGET/Name", "strval": "KEYBOARD SET TARGET", "InheritedType": 10 },
    { "strtype": "KEYBOARD SET TARGET/Call", "strval": "KeyboardSetTarget( <{Keyboard}>,  <{TextArea}>)", "InheritedType": 10 },
    { "strtype": "KEYBOARD SET TARGET/CallC", "strval": "_ui_keyboard_set_target(<{Keyboard}>,  <{TextArea}>);", "InheritedType": 10 },
    { "strtype": "KEYBOARD SET TARGET/Keyboard", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "KEYBOARD SET TARGET/TextArea", "strval": "GUID...", "InheritedType": 9 }
  ]
}
```

#### MOVE CURSOR — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "MOVE CURSOR",
  "childs": [
    { "strtype": "MOVE CURSOR/Name", "strval": "MOVE CURSOR", "InheritedType": 10 },
    { "strtype": "MOVE CURSOR/Call", "strval": "TextAreaMoveCursor( <{Target}>, \"<{Direction}>\" )", "InheritedType": 10 },
    { "strtype": "MOVE CURSOR/CallC", "strval": "_ui_textarea_move_cursor( <{Target}>, UI_MOVE_CURSOR_<{Direction}>);", "InheritedType": 10 },
    { "strtype": "MOVE CURSOR/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "MOVE CURSOR/Direction", "strval": "RIGHT", "InheritedType": 3 }
  ]
}
```
Direction choices: `UP`, `RIGHT`, `DOWN`, `LEFT`

### Other Actions

#### STEP SPINBOX — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "STEP SPINBOX",
  "childs": [
    { "strtype": "STEP SPINBOX/Name", "strval": "STEP SPINBOX", "InheritedType": 10 },
    { "strtype": "STEP SPINBOX/Call", "strval": "StepSpinbox( <{Target}>, <{Direction}> )", "InheritedType": 10 },
    { "strtype": "STEP SPINBOX/CallC", "strval": "_ui_spinbox_step( <{Target}>, <{Direction}>);", "InheritedType": 10 },
    { "strtype": "STEP SPINBOX/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "STEP SPINBOX/Direction", "strval": "1", "InheritedType": 3 }
  ]
}
```
Direction choices: `1(INCREMENT)`, `-1(DECREMENT)`

#### SWITCH THEME — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "SWITCH THEME",
  "childs": [
    { "strtype": "SWITCH THEME/Name", "strval": "SWITCH THEME", "InheritedType": 10 },
    { "strtype": "SWITCH THEME/Call", "strval": "SwitchTheme( <{Theme}> )", "InheritedType": 10 },
    { "strtype": "SWITCH THEME/CallC", "strval": "_ui_switch_theme( <{Theme}> );", "InheritedType": 10 },
    { "strtype": "SWITCH THEME/Theme", "strval": "", "InheritedType": 10 }
  ]
}
```

### Property-Setting Actions

#### LABEL_PROPERTY ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "LABEL_PROPERTY",
  "childs": [
    { "strtype": "LABEL_PROPERTY/Name", "strval": "LABEL_PROPERTY", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/Call", "strval": "SetLabelProperty(<{Target}>, '<{Property}>', '<{Value}>')", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/CallC", "strval": "_ui_label_set_property(<{Target}>, _UI_LABEL_PROPERTY_<{Property}>, \"<{Value}>\");", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "LABEL_PROPERTY/Property", "strval": "Text", "InheritedType": 3 },
    { "strtype": "LABEL_PROPERTY/Value", "strval": "", "InheritedType": 10 }
  ]
}
```
Property choices: `Text`

#### BAR_PROPERTY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "BAR_PROPERTY",
  "childs": [
    { "strtype": "BAR_PROPERTY/Name", "strval": "BAR_PROPERTY", "InheritedType": 10 },
    { "strtype": "BAR_PROPERTY/Call", "strval": "SetBarProperty(<{Target}>, '<{Property}>', <{Value}>)", "InheritedType": 10 },
    { "strtype": "BAR_PROPERTY/CallC", "strval": "_ui_bar_set_property(<{Target}>, _UI_BAR_PROPERTY_<{Property}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "BAR_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "BAR_PROPERTY/Property", "strval": "Value_with_anim", "InheritedType": 3 },
    { "strtype": "BAR_PROPERTY/Value", "strval": "", "InheritedType": 10 }
  ]
}
```
Property choices: `Value_with_anim`, `Value`

#### SLIDER_PROPERTY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "SLIDER_PROPERTY",
  "childs": [
    { "strtype": "SLIDER_PROPERTY/Name", "strval": "SLIDER_PROPERTY", "InheritedType": 10 },
    { "strtype": "SLIDER_PROPERTY/Call", "strval": "SetSliderProperty(<{Target}>, '<{Property}>', <{Value}>)", "InheritedType": 10 },
    { "strtype": "SLIDER_PROPERTY/CallC", "strval": "_ui_slider_set_property(<{Target}>, _UI_SLIDER_PROPERTY_<{Property}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "SLIDER_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SLIDER_PROPERTY/Property", "strval": "Value_with_anim", "InheritedType": 3 },
    { "strtype": "SLIDER_PROPERTY/Value", "strval": "", "InheritedType": 10 }
  ]
}
```
Property choices: `Value_with_anim`, `Value`

#### DROPDOWN_PROPERTY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "DROPDOWN_PROPERTY",
  "childs": [
    { "strtype": "DROPDOWN_PROPERTY/Name", "strval": "DROPDOWN_PROPERTY", "InheritedType": 10 },
    { "strtype": "DROPDOWN_PROPERTY/Call", "strval": "SetDropdownProperty(<{Target}>, '<{Property}>', <{Value}>)", "InheritedType": 10 },
    { "strtype": "DROPDOWN_PROPERTY/CallC", "strval": "_ui_dropdown_set_property(<{Target}>, _UI_DROPDOWN_PROPERTY_<{Property}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "DROPDOWN_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "DROPDOWN_PROPERTY/Property", "strval": "Selected", "InheritedType": 3 },
    { "strtype": "DROPDOWN_PROPERTY/Value", "strval": "", "InheritedType": 6 }
  ]
}
```
Property choices: `Selected`

#### IMAGE_PROPERTY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "IMAGE_PROPERTY",
  "childs": [
    { "strtype": "IMAGE_PROPERTY/Name", "strval": "IMAGE_PROPERTY", "InheritedType": 10 },
    { "strtype": "IMAGE_PROPERTY/Call", "strval": "SetImageProperty(<{Target}>, '<{Property}>', <{Value}>, <{Value_}>)", "InheritedType": 10 },
    { "strtype": "IMAGE_PROPERTY/CallC", "strval": "_ui_image_set_property(<{Target}>, _UI_IMAGE_PROPERTY_<{Property}>,& <{Value}>);", "InheritedType": 10 },
    { "strtype": "IMAGE_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "IMAGE_PROPERTY/Property", "strval": "Image", "InheritedType": 3 },
    { "strtype": "IMAGE_PROPERTY/Value", "strval": "noimage", "InheritedType": 12 },
    { "strtype": "IMAGE_PROPERTY/Value_", "strval": "0", "InheritedType": 6 }
  ]
}
```
Property choices: `Image`, `Angle`, `Zoom`

#### ROLLER_PROPERTY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "ROLLER_PROPERTY",
  "childs": [
    { "strtype": "ROLLER_PROPERTY/Name", "strval": "ROLLER_PROPERTY", "InheritedType": 10 },
    { "strtype": "ROLLER_PROPERTY/Call", "strval": "SetRollerProperty(<{Target}>, '<{Property}>', <{Value}>)", "InheritedType": 10 },
    { "strtype": "ROLLER_PROPERTY/CallC", "strval": "_ui_roller_set_property(<{Target}>, _UI_ROLLER_PROPERTY_<{Property}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "ROLLER_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "ROLLER_PROPERTY/Property", "strval": "Selected_with_anim", "InheritedType": 3 },
    { "strtype": "ROLLER_PROPERTY/Value", "strval": "", "InheritedType": 10 }
  ]
}
```
Property choices: `Selected_with_anim`, `Selected`

#### BASIC_PROPERTY — internal_ref confirmed
```json
{
  "strtype": "_event/action", "strval": "BASIC_PROPERTY",
  "childs": [
    { "strtype": "BASIC_PROPERTY/Name", "strval": "BASIC_PROPERTY", "InheritedType": 10 },
    { "strtype": "BASIC_PROPERTY/Call", "strval": "SetPanelProperty(<{Target}>, '<{Property}>', <{Value}>)", "InheritedType": 10 },
    { "strtype": "BASIC_PROPERTY/CallC", "strval": "_ui_basic_set_property(<{Target}>, _UI_BASIC_PROPERTY_<{Property}>,  <{Value}>);", "InheritedType": 10 },
    { "strtype": "BASIC_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "BASIC_PROPERTY/Property", "strval": "Position_X", "InheritedType": 3 },
    { "strtype": "BASIC_PROPERTY/Value", "strval": "0", "InheritedType": 6 }
  ]
}
```
Property choices: `Position_X`, `Position_Y`, `Width`, `Height`

### Complete Action Summary (24 user-facing actions)

| Category | Actions | Source |
|----------|--------|:---:|
| Navigation | CHANGE SCREEN, DELETE SCREEN | ✅, internal_ref |
| Code | CALL FUNCTION | ✅ |
| Animation | PLAY ANIMATION, SET OPACITY | ✅, internal_ref |
| Value Increment | INCREMENT ARC, INCREMENT BAR, INCREMENT SLIDER | ✅, internal_ref, internal_ref |
| Property Setting | LABEL_PROPERTY, SLIDER_PROPERTY, BAR_PROPERTY, DROPDOWN_PROPERTY, IMAGE_PROPERTY, ROLLER_PROPERTY, BASIC_PROPERTY | ✅, internal_ref |
| Text Display | SET TEXT VALUE FROM ARC, SET TEXT VALUE FROM SLIDER, SET TEXT VALUE WHEN CHECKED | internal_ref |
| State/Flag | MODIFY FLAG, MODIFY STATE | internal_ref |
| Keyboard | KEYBOARD SET TARGET, MOVE CURSOR | internal_ref |
| Other | STEP SPINBOX, SWITCH THEME | internal_ref |

## Screen Transition Fade Modes

| Mode | Description |
|------|-------------|
| `NONE` | Instant switch |
| `FADE_ON` | New screen fades in ✅ confirmed |
| `FADE_OUT` | Current screen fades out |
| `MOVE_LEFT` | Both screens push left ✅ confirmed |
| `MOVE_RIGHT` | Both screens push right ✅ confirmed |
| `MOVE_TOP` | Both screens push up |
| `MOVE_BOTTOM` | Both screens push down |
| `OVER_LEFT` | New screen slides over from left |
| `OVER_RIGHT` | New screen slides over from right |
| `OVER_TOP` | New screen slides over from top |
| `OVER_BOTTOM` | New screen slides over from bottom |
| `OUT_LEFT` | Current screen slides out to left |
| `OUT_RIGHT` | Current screen slides out to right |
| `OUT_TOP` | Current screen slides out to top |
| `OUT_BOTTOM` | Current screen slides out to bottom |
