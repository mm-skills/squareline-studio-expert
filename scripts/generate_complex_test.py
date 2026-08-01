#!/usr/bin/env python3
"""
Generate a complex SquareLine Studio test project that exercises:
- 3 screens with cross-screen navigation
- Multiple widget types (Button, Label, Slider, Arc, Switch, Checkbox, Bar, Dropdown)
- FLEX layout on a panel
- Custom styles (colors, borders, padding, opacity)
- Events: CHANGE SCREEN, CALL FUNCTION, LABEL_PROPERTY, INCREMENT ARC
- Style states (PRESSED on buttons)
"""
import json
import os
import random
from datetime import datetime


NID_COUNTER = 1000400  # Start high to avoid clashes with default nids


def next_nid():
    global NID_COUNTER
    NID_COUNTER += 1
    return NID_COUNTER


def guid():
    a = random.randint(10000000, 99999999)
    b = random.randint(100000, 999999)
    c = random.randint(1000000, 9999999)
    return f"GUID{a}-{b}S{c}"


def base_props(name, x, y, w, h, align="CENTER"):
    """Standard object properties every widget needs."""
    return [
        {"nid": 10, "strtype": "OBJECT/Name", "strval": name, "InheritedType": 10},
        {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
        {
            "Flow": 0, "Wrap": False, "Reversed": False,
            "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
            "LayoutType": 0, "nid": 30, "strtype": "OBJECT/Layout_type",
            "strval": "No_layout", "InheritedType": 13
        },
        {"nid": 40, "strtype": "OBJECT/Transform", "InheritedType": 1},
        {"nid": 50, "flags": 17, "strtype": "OBJECT/Position", "intarray": [x, y], "InheritedType": 7},
        {"nid": 60, "flags": 17, "strtype": "OBJECT/Size", "intarray": [w, h], "InheritedType": 7},
        {"nid": 70, "strtype": "OBJECT/Align", "strval": align, "InheritedType": 3},
        {"nid": 75, "strtype": "OBJECT/Extend_click_area", "InheritedType": 6},
        {"nid": 90, "flags": 1048576, "strtype": "OBJECT/Flags", "InheritedType": 1},
        {"nid": 225, "flags": 1048576, "strtype": "OBJECT/Scrolling", "InheritedType": 1},
        {"nid": 230, "strtype": "OBJECT/Scrollable", "strval": "False", "InheritedType": 2},
        {"nid": 300, "strtype": "OBJECT/Scrollbar_mode", "strval": "AUTO", "InheritedType": 3},
        {"nid": 310, "strtype": "OBJECT/Scroll_direction", "strval": "ALL", "InheritedType": 3},
        {"nid": 314, "strtype": "OBJECT/Scroll_snap_x", "strval": "NONE", "InheritedType": 3},
        {"nid": 315, "strtype": "OBJECT/Scroll_snap_y", "strval": "NONE", "InheritedType": 3},
        {"nid": 320, "flags": 1048576, "strtype": "OBJECT/States", "InheritedType": 1},
    ]


def flex_layout_props(flow=0, wrap=False):
    """Return a Layout_type property configured for FLEX."""
    return {
        "Flow": flow, "Wrap": wrap, "Reversed": False,
        "MainAlignment": 0, "CrossAlignment": 1, "TrackAlignment": 0,
        "LayoutType": 1, "nid": 30, "strtype": "OBJECT/Layout_type",
        "strval": "No_layout", "InheritedType": 13
    }


def style_part(prefix, part_name, part_label, nid, childs=None):
    """Create a style part property."""
    return {
        "part": f"lv.PART.{part_name}",
        "childs": childs or [],
        "nid": nid,
        "strtype": f"{prefix}/Style_{part_label}",
        "strval": f"lv.PART.{part_name}, Rectangle, Pad, Text",
        "InheritedType": 11
    }


def style_state_with_bg(state, r, g, b, a=255):
    """Create a style state with a background color."""
    return {
        "strtype": "_stylestate/state",
        "strval": state,
        "childs": [
            {"nid": next_nid(), "strtype": "_style/Bg_Color",
             "intarray": [r, g, b, a], "InheritedType": 7}
        ]
    }


def style_state_full(state, bg_color, border_color=None, border_width=None,
                     text_color=None, bg_radius=None, padding=None):
    """Create a style state with multiple properties."""
    childs = [
        {"nid": next_nid(), "strtype": "_style/Bg_Color",
         "intarray": bg_color, "InheritedType": 7}
    ]
    if border_color:
        childs.append({"nid": next_nid(), "strtype": "_style/Border_Color",
                       "intarray": border_color, "InheritedType": 7})
    if border_width is not None:
        childs.append({"nid": next_nid(), "strtype": "_style/Border width",
                       "integer": border_width, "InheritedType": 6})
    if text_color:
        childs.append({"nid": next_nid(), "strtype": "_style/Text_Color",
                       "intarray": text_color, "InheritedType": 7})
    if bg_radius is not None:
        childs.append({"nid": next_nid(), "strtype": "_style/Bg_Radius",
                       "integer": bg_radius, "InheritedType": 6})
    if padding:
        childs.append({"nid": next_nid(), "strtype": "_style/Padding",
                       "intarray": padding, "InheritedType": 7})
    return {"strtype": "_stylestate/state", "strval": state, "childs": childs}


def event_change_screen(target_guid, fade="FADE_ON", speed=500, delay=0, event_name="Nav"):
    """Create a CHANGE SCREEN event handler."""
    n = next_nid
    return {
        "disabled": False, "nid": n(), "strtype": "_event/EventHandler",
        "strval": "CLICKED",
        "childs": [
            {"nid": n(), "strtype": "_event/name", "strval": event_name, "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_C", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_P", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/action", "strval": "CHANGE SCREEN",
             "childs": [
                 {"nid": n(), "strtype": "CHANGE SCREEN/Name", "strval": "CHANGE SCREEN", "InheritedType": 10},
                 {"nid": n(), "strtype": "CHANGE SCREEN/Call",
                  "strval": "ChangeScreen( <{Screen_to}>, lv.SCR_LOAD_ANIM.<{Fade_mode}>, <{Speed}>, <{Delay}>)",
                  "InheritedType": 10},
                 {"nid": n(), "strtype": "CHANGE SCREEN/CallC",
                  "strval": "_ui_screen_change( &<{Screen_to}>, LV_SCR_LOAD_ANIM_<{Fade_mode}>, <{Speed}>, <{Delay}>, &<{Screen_to}>_screen_init);",
                  "InheritedType": 10},
                 {"nid": n(), "strtype": "CHANGE SCREEN/Screen_to", "strval": target_guid, "InheritedType": 9},
                 {"nid": n(), "strtype": "CHANGE SCREEN/Fade_mode", "strval": fade, "InheritedType": 3},
                 {"nid": n(), "strtype": "CHANGE SCREEN/Speed", "integer": speed, "InheritedType": 6},
                 {"nid": n(), "strtype": "CHANGE SCREEN/Delay", "InheritedType": 6},
             ], "InheritedType": 10},
        ], "InheritedType": 4
    }


def event_call_function(func_name, event_name="FuncEvent"):
    """Create a CALL FUNCTION event handler."""
    n = next_nid
    return {
        "disabled": False, "nid": n(), "strtype": "_event/EventHandler",
        "strval": "CLICKED",
        "childs": [
            {"nid": n(), "strtype": "_event/name", "strval": event_name, "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_C", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_P", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/action", "strval": "CALL FUNCTION",
             "childs": [
                 {"nid": n(), "strtype": "CALL FUNCTION/Name", "strval": "CALL FUNCTION", "InheritedType": 10},
                 {"nid": n(), "strtype": "CALL FUNCTION/Call",
                  "strval": "<{Function_name}>( )", "InheritedType": 10},
                 {"nid": n(), "strtype": "CALL FUNCTION/CallC",
                  "strval": "<{Function_name}>(e);", "InheritedType": 10},
                 {"nid": n(), "strtype": "CALL FUNCTION/Function_name",
                  "strval": func_name, "InheritedType": 10},
             ], "InheritedType": 10},
        ], "InheritedType": 4
    }


def event_label_property(target_guid, value, event_name="SetLabel"):
    """Create a LABEL_PROPERTY event handler."""
    n = next_nid
    return {
        "disabled": False, "nid": n(), "strtype": "_event/EventHandler",
        "strval": "CLICKED",
        "childs": [
            {"nid": n(), "strtype": "_event/name", "strval": event_name, "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_C", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_P", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/action", "strval": "LABEL_PROPERTY",
             "childs": [
                 {"nid": n(), "strtype": "LABEL_PROPERTY/Name", "strval": "LABEL_PROPERTY", "InheritedType": 10},
                 {"nid": n(), "strtype": "LABEL_PROPERTY/Call",
                  "strval": "SetLabelProperty(<{Target}>, '<{Property}>', '<{Value}>')", "InheritedType": 10},
                 {"nid": n(), "strtype": "LABEL_PROPERTY/CallC",
                  "strval": '_ui_label_set_property(<{Target}>, _UI_LABEL_PROPERTY_<{Property}>, "<{Value}>");',
                  "InheritedType": 10},
                 {"nid": n(), "strtype": "LABEL_PROPERTY/Target", "strval": target_guid, "InheritedType": 9},
                 {"nid": n(), "strtype": "LABEL_PROPERTY/Property", "strval": "Text", "InheritedType": 3},
                 {"nid": n(), "strtype": "LABEL_PROPERTY/Value", "strval": value, "InheritedType": 10},
             ], "InheritedType": 10},
        ], "InheritedType": 4
    }


def event_increment_arc(target_guid, increment=10, trigger="VALUE_CHANGED", event_name="IncArc"):
    """Create an INCREMENT ARC event handler."""
    n = next_nid
    return {
        "disabled": False, "nid": n(), "strtype": "_event/EventHandler",
        "strval": trigger,
        "childs": [
            {"nid": n(), "strtype": "_event/name", "strval": event_name, "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_C", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/condition_P", "strval": "", "InheritedType": 10},
            {"nid": n(), "strtype": "_event/action", "strval": "INCREMENT ARC",
             "childs": [
                 {"nid": n(), "strtype": "INCREMENT ARC/Name", "strval": "INCREMENT ARC", "InheritedType": 10},
                 {"nid": n(), "strtype": "INCREMENT ARC/Call",
                  "strval": "IncrementArc( <{Target}>, <{Value}> )", "InheritedType": 10},
                 {"nid": n(), "strtype": "INCREMENT ARC/CallC",
                  "strval": "_ui_arc_increment( <{Target}>, <{Value}>);", "InheritedType": 10},
                 {"nid": n(), "strtype": "INCREMENT ARC/Target", "strval": target_guid, "InheritedType": 9},
                 {"nid": n(), "strtype": "INCREMENT ARC/Value", "integer": increment, "InheritedType": 6},
             ], "InheritedType": 10},
        ], "InheritedType": 4
    }


def make_screen(name, screen_guid, children=None):
    """Create a SCREEN widget."""
    return {
        "guid": screen_guid,
        "children": children or [],
        "isPage": True,
        "properties": [
            {"nid": 10, "strtype": "OBJECT/Name", "strval": name, "InheritedType": 10},
            {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0, "nid": 30, "strtype": "OBJECT/Layout_type",
                "strval": "No_layout", "InheritedType": 13
            },
            {"nid": 40, "strtype": "OBJECT/Transform", "InheritedType": 1},
            {"nid": 90, "flags": 1048576, "strtype": "OBJECT/Flags", "InheritedType": 1},
            {"nid": 225, "flags": 1048576, "strtype": "OBJECT/Scrolling", "InheritedType": 1},
            {"nid": 230, "strtype": "OBJECT/Scrollable", "strval": "False", "InheritedType": 2},
            {"nid": 300, "strtype": "OBJECT/Scrollbar_mode", "strval": "AUTO", "InheritedType": 3},
            {"nid": 310, "strtype": "OBJECT/Scroll_direction", "strval": "ALL", "InheritedType": 3},
            {"nid": 314, "strtype": "OBJECT/Scroll_snap_x", "strval": "NONE", "InheritedType": 3},
            {"nid": 315, "strtype": "OBJECT/Scroll_snap_y", "strval": "NONE", "InheritedType": 3},
            {"nid": 320, "flags": 1048576, "strtype": "OBJECT/States", "InheritedType": 1},
            {"nid": 1010, "strtype": "SCREEN/Screen", "InheritedType": 1},
            {"nid": 1020, "strtype": "SCREEN/Temporary", "strval": "False", "InheritedType": 2},
            style_part("SCREEN", "MAIN", "main", 1040),
            style_part("SCREEN", "SCROLLBAR", "scrollbar", 1050),
        ],
        "saved_objtypeKey": "SCREEN"
    }


def make_button(name, x, y, w, h, extra_props=None):
    props = base_props(name, x, y, w, h)
    props.append(style_part("BUTTON", "MAIN", "main", 1010))
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "BUTTON"}


def make_label(name, text, x, y, w=None, h=None, extra_props=None):
    props = base_props(name, x, y, w or 100, h or 20)
    # Override size to content-fit
    for p in props:
        if p.get("strtype") == "OBJECT/Size":
            p["flags"] = 51  # Content-fit
    props.extend([
        {"nid": 1010, "strtype": "LABEL/Label", "InheritedType": 1},
        {"nid": 1020, "strtype": "LABEL/Text", "strval": text, "InheritedType": 10},
        {"nid": 1030, "strtype": "LABEL/Long_mode", "strval": "WRAP", "InheritedType": 3},
        {"nid": 1040, "strtype": "LABEL/Recolor", "strval": "False", "InheritedType": 2},
        style_part("LABEL", "MAIN", "main", 1050),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "LABEL"}


def make_slider(name, x, y, w, h, min_val=0, max_val=100, value=50, extra_props=None):
    props = base_props(name, x, y, w, h)
    props.extend([
        {"nid": 1010, "strtype": "SLIDER/Slider", "InheritedType": 1},
        {"nid": 1020, "flags": 16, "strtype": "SLIDER/Range", "intarray": [min_val, max_val], "InheritedType": 7},
        {"nid": 1030, "strtype": "SLIDER/Mode", "strval": "NORMAL", "InheritedType": 3},
        {"nid": 1040, "strtype": "SLIDER/Value", "integer": value, "InheritedType": 6},
        {"nid": 1050, "strtype": "SLIDER/Value_left", "InheritedType": 6},
        style_part("SLIDER", "MAIN", "main", 1060),
        style_part("SLIDER", "INDICATOR", "indicator", 1070),
        style_part("SLIDER", "KNOB", "knob", 1080),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "SLIDER"}


def make_arc(name, x, y, w, h, value=50, min_val=0, max_val=100, extra_props=None):
    props = base_props(name, x, y, w, h)
    props.extend([
        {"nid": 1010, "strtype": "ARC/Arc", "InheritedType": 1},
        {"nid": 1020, "strtype": "ARC/Value", "integer": value, "InheritedType": 6},
        {"nid": 1030, "flags": 16, "strtype": "ARC/Range", "intarray": [min_val, max_val], "InheritedType": 7},
        {"nid": 1040, "flags": 16, "strtype": "ARC/Bg_angles", "intarray": [135, 45], "InheritedType": 7},
        {"nid": 1050, "strtype": "ARC/Rotation", "InheritedType": 6},
        {"nid": 1060, "strtype": "ARC/Mode", "strval": "NORMAL", "InheritedType": 3},
        style_part("ARC", "MAIN", "main", 1070),
        style_part("ARC", "INDICATOR", "indicator", 1080),
        style_part("ARC", "KNOB", "knob", 1090),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "ARC"}


def make_switch(name, x, y, extra_props=None):
    props = base_props(name, x, y, 50, 25)
    props.extend([
        style_part("SWITCH", "MAIN", "main", 1010),
        style_part("SWITCH", "INDICATOR", "indicator", 1020),
        style_part("SWITCH", "KNOB", "knob", 1030),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "SWITCH"}


def make_checkbox(name, title, x, y, extra_props=None):
    props = base_props(name, x, y, 100, 20)
    for p in props:
        if p.get("strtype") == "OBJECT/Size":
            p["flags"] = 51
    props.extend([
        {"nid": 1010, "strtype": "CHECKBOX/Checkbox", "InheritedType": 1},
        {"nid": 1020, "strtype": "CHECKBOX/Title", "strval": title, "InheritedType": 10},
        style_part("CHECKBOX", "MAIN", "main", 1030),
        {
            "part": "lv.PART.INDICATOR", "childs": [],
            "nid": 1040, "strtype": "CHECKBOX/Style_bullet",
            "strval": "lv.PART.INDICATOR, Rectangle", "InheritedType": 11
        },
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "CHECKBOX"}


def make_bar(name, x, y, w, h, value=60, extra_props=None):
    props = base_props(name, x, y, w, h)
    props.extend([
        {"nid": 1010, "strtype": "BAR/Bar", "InheritedType": 1},
        {"nid": 1020, "strtype": "BAR/Value", "integer": value, "InheritedType": 6},
        {"nid": 1030, "strtype": "BAR/Value_start", "InheritedType": 6},
        {"nid": 1040, "flags": 16, "strtype": "BAR/Range", "intarray": [0, 100], "InheritedType": 7},
        {"nid": 1050, "strtype": "BAR/Mode", "strval": "NORMAL", "InheritedType": 3},
        style_part("BAR", "MAIN", "main", 1060),
        style_part("BAR", "INDICATOR", "indicator", 1070),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "BAR"}


def make_dropdown(name, options, x, y, w, h, extra_props=None):
    props = base_props(name, x, y, w, h)
    props.extend([
        {"nid": 1010, "strtype": "DROPDOWN/Dropdown", "InheritedType": 1},
        {"nid": 1020, "strtype": "DROPDOWN/Options", "strval": "\\n".join(options), "InheritedType": 10},
        {"nid": 1030, "strtype": "DROPDOWN/Base_text", "strval": "", "InheritedType": 10},
        {"nid": 1040, "strtype": "DROPDOWN/Show_selected", "strval": "True", "InheritedType": 2},
        {"nid": 1050, "strtype": "DROPDOWN/List_align", "strval": "BOTTOM", "InheritedType": 3},
        style_part("DROPDOWN", "MAIN", "main", 1060),
        style_part("DROPDOWN", "INDICATOR", "indicator", 1070),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": [], "properties": props, "saved_objtypeKey": "DROPDOWN"}


def make_panel(name, x, y, w, h, children=None, use_flex=False, extra_props=None):
    props = base_props(name, x, y, w, h)
    if use_flex:
        # Replace the layout_type with FLEX
        for i, p in enumerate(props):
            if p.get("strtype") == "OBJECT/Layout_type":
                props[i] = flex_layout_props(flow=0, wrap=True)
                break
    props.extend([
        style_part("PANEL", "MAIN", "main", 1010),
        style_part("PANEL", "SCROLLBAR", "scrollbar", 1020),
    ])
    if extra_props:
        props.extend(extra_props)
    return {"guid": guid(), "children": children or [], "properties": props, "saved_objtypeKey": "PANEL"}


def main():
    output_dir = "/tmp/sls_complex_test/"
    project_name = "ComplexTest"
    width, height = 480, 320

    # Pre-generate GUIDs for screens so we can cross-reference
    screen1_guid = guid()
    screen2_guid = guid()
    screen3_guid = guid()

    # Pre-generate GUID for the status label (so button can reference it)
    status_label = make_label("StatusLabel", "Ready", 0, 120)
    status_label_guid = status_label["guid"]

    # Pre-generate GUID for the arc (so increment button can reference it)
    arc_widget = make_arc("GaugeArc", 0, 0, 150, 150, value=25)
    arc_guid = arc_widget["guid"]

    # ==================== SCREEN 1: Dashboard ====================
    # Title
    title_label = make_label("TitleLabel", "Dashboard", 0, -140)

    # Navigation buttons with styled backgrounds and PRESSED state
    nav_btn_style = style_part("BUTTON", "MAIN", "main", 1010, childs=[
        style_state_full("DEFAULT",
                         bg_color=[0, 120, 215, 255],
                         border_color=[0, 80, 180, 255],
                         border_width=2,
                         text_color=[255, 255, 255, 255],
                         bg_radius=8),
        style_state_full("PRESSED",
                         bg_color=[0, 80, 180, 255],
                         text_color=[200, 220, 255, 255]),
    ])

    go_settings_btn = make_button("GoSettingsBtn", -120, 130, 120, 40)
    # Replace style with styled one and add nav event
    go_settings_btn["properties"] = [p for p in go_settings_btn["properties"]
                                     if p.get("strtype") != "BUTTON/Style_main"]
    go_settings_btn["properties"].append(nav_btn_style)
    go_settings_btn["properties"].append(
        event_change_screen(screen2_guid, "MOVE_LEFT", 400, event_name="GoSettings"))

    go_data_btn = make_button("GoDataBtn", 120, 130, 120, 40)
    go_data_btn["properties"] = [p for p in go_data_btn["properties"]
                                 if p.get("strtype") != "BUTTON/Style_main"]
    go_data_btn["properties"].append(nav_btn_style)
    go_data_btn["properties"].append(
        event_change_screen(screen3_guid, "MOVE_RIGHT", 400, event_name="GoData"))

    # Button labels (as children of buttons)
    settings_label = make_label("SettingsBtnLabel", "Settings", 0, 0)
    data_label = make_label("DataBtnLabel", "Data View", 0, 0)
    go_settings_btn["children"] = [settings_label]
    go_data_btn["children"] = [data_label]

    # Slider with value
    main_slider = make_slider("BrightnessSlider", 0, -60, 200, 10, 0, 100, 70)

    # Arc gauge
    # Already created above

    # Status label (already created above, referenced by button)

    # Increment arc button
    inc_arc_btn = make_button("IncArcBtn", 0, 80, 100, 35)
    inc_arc_btn["properties"].append(
        event_increment_arc(arc_guid, 15, "CLICKED", "IncrementGauge"))
    inc_btn_label = make_label("IncBtnLabel", "+15", 0, 0)
    inc_arc_btn["children"] = [inc_btn_label]

    # Set label button
    set_label_btn = make_button("SetLabelBtn", -120, 80, 100, 35)
    set_label_btn["properties"].append(
        event_label_property(status_label_guid, "Active!", "UpdateStatus"))
    set_lbl_label = make_label("SetLblBtnLabel", "Activate", 0, 0)
    set_label_btn["children"] = [set_lbl_label]

    # Call function button
    func_btn = make_button("CallFuncBtn", 120, 80, 100, 35)
    func_btn["properties"].append(
        event_call_function("onCustomAction", "CustomFunc"))
    func_btn_label = make_label("FuncBtnLabel", "Custom", 0, 0)
    func_btn["children"] = [func_btn_label]

    # Screen 1 with dark background style
    screen1_style = style_part("SCREEN", "MAIN", "main", 1040, childs=[
        style_state_full("DEFAULT",
                         bg_color=[25, 25, 35, 255],
                         text_color=[220, 220, 230, 255]),
    ])

    screen1 = make_screen("Dashboard", screen1_guid, children=[
        title_label, main_slider, arc_widget, status_label,
        set_label_btn, inc_arc_btn, func_btn,
        go_settings_btn, go_data_btn,
    ])
    # Replace screen style
    screen1["properties"] = [p for p in screen1["properties"]
                             if p.get("strtype") != "SCREEN/Style_main"]
    screen1["properties"].append(screen1_style)

    # ==================== SCREEN 2: Settings ====================
    # FLEX panel with controls
    switch1 = make_switch("WifiSwitch", 0, 0)
    switch2 = make_switch("BtSwitch", 0, 0)
    check1 = make_checkbox("AutoUpdate", "Auto-update", 0, 0)
    check2 = make_checkbox("DarkMode", "Dark mode", 0, 0)
    dropdown1 = make_dropdown("LanguageDrop", ["English", "Français", "Deutsch", "日本語"], 0, 0, 130, 35)

    controls_panel = make_panel("ControlsPanel", 0, -20, 300, 180,
                                children=[switch1, switch2, check1, check2, dropdown1],
                                use_flex=True)

    # Styled panel with border and padding
    panel_style = style_part("PANEL", "MAIN", "main", 1010, childs=[
        style_state_full("DEFAULT",
                         bg_color=[35, 35, 50, 255],
                         border_color=[60, 60, 100, 255],
                         border_width=1,
                         bg_radius=12,
                         padding=[10, 10, 10, 10]),
    ])
    controls_panel["properties"] = [p for p in controls_panel["properties"]
                                    if p.get("strtype") != "PANEL/Style_main"]
    controls_panel["properties"].append(panel_style)

    settings_title = make_label("SettingsTitle", "Settings", 0, -140)

    back_btn2 = make_button("BackBtn2", 0, 130, 100, 35)
    back_btn2["properties"].append(
        event_change_screen(screen1_guid, "MOVE_RIGHT", 400, event_name="BackToDash"))
    back_lbl2 = make_label("BackLbl2", "← Back", 0, 0)
    back_btn2["children"] = [back_lbl2]

    screen2 = make_screen("Settings", screen2_guid, children=[
        settings_title, controls_panel, back_btn2,
    ])
    screen2_style = style_part("SCREEN", "MAIN", "main", 1040, childs=[
        style_state_full("DEFAULT", bg_color=[20, 25, 40, 255], text_color=[200, 200, 220, 255]),
    ])
    screen2["properties"] = [p for p in screen2["properties"]
                             if p.get("strtype") != "SCREEN/Style_main"]
    screen2["properties"].append(screen2_style)

    # ==================== SCREEN 3: Data View ====================
    bar1 = make_bar("CpuBar", -60, -60, 150, 15, value=75)
    bar2 = make_bar("MemBar", -60, -30, 150, 15, value=42)
    bar3 = make_bar("DiskBar", -60, 0, 150, 15, value=88)

    cpu_label = make_label("CpuLabel", "CPU: 75%", -160, -60)
    mem_label = make_label("MemLabel", "MEM: 42%", -160, -30)
    disk_label = make_label("DiskLabel", "DSK: 88%", -160, 0)

    data_title = make_label("DataTitle", "System Monitor", 0, -140)

    slider_vert = make_slider("TempSlider", 120, -30, 10, 120, 0, 100, 65)

    back_btn3 = make_button("BackBtn3", 0, 130, 100, 35)
    back_btn3["properties"].append(
        event_change_screen(screen1_guid, "MOVE_LEFT", 400, event_name="BackToDash2"))
    back_lbl3 = make_label("BackLbl3", "← Back", 0, 0)
    back_btn3["children"] = [back_lbl3]

    screen3 = make_screen("DataView", screen3_guid, children=[
        data_title, cpu_label, mem_label, disk_label,
        bar1, bar2, bar3, slider_vert, back_btn3,
    ])
    screen3_style = style_part("SCREEN", "MAIN", "main", 1040, childs=[
        style_state_full("DEFAULT", bg_color=[15, 20, 15, 255], text_color=[100, 255, 100, 255]),
    ])
    screen3["properties"] = [p for p in screen3["properties"]
                             if p.get("strtype") != "SCREEN/Style_main"]
    screen3["properties"].append(screen3_style)

    # ==================== Assemble Project ====================
    root_guid_val = guid()
    global NID_COUNTER

    spj = {
        "root": {
            "guid": root_guid_val,
            "children": [screen1, screen2, screen3],
            "properties": [
                {"nid": NID_COUNTER + 1, "strtype": "STARTEVENTS/Name",
                 "strval": "___initial_actions0", "InheritedType": 10}
            ],
            "saved_objtypeKey": "STARTEVENTS"
        },
        "animations": [],
        "selected_theme": "Default",
        "selected_screen": screen1_guid,
        "info": {
            "name": f"{project_name}.spj",
            "depth": 1, "width": width, "height": height,
            "rotation": 0, "offset_x": 0, "offset_y": 0,
            "shape": "RECTANGLE", "multilang": "DISABLE", "description": "",
            "board": "Custom Board", "board_version": "v1.0.0",
            "editor_version": "1.6.1", "image": "",
            "export_temp_image": False, "force_export_images": False,
            "flat_export": True, "advanced_alpha": False,
            "pointfilter": False, "theme_simplified": False,
            "theme_dark": False, "theme_color1": 5, "theme_color2": 0,
            "custom_variable_prefix": "uic",
            "separate_screen_save": False, "hierarchy_state_save": False,
            "reverse_event_order": False, "backup_cnt": 0, "autosave_cnt": 0,
            "group_color_cnt": 0, "imagebytearrayprefix": None,
            "lvgl_version": "8.3.11", "callfuncsexport": "C_FILE",
            "imageexport": "SOURCE", "lvgl_include_path": None,
            "naming": "Name", "naming_force_lowercase": False,
            "naming_add_subcomponent": False,
            "nidcnt": NID_COUNTER + 10, "BitDepth": 16, "Name": project_name
        }
    }

    sll = {
        "name": f"{project_name}.spj", "depth": 1,
        "width": width, "height": height, "rotation": 0,
        "offset_x": 0, "offset_y": 0, "shape": "RECTANGLE",
        "multilang": "DISABLE", "description": "",
        "board": "Custom Board", "board_version": "v1.0.0",
        "editor_version": "1.6.1", "image": "",
        "export_temp_image": False, "force_export_images": False,
        "flat_export": True, "advanced_alpha": False,
        "pointfilter": False, "theme_simplified": False,
        "theme_dark": False, "theme_color1": 5, "theme_color2": 0,
        "custom_variable_prefix": "uic",
        "separate_screen_save": False, "hierarchy_state_save": False,
        "reverse_event_order": False, "backup_cnt": 0, "autosave_cnt": 0,
        "group_color_cnt": 0, "imagebytearrayprefix": "",
        "lvgl_version": "8.3.11", "callfuncsexport": "C_FILE",
        "imageexport": "SOURCE", "lvgl_include_path": "",
        "naming": "Name", "naming_force_lowercase": False,
        "naming_add_subcomponent": False,
        "nidcnt": NID_COUNTER + 10
    }

    slt = {"deftheme": {"name": "Default", "properties": []},
           "themes": [], "selected_theme": "Default"}

    info = {
        "project_name": f"{project_name}.spj",
        "datetime": datetime.now().astimezone().isoformat(),
        "editor_version": "1.6.1", "project_version": 1, "user": ""
    }

    # Write
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "assets"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "components"), exist_ok=True)

    with open(os.path.join(output_dir, f"{project_name}.spj"), "w") as f:
        json.dump(spj, f, indent=2)
    with open(os.path.join(output_dir, f"{project_name}.sll"), "w") as f:
        json.dump(sll, f, indent=4)
    with open(os.path.join(output_dir, "Themes.slt"), "w") as f:
        json.dump(slt, f, indent=2)
    with open(os.path.join(output_dir, "project.info"), "w") as f:
        json.dump(info, f, indent=4)

    # Stats
    def count_widgets(obj):
        c = 1 if isinstance(obj, dict) and obj.get("saved_objtypeKey") else 0
        for child in (obj.get("children", []) if isinstance(obj, dict) else []):
            c += count_widgets(child)
        return c

    def count_events(obj):
        c = 0
        if isinstance(obj, dict):
            for p in obj.get("properties", []):
                if p.get("strtype") == "_event/EventHandler":
                    c += 1
            for child in obj.get("children", []):
                c += count_events(child)
        return c

    total_widgets = count_widgets(spj["root"])
    total_events = count_events(spj["root"])

    print(f"✅ Complex test project generated at: {output_dir}")
    print(f"   Screens: 3 (Dashboard, Settings, DataView)")
    print(f"   Widgets: {total_widgets} total")
    print(f"   Events: {total_events} (CHANGE SCREEN, CALL FUNCTION, LABEL_PROPERTY, INCREMENT ARC)")
    print(f"   Features: FLEX layout, styled buttons with PRESSED state, dark backgrounds,")
    print(f"             borders, padding, radius, cross-screen navigation, 4 action types")
    print(f"   Max nid: {NID_COUNTER}, nidcnt: {NID_COUNTER + 10}")


if __name__ == "__main__":
    main()
