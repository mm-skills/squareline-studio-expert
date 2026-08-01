# Interactive Widgets

## Button
**Common patterns:** Buttons themselves do not have text. You must create a Label widget and set it as a child of the Button to give it text. Center the label (`Align="CENTER"`).
**PRESSED state styling:**
To add a visual effect on press, define a `PRESSED` stylestate in `Style_main`:
```json
{
  "strtype": "_stylestate/state",
  "strval": "PRESSED",
  "childs": [
    {
      "nid": 1055, "strtype": "_style/Bg_Color",
      "intarray": [0, 80, 180, 255], "InheritedType": 7
    }
  ]
}
```

## ImgButton
**Typical use case:** A button that changes its asset based on state (released, pressed, checked).
**Image states:**
Must provide assets for each state explicitly:
```json
{
  "nid": 1020, "strtype": "IMGBUTTON/Button_state", "strval": "RELEASED", "InheritedType": 3
},
{
  "nid": 1030, "strtype": "IMGBUTTON/Image_released", "strval": "assets/btn_rel.png", "InheritedType": 5
},
{
  "nid": 1040, "strtype": "IMGBUTTON/Image_pressed", "strval": "assets/btn_pr.png", "InheritedType": 5
}
```

## Textarea
**Typical use case:** User text input field.
**Textarea properties:**
```json
{
  "nid": 1020, "strtype": "TEXTAREA/Text", "strval": "", "InheritedType": 10
},
{
  "nid": 1030, "strtype": "TEXTAREA/Placeholder", "strval": "Enter text...", "InheritedType": 10
},
{
  "nid": 1040, "strtype": "TEXTAREA/Accepted_characters", "strval": "", "InheritedType": 10
},
{
  "nid": 1050, "strtype": "TEXTAREA/Max_text_length", "integer": 98989898, "InheritedType": 6
},
{
  "nid": 1060, "strtype": "TEXTAREA/One_line_mode", "strval": "True", "InheritedType": 2
},
{
  "nid": 1070, "strtype": "TEXTAREA/Password_mode", "strval": "False", "InheritedType": 2
}
```

## Keyboard
**Typical use case:** On-screen virtual keyboard for Textarea input.
**Keyboard target_textarea linking:**
You must link the Keyboard to a specific Textarea using its GUID, or set it to `"-"` if handled dynamically in code.
```json
{
  "nid": 1010, "strtype": "KEYBOARD/Mode", "strval": "TEXT_LOWER", "InheritedType": 3
},
{
  "nid": 1020, "strtype": "KEYBOARD/Target_textarea", "strval": "GUID12345678-123456S1234567", "InheritedType": 9
}
```

## Colorwheel
**Typical use case:** Picking a color hue, saturation, or value.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "COLORWHEEL/Mode", "strval": "HUE", "InheritedType": 3
},
{
  "nid": 1020, "strtype": "COLORWHEEL/Fixed_mode", "strval": "False", "InheritedType": 2
}
```
**Style parts:** `Style_main` (MAIN), `Style_knob` (KNOB)
