#!/usr/bin/env python3
"""
Widget helper library for SquareLine Studio project generation.

Provides a WidgetBuilder class that simplifies widget construction by handling:
- GUID generation with uniqueness tracking
- nidcnt auto-increment for dynamic properties
- All 16 mandatory OBJECT/* base properties
- Widget-type-specific properties and style parts
- Style state construction with correct key names (including SLS quirks)
- Event action construction with correct Call/CallC templates
- Color array length validation (4 for RGBA, 3 for gradient)
- Font validation against built-in Montserrat sizes

Usage:
    from widget_helpers import WidgetBuilder

    wb = WidgetBuilder()
    label = wb.label("title", text="Hello", font="montserrat_24",
                     align="CENTER", y_offset=-60,
                     color=[255, 255, 255, 255])
    button = wb.button("save_btn", text="Save", size=(120, 48),
                       on_click=wb.change_screen(target_guid))
    wb.add_children(screen_node, [label, button])
"""
import random
import warnings


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BUILTIN_MONTSERRAT_SIZES = frozenset(range(8, 50, 2))  # 8,10,...,48

# Standard alignment values accepted by SLS
ALIGNMENTS = {
    "CENTER", "TOP_LEFT", "TOP_MID", "TOP_RIGHT",
    "BOTTOM_LEFT", "BOTTOM_MID", "BOTTOM_RIGHT",
    "LEFT_MID", "RIGHT_MID",
}

# Style property key names with their exact SLS formatting (including quirks)
# Maps from a normalised name to the real SLS key
_STYLE_KEY_MAP = {
    "bg_color": "_style/Bg_Color",
    "bg_radius": "_style/Bg_Radius",
    "bg_gradient_color": "_style/Bg_gradiens_Color",  # SLS typo is real
    "bg_gradient_params": "_style/Bg_gradient_params",
    "gradient_direction": "_style/Gradient direction",  # space is real
    "clip_corner": "_style/Clip_corner",
    "bg_image": "_style/Bg_Image",
    "bg_image_opa": "_style/Bg_Image_opa",
    "bg_image_recolor": "_style/Bg_Image_Recolor",
    "bg_image_tiled": "_style/Bg_Image_Tiled",
    "border_color": "_style/Border_Color",
    "border_width": "_style/Border width",  # space is real
    "border_side": "_style/Border side",  # space is real
    "outline_color": "_style/Outline_Color",
    "outline_params": "_style/Outline_params",
    "shadow_color": "_style/Shadow_Color",
    "shadow_params": "_style/Shadow_params",
    "shadow_offset": "_style/Shadow_offset",
    "blend_mode": "_style/Blend mode",  # space is real
    "blend_opacity": "_style/Blend_opacity",
    "padding": "_style/Padding",
    "padding_rowcol": "_style/Padding_RowCol",
    "text_color": "_style/Text_Color",
    "text_font": "_style/Text_Font",
    "text_align": "_style/Text_Align",
    "text_spacing": "_style/Text_Spacing",
    "text_decor": "_style/Text_Decor",
    "transform_width": "_style/Transform_width",
    "transform_height": "_style/Transform_height",
    "transform_rotation": "_style/Transform_rotation",
    "transform_scale": "_style/Transform_scale",
    "transform_pivot": "_style/Transform_pivot",
    "arc_image": "_style/Arc_Image",
    "arc_rounded": "_style/Arc_Rounded",
    "arc_width": "_style/Arc_Width",
}

# Which style properties use intarray (IT=7) and what flags value
_STYLE_INTARRAY_PROPS = {
    "bg_color": (4096, 4),        # [R, G, B, A]
    "bg_gradient_color": (256, 3),  # [R, G, B] — no alpha!
    "bg_gradient_params": (16, 2),  # [start_opa, end_opa]
    "border_color": (4096, 4),
    "outline_color": (4096, 4),
    "outline_params": (16, 2),
    "shadow_color": (4096, 4),
    "shadow_params": (16, 2),
    "shadow_offset": (16, 2),
    "text_color": (4096, 4),
    "text_spacing": (16, 2),
    "padding": (4096, 4),         # [top, bottom, left, right]
    "padding_rowcol": (16, 2),
    "transform_width": (16, 2),
    "transform_height": (16, 2),
    "transform_pivot": (16, 2),
    "bg_image_recolor": (4096, 4),
}

# Style properties that use integer (IT=6)
_STYLE_INT_PROPS = {
    "bg_radius", "border_width", "blend_opacity", "bg_image_opa",
    "transform_rotation", "transform_scale", "arc_width",
}

# Style properties that use strval (IT=3)
_STYLE_STR_PROPS = {
    "gradient_direction", "clip_corner", "bg_image_tiled",
    "border_side", "blend_mode", "text_font", "text_align",
    "text_decor", "arc_rounded",
}

# Style properties that use asset path (IT=5)
_STYLE_ASSET_PROPS = {"bg_image", "arc_image"}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _validate_font(font_name):
    """Warn if a font name doesn't match a known built-in Montserrat size."""
    if font_name.startswith("ui_font_"):
        return  # Custom font, always valid
    if font_name.startswith("montserrat_"):
        try:
            size = int(font_name.split("_", 1)[1])
        except (ValueError, IndexError):
            warnings.warn(
                f"Font '{font_name}': cannot parse size from name. "
                f"Built-in Montserrat sizes are even numbers 8-48.",
                stacklevel=3,
            )
            return
        if size not in BUILTIN_MONTSERRAT_SIZES:
            warnings.warn(
                f"Font '{font_name}': size {size} is not a built-in Montserrat size. "
                f"Built-in sizes are even numbers 8-48. "
                f"Use SLS Font Manager to generate custom sizes.",
                stacklevel=3,
            )


def _validate_color(name, arr, expected_len):
    """Validate a color array has the expected length."""
    if len(arr) != expected_len:
        raise ValueError(
            f"Color array for '{name}' must have {expected_len} elements "
            f"(got {len(arr)}). "
            f"{'[R, G, B, A] (0-255)' if expected_len == 4 else '[R, G, B] (0-255, no alpha)'}"
        )


# ---------------------------------------------------------------------------
# WidgetBuilder
# ---------------------------------------------------------------------------

class WidgetBuilder:
    """
    Stateful builder for SquareLine Studio widget JSON structures.

    Tracks GUID uniqueness and nidcnt to prevent collisions across
    all widgets built by the same builder instance.
    """

    def __init__(self, starting_nidcnt=1000400, lvgl_version="9.2.2"):
        """
        Args:
            starting_nidcnt: Starting value for dynamic nid allocation.
                Must be higher than any fixed widget property nids (typically < 2000).
                Default 1000400 matches the pattern used in SLS projects.
            lvgl_version: Target LVGL version string (e.g., "8.3.11", "9.2.2").
                Used to validate widget compatibility. Default "9.2.2" matches
                current SLS bundled examples.
        """
        self._nidcnt = starting_nidcnt
        self._guids = set()
        self._lvgl_major = int(lvgl_version.split(".")[0]) if lvgl_version else 9

    @property
    def nidcnt(self):
        """Current nidcnt value. Use this for the .sll / .spj info block."""
        return self._nidcnt

    def _next_nid(self):
        """Allocate the next dynamic nid."""
        self._nidcnt += 1
        return self._nidcnt

    def _guid(self):
        """Generate a unique GUID in SLS format."""
        for _ in range(1000):
            a = random.randint(10000000, 99999999)
            b = random.randint(100000, 999999)
            c = random.randint(1000000, 9999999)
            g = f"GUID{a}-{b}S{c}"
            if g not in self._guids:
                self._guids.add(g)
                return g
        raise RuntimeError("Failed to generate unique GUID after 1000 attempts")

    # ------------------------------------------------------------------
    # Base property boilerplate
    # ------------------------------------------------------------------

    def _base_props(self, name, x=0, y=0, w=100, h=50, align="CENTER",
                    content_fit=False):
        """
        Generate the 16 mandatory OBJECT/* properties every widget needs.

        Args:
            name: Widget name (must be unique within the project)
            x, y: Position offset from alignment point
            w, h: Width and height in pixels
            align: Alignment within parent (CENTER, TOP_LEFT, etc.)
            content_fit: If True, use content-fit sizing (flags=51)
        """
        size_flags = 51 if content_fit else 17
        return [
            {"nid": 10, "strtype": "OBJECT/Name", "strval": name,
             "InheritedType": 10},
            {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0, "nid": 30, "strtype": "OBJECT/Layout_type",
                "strval": "No_layout", "InheritedType": 13
            },
            {"nid": 40, "strtype": "OBJECT/Transform", "InheritedType": 1},
            {"nid": 50, "flags": 17, "strtype": "OBJECT/Position",
             "intarray": [x, y], "InheritedType": 7},
            {"nid": 60, "flags": size_flags, "strtype": "OBJECT/Size",
             "intarray": [w, h], "InheritedType": 7},
            {"nid": 70, "strtype": "OBJECT/Align", "strval": align,
             "InheritedType": 3},
            {"nid": 75, "strtype": "OBJECT/Extend_click_area",
             "InheritedType": 6},
            {"nid": 90, "flags": 1048576, "strtype": "OBJECT/Flags",
             "InheritedType": 1},
            {"nid": 225, "flags": 1048576, "strtype": "OBJECT/Scrolling",
             "InheritedType": 1},
            {"nid": 230, "strtype": "OBJECT/Scrollable", "strval": "False",
             "InheritedType": 2},
            {"nid": 300, "strtype": "OBJECT/Scrollbar_mode", "strval": "AUTO",
             "InheritedType": 3},
            {"nid": 310, "strtype": "OBJECT/Scroll_direction", "strval": "ALL",
             "InheritedType": 3},
            {"nid": 314, "strtype": "OBJECT/Scroll_snap_x", "strval": "NONE",
             "InheritedType": 3},
            {"nid": 315, "strtype": "OBJECT/Scroll_snap_y", "strval": "NONE",
             "InheritedType": 3},
            {"nid": 320, "flags": 1048576, "strtype": "OBJECT/States",
             "InheritedType": 1},
        ]

    def _style_part(self, prefix, part_name, part_label, nid, childs=None):
        """Create a style part property."""
        return {
            "part": f"lv.PART.{part_name}",
            "childs": childs or [],
            "nid": nid,
            "strtype": f"{prefix}/Style_{part_label}",
            "strval": f"lv.PART.{part_name}, Rectangle, Pad, Text",
            "InheritedType": 11,
        }

    def _checkbox_bullet_part(self, nid, childs=None):
        """Create the CHECKBOX bullet (indicator) style part."""
        return {
            "part": "lv.PART.INDICATOR",
            "childs": childs or [],
            "nid": nid,
            "strtype": "CHECKBOX/Style_bullet",
            "strval": "lv.PART.INDICATOR, Rectangle",
            "InheritedType": 11,
        }

    def _flex_layout_type(self, flow=0, wrap=False, main_align=0,
                          cross_align=1, track_align=0):
        """Return a Layout_type property configured for FLEX layout."""
        return {
            "Flow": flow, "Wrap": wrap, "Reversed": False,
            "MainAlignment": main_align, "CrossAlignment": cross_align,
            "TrackAlignment": track_align,
            "LayoutType": 1, "nid": 30, "strtype": "OBJECT/Layout_type",
            "strval": "No_layout", "InheritedType": 13,
        }

    # ------------------------------------------------------------------
    # Style builder
    # ------------------------------------------------------------------

    def style(self, **kwargs):
        """
        Build a style state properties list from keyword arguments.

        Uses normalised names that map to SLS's exact (sometimes quirky) keys.
        Validates color array lengths and font names.

        Args:
            bg_color: [R, G, B, A] background color
            bg_radius: int corner radius
            bg_gradient_color: [R, G, B] gradient end color (no alpha!)
            bg_gradient_params: [start_opa, end_opa]
            gradient_direction: "HOR" or "VER"
            border_color: [R, G, B, A]
            border_width: int px
            border_side: "FULL", "BOTTOM", "TOP", etc.
            outline_color: [R, G, B, A]
            outline_params: [width, offset]
            shadow_color: [R, G, B, A]
            shadow_params: [width, spread]
            shadow_offset: [x, y]
            blend_mode: "NORMAL", "ADDITIVE", "SUBTRACTIVE"
            blend_opacity: 0-255
            padding: [top, bottom, left, right]
            padding_rowcol: [row, column]
            text_color: [R, G, B, A]
            text_font: font name (e.g. "montserrat_14")
            text_align: "AUTO", "CENTER", "LEFT", "RIGHT"
            text_spacing: [letter, line]
            text_decor: "NONE", "UNDERLINE", "STRIKETHROUGH"
            pad_all: int — shorthand sets all 4 padding values

        Returns:
            List of style property dicts ready for use in a style state.
        """
        props = []

        # Handle pad_all shorthand
        if "pad_all" in kwargs and "padding" not in kwargs:
            v = kwargs.pop("pad_all")
            kwargs["padding"] = [v, v, v, v]
        elif "pad_all" in kwargs:
            kwargs.pop("pad_all")

        for key, value in kwargs.items():
            if key == "pad_all":
                continue  # Already handled

            if key not in _STYLE_KEY_MAP:
                raise ValueError(
                    f"Unknown style property '{key}'. "
                    f"Valid properties: {sorted(_STYLE_KEY_MAP.keys())}"
                )

            strtype = _STYLE_KEY_MAP[key]

            if key in _STYLE_INTARRAY_PROPS:
                flags, expected_len = _STYLE_INTARRAY_PROPS[key]
                if not isinstance(value, (list, tuple)):
                    raise TypeError(
                        f"Style property '{key}' requires a list/tuple, got {type(value).__name__}"
                    )
                _validate_color(key, value, expected_len)
                props.append({
                    "nid": self._next_nid(),
                    "strtype": strtype,
                    "flags": flags,
                    "intarray": list(value),
                    "InheritedType": 7,
                })
            elif key in _STYLE_INT_PROPS:
                props.append({
                    "nid": self._next_nid(),
                    "strtype": strtype,
                    "integer": int(value),
                    "InheritedType": 6,
                })
            elif key in _STYLE_STR_PROPS:
                if key == "text_font":
                    _validate_font(str(value))
                props.append({
                    "nid": self._next_nid(),
                    "strtype": strtype,
                    "strval": str(value),
                    "InheritedType": 3,
                })
            elif key in _STYLE_ASSET_PROPS:
                props.append({
                    "nid": self._next_nid(),
                    "strtype": strtype,
                    "strval": str(value),
                    "InheritedType": 5,
                })
            else:
                raise ValueError(f"Unhandled style property type for '{key}'")

        return props

    def style_state(self, state="DEFAULT", **kwargs):
        """
        Build a complete style state dict.

        Args:
            state: Style state name ("DEFAULT", "PRESSED", "CHECKED",
                   "FOCUSED", "DISABLED", etc.)
            **kwargs: Style properties (same as style() method)

        Returns:
            A style state dict ready for insertion into a style part's childs.
        """
        return {
            "strtype": "_stylestate/state",
            "strval": state,
            "childs": self.style(**kwargs),
        }

    # ------------------------------------------------------------------
    # Event builders
    # ------------------------------------------------------------------

    def change_screen(self, target_guid, fade="FADE_ON", speed=500, delay=0):
        """
        Build a CHANGE SCREEN action dict.

        Args:
            target_guid: GUID of the target screen
            fade: Transition animation ("FADE_ON", "MOVE_LEFT", "MOVE_RIGHT", etc.)
            speed: Transition speed in ms
            delay: Delay before transition in ms

        Returns:
            Action dict for use in event_handler's action slot.
        """
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "CHANGE SCREEN",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "CHANGE SCREEN/Name",
                 "strval": "CHANGE SCREEN", "InheritedType": 10},
                {"nid": n(), "strtype": "CHANGE SCREEN/Call",
                 "strval": "ChangeScreen( <{Screen_to}>, lv.SCR_LOAD_ANIM.<{Fade_mode}>, <{Speed}>, <{Delay}>)",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "CHANGE SCREEN/CallC",
                 "strval": "_ui_screen_change( &<{Screen_to}>, LV_SCR_LOAD_ANIM_<{Fade_mode}>, <{Speed}>, <{Delay}>, &<{Screen_to}>_screen_init);",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "CHANGE SCREEN/Screen_to",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "CHANGE SCREEN/Fade_mode",
                 "strval": fade, "InheritedType": 3},
                {"nid": n(), "strtype": "CHANGE SCREEN/Speed",
                 "integer": speed, "InheritedType": 6},
                {"nid": n(), "strtype": "CHANGE SCREEN/Delay",
                 "integer": delay, "InheritedType": 6},
            ],
        }

    def call_function(self, func_name):
        """
        Build a CALL FUNCTION action dict.

        Args:
            func_name: Name of the C/Python function to call

        Returns:
            Action dict for use in event_handler's action slot.
        """
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "CALL FUNCTION",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "CALL FUNCTION/Name",
                 "strval": "CALL FUNCTION", "InheritedType": 10},
                {"nid": n(), "strtype": "CALL FUNCTION/Call",
                 "strval": "<{Function_name}>( )", "InheritedType": 10},
                {"nid": n(), "strtype": "CALL FUNCTION/CallC",
                 "strval": "<{Function_name}>(e);", "InheritedType": 10},
                {"nid": n(), "strtype": "CALL FUNCTION/Function_name",
                 "strval": func_name, "InheritedType": 10},
                {"nid": n(), "strtype": "CALL FUNCTION/Dont_export_function",
                 "strval": "False", "InheritedType": 2},
            ],
        }

    def set_label_property(self, target_guid, value, prop="Text"):
        """
        Build a LABEL_PROPERTY action dict.

        Args:
            target_guid: GUID of the target label widget
            value: Value to set (text content)
            prop: Property to set ("Text" by default)

        Returns:
            Action dict for use in event_handler's action slot.
        """
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "LABEL_PROPERTY",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "LABEL_PROPERTY/Name",
                 "strval": "LABEL_PROPERTY", "InheritedType": 10},
                {"nid": n(), "strtype": "LABEL_PROPERTY/Call",
                 "strval": "SetLabelProperty(<{Target}>, '<{Property}>', '<{Value}>')",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "LABEL_PROPERTY/CallC",
                 "strval": '_ui_label_set_property(<{Target}>, _UI_LABEL_PROPERTY_<{Property}>, "<{Value}>");',
                 "InheritedType": 10},
                {"nid": n(), "strtype": "LABEL_PROPERTY/Target",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "LABEL_PROPERTY/Property",
                 "strval": prop, "InheritedType": 3},
                {"nid": n(), "strtype": "LABEL_PROPERTY/Value",
                 "strval": value, "InheritedType": 10},
            ],
        }

    def increment_arc(self, target_guid, value=10):
        """
        Build an INCREMENT ARC action dict.

        Args:
            target_guid: GUID of the target arc widget
            value: Increment amount

        Returns:
            Action dict for use in event_handler's action slot.
        """
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "INCREMENT ARC",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "INCREMENT ARC/Name",
                 "strval": "INCREMENT ARC", "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT ARC/Call",
                 "strval": "IncrementArc( <{Target}>, <{Value}> )",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT ARC/CallC",
                 "strval": "_ui_arc_increment( <{Target}>, <{Value}>);",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT ARC/Target",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "INCREMENT ARC/Value",
                 "integer": value, "InheritedType": 6},
            ],
        }

    def increment_slider(self, target_guid, value=10):
        """Build an INCREMENT SLIDER action dict."""
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "INCREMENT SLIDER",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "INCREMENT SLIDER/Name",
                 "strval": "INCREMENT SLIDER", "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT SLIDER/Call",
                 "strval": "IncrementSlider( <{Target}>, <{Value}> )",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT SLIDER/CallC",
                 "strval": "_ui_slider_increment( <{Target}>, <{Value}>);",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT SLIDER/Target",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "INCREMENT SLIDER/Value",
                 "integer": value, "InheritedType": 6},
            ],
        }

    def increment_bar(self, target_guid, value=10):
        """Build an INCREMENT BAR action dict."""
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "INCREMENT BAR",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "INCREMENT BAR/Name",
                 "strval": "INCREMENT BAR", "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT BAR/Call",
                 "strval": "IncrementBar( <{Target}>, <{Value}> )",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT BAR/CallC",
                 "strval": "_ui_bar_increment( <{Target}>, <{Value}>);",
                 "InheritedType": 10},
                {"nid": n(), "strtype": "INCREMENT BAR/Target",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "INCREMENT BAR/Value",
                 "integer": value, "InheritedType": 6},
            ],
        }

    def modify_flag(self, target_guid, flag, action="ADD"):
        """
        Build a MODIFY FLAG action dict.

        Args:
            target_guid: GUID of the target widget
            flag: Flag name (e.g. "Hidden", "Clickable", "Disabled")
            action: "ADD" to set, "REMOVE" to clear

        Returns:
            Action dict for use in event_handler's action slot.
        """
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "MODIFY FLAG",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "MODIFY FLAG/Name",
                 "strval": "MODIFY FLAG", "InheritedType": 10},
                {"nid": n(), "strtype": "MODIFY FLAG/Target",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "MODIFY FLAG/Flag",
                 "strval": flag, "InheritedType": 3},
                {"nid": n(), "strtype": "MODIFY FLAG/Action",
                 "strval": action, "InheritedType": 3},
            ],
        }

    def modify_state(self, target_guid, state, action="ADD"):
        """
        Build a MODIFY STATE action dict.

        Args:
            target_guid: GUID of the target widget
            state: State name (e.g. "Checked", "Disabled", "Focused")
            action: "ADD" to set, "REMOVE" to clear

        Returns:
            Action dict for use in event_handler's action slot.
        """
        n = self._next_nid
        return {
            "strtype": "_event/action", "strval": "MODIFY STATE",
            "InheritedType": 10,
            "childs": [
                {"nid": n(), "strtype": "MODIFY STATE/Name",
                 "strval": "MODIFY STATE", "InheritedType": 10},
                {"nid": n(), "strtype": "MODIFY STATE/Target",
                 "strval": target_guid, "InheritedType": 9},
                {"nid": n(), "strtype": "MODIFY STATE/State",
                 "strval": state, "InheritedType": 3},
                {"nid": n(), "strtype": "MODIFY STATE/Action",
                 "strval": action, "InheritedType": 3},
            ],
        }

    def event_handler(self, trigger="CLICKED", action=None, event_name=None):
        """
        Wrap an action in a full EventHandler property.

        Args:
            trigger: Event trigger type ("CLICKED", "VALUE_CHANGED",
                    "SCREEN_LOADED", etc.)
            action: Action dict from change_screen(), call_function(), etc.
            event_name: Display name for the event (auto-generated if None)

        Returns:
            A complete EventHandler property dict to append to widget properties.
        """
        if action is None:
            raise ValueError("event_handler requires an action")
        if event_name is None:
            event_name = trigger.replace("(", "_").replace(")", "")
        n = self._next_nid
        return {
            "disabled": False,
            "nid": n(),
            "strtype": "_event/EventHandler",
            "strval": trigger,
            "InheritedType": 4,
            "childs": [
                {"nid": n(), "strtype": "_event/name",
                 "strval": event_name, "InheritedType": 10},
                {"nid": n(), "strtype": "_event/condition_C",
                 "strval": "", "InheritedType": 10},
                {"nid": n(), "strtype": "_event/condition_P",
                 "strval": "", "InheritedType": 10},
                action,
            ],
        }

    # ------------------------------------------------------------------
    # Widget builders
    # ------------------------------------------------------------------

    def screen(self, name, bg_color=None, editor_posx=600, editor_posy=-600):
        """
        Create a SCREEN widget.

        Args:
            name: Screen name
            bg_color: Optional [R, G, B, A] background colour
            editor_posx: Editor canvas X position
            editor_posy: Editor canvas Y position

        Returns:
            Screen widget dict with guid accessible via result["guid"].
        """
        g = self._guid()
        style_childs = []
        if bg_color is not None:
            _validate_color("bg_color", bg_color, 4)
            style_childs = [
                self.style_state("DEFAULT", bg_color=bg_color)
            ]

        props = [
            {"nid": 10, "strtype": "OBJECT/Name", "strval": name,
             "InheritedType": 10},
            {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0, "nid": 30, "strtype": "OBJECT/Layout_type",
                "strval": "No_layout", "InheritedType": 13,
            },
            {"nid": 40, "strtype": "OBJECT/Transform", "InheritedType": 1},
            {"nid": 90, "flags": 1048576, "strtype": "OBJECT/Flags",
             "InheritedType": 1},
            {"nid": 225, "flags": 1048576, "strtype": "OBJECT/Scrolling",
             "InheritedType": 1},
            {"nid": 230, "strtype": "OBJECT/Scrollable", "strval": "False",
             "InheritedType": 2},
            {"nid": 300, "strtype": "OBJECT/Scrollbar_mode", "strval": "AUTO",
             "InheritedType": 3},
            {"nid": 310, "strtype": "OBJECT/Scroll_direction",
             "strval": "ALL", "InheritedType": 3},
            {"nid": 314, "strtype": "OBJECT/Scroll_snap_x", "strval": "NONE",
             "InheritedType": 3},
            {"nid": 315, "strtype": "OBJECT/Scroll_snap_y", "strval": "NONE",
             "InheritedType": 3},
            {"nid": 320, "flags": 1048576, "strtype": "OBJECT/States",
             "InheritedType": 1},
            {"nid": 1010, "strtype": "SCREEN/Screen", "InheritedType": 1},
            {"nid": 1020, "strtype": "SCREEN/Temporary", "strval": "False",
             "InheritedType": 2},
            self._style_part("SCREEN", "MAIN", "main", 1040,
                             childs=style_childs),
            self._style_part("SCREEN", "SCROLLBAR", "scrollbar", 1050),
        ]

        return {
            "guid": g,
            "children": [],
            "isPage": True,
            "editor_posx": editor_posx,
            "editor_posy": editor_posy,
            "properties": props,
            "saved_objtypeKey": "SCREEN",
        }

    def label(self, name, text="Label", font=None, color=None,
              long_mode="WRAP", size=None, align="CENTER",
              x_offset=0, y_offset=0, style=None, on_click=None):
        """
        Create a LABEL widget.

        Args:
            name: Widget name
            text: Label text content
            font: Font name (e.g. "montserrat_14"). Validated against built-ins.
            color: Optional [R, G, B, A] text colour
            long_mode: "WRAP", "SCROLL", "DOT", or "CLIP"
            size: Optional (w, h) tuple. Defaults to content-fit.
            align: Alignment within parent
            x_offset, y_offset: Position offset
            style: Optional list of style properties from self.style()
            on_click: Optional action from change_screen(), call_function(), etc.

        Returns:
            Label widget dict.
        """
        w, h = size if size else (100, 20)
        content_fit = size is None

        props = self._base_props(name, x_offset, y_offset, w, h, align,
                                 content_fit=content_fit)
        props.extend([
            {"nid": 1010, "strtype": "LABEL/Label", "InheritedType": 1},
            {"nid": 1020, "strtype": "LABEL/Text", "strval": text,
             "InheritedType": 10},
            {"nid": 1030, "strtype": "LABEL/Long_mode", "strval": long_mode,
             "InheritedType": 3},
            {"nid": 1040, "strtype": "LABEL/Recolor", "strval": "False",
             "InheritedType": 2},
        ])

        # Build style childs from font, color, and explicit style
        style_childs = []
        default_style_props = []
        if font:
            _validate_font(font)
            default_style_props.append({
                "nid": self._next_nid(), "strtype": "_style/Text_Font",
                "strval": font, "InheritedType": 3,
            })
        if color:
            _validate_color("text_color", color, 4)
            default_style_props.append({
                "nid": self._next_nid(), "strtype": "_style/Text_Color",
                "flags": 4096, "intarray": list(color), "InheritedType": 7,
            })
        if style:
            default_style_props.extend(style)
        if default_style_props:
            style_childs.append({
                "strtype": "_stylestate/state",
                "strval": "DEFAULT",
                "childs": default_style_props,
            })

        props.append(self._style_part("LABEL", "MAIN", "main", 1050,
                                       childs=style_childs))

        widget = {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "LABEL",
        }

        if on_click:
            widget["properties"].append(
                self.event_handler("CLICKED", on_click))

        return widget

    def button(self, name, text=None, size=(100, 40), align="CENTER",
               x_offset=0, y_offset=0, style=None, pressed_style=None,
               on_click=None, font=None):
        """
        Create a BUTTON widget, optionally with a child LABEL.

        Args:
            name: Widget name
            text: Optional button text (creates a child label)
            size: (width, height) tuple
            align: Alignment within parent
            x_offset, y_offset: Position offset
            style: Optional DEFAULT state style props from self.style()
            pressed_style: Optional PRESSED state style props from self.style()
            on_click: Optional action from change_screen(), call_function(), etc.
            font: Font for the button label text

        Returns:
            Button widget dict. Access child label via result["children"][0].
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)

        # Build style
        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state",
                "strval": "DEFAULT",
                "childs": style,
            })
        if pressed_style:
            style_childs.append({
                "strtype": "_stylestate/state",
                "strval": "PRESSED",
                "childs": pressed_style,
            })

        props.append(self._style_part("BUTTON", "MAIN", "main", 1010,
                                       childs=style_childs))

        children = []
        if text:
            children.append(
                self.label(f"{name}_Label", text=text, font=font))

        widget = {
            "guid": self._guid(), "children": children, "properties": props,
            "saved_objtypeKey": "BUTTON",
        }

        if on_click:
            widget["properties"].append(
                self.event_handler("CLICKED", on_click))

        return widget

    def image(self, name, src="", size=(100, 100), align="CENTER",
              x_offset=0, y_offset=0, zoom=256, angle=0, pivot=None,
              style=None):
        """
        Create an IMAGE widget.

        Args:
            name: Widget name
            src: Asset path (e.g. "assets/icon.png")
            size: (width, height) tuple
            align: Alignment
            x_offset, y_offset: Position offset
            zoom: Scale factor (256 = 100%)
            angle: Rotation in 0.1° units
            pivot: Optional [x, y] rotation pivot point
            style: Optional style properties

        Returns:
            Image widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "IMAGE/Image", "InheritedType": 1},
            {"nid": 1020, "strtype": "IMAGE/Asset", "strval": src,
             "InheritedType": 5},
        ])
        if pivot is not None:
            props.append({"nid": 1030, "flags": 16,
                          "strtype": "IMAGE/Pivot", "intarray": list(pivot),
                          "InheritedType": 7})
        if angle != 0:
            props.append({"nid": 1040, "strtype": "IMAGE/Rotation",
                          "integer": angle, "InheritedType": 6})
        if zoom != 256:
            props.append({"nid": 1050, "strtype": "IMAGE/Scale",
                          "integer": zoom, "InheritedType": 6})

        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state", "strval": "DEFAULT",
                "childs": style,
            })
        props.append(self._style_part("IMAGE", "MAIN", "main", 1060,
                                       childs=style_childs))

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "IMAGE",
        }

    def arc(self, name, value=50, range=(0, 100), bg_angles=(135, 45),
            size=(150, 150), align="CENTER", x_offset=0, y_offset=0,
            mode="NORMAL", style=None, indicator_style=None,
            knob_style=None):
        """
        Create an ARC widget.

        Args:
            name: Widget name
            value: Current arc value
            range: (min, max) value range
            bg_angles: (start_angle, end_angle) for background arc
            size: (width, height) — arcs are typically square
            align: Alignment
            x_offset, y_offset: Position offset
            mode: "NORMAL", "REVERSE", or "SYMMETRICAL"
            style: Optional main style properties
            indicator_style: Optional indicator style properties
            knob_style: Optional knob style properties

        Returns:
            Arc widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "ARC/Arc", "InheritedType": 1},
            {"nid": 1020, "strtype": "ARC/Value", "integer": value,
             "InheritedType": 6},
            {"nid": 1030, "flags": 16, "strtype": "ARC/Range",
             "intarray": list(range), "InheritedType": 7},
            {"nid": 1040, "flags": 16, "strtype": "ARC/Bg_angles",
             "intarray": list(bg_angles), "InheritedType": 7},
            {"nid": 1050, "strtype": "ARC/Rotation", "InheritedType": 6},
            {"nid": 1060, "strtype": "ARC/Mode", "strval": mode,
             "InheritedType": 3},
        ])

        for part_args in [
            ("ARC", "MAIN", "main", 1070, style),
            ("ARC", "INDICATOR", "indicator", 1080, indicator_style),
            ("ARC", "KNOB", "knob", 1090, knob_style),
        ]:
            prefix, part_name, part_label, nid, part_style = part_args
            childs = []
            if part_style:
                childs.append({
                    "strtype": "_stylestate/state", "strval": "DEFAULT",
                    "childs": part_style,
                })
            props.append(self._style_part(prefix, part_name, part_label, nid,
                                           childs=childs))

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "ARC",
        }

    def slider(self, name, value=50, range=(0, 100), size=(200, 10),
               align="CENTER", x_offset=0, y_offset=0, mode="NORMAL",
               style=None, indicator_style=None, knob_style=None,
               on_value_changed=None):
        """
        Create a SLIDER widget.

        Args:
            name: Widget name
            value: Current slider value
            range: (min, max) value range
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            mode: "NORMAL", "SYMMETRICAL", or "RANGE"
            style: Optional main style properties
            indicator_style: Optional indicator style properties
            knob_style: Optional knob style properties
            on_value_changed: Optional action for VALUE_CHANGED event

        Returns:
            Slider widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "SLIDER/Slider", "InheritedType": 1},
            {"nid": 1020, "flags": 16, "strtype": "SLIDER/Range",
             "intarray": list(range), "InheritedType": 7},
            {"nid": 1030, "strtype": "SLIDER/Mode", "strval": mode,
             "InheritedType": 3},
            {"nid": 1040, "strtype": "SLIDER/Value", "integer": value,
             "InheritedType": 6},
            {"nid": 1050, "strtype": "SLIDER/Value_left",
             "InheritedType": 6},
        ])

        for part_args in [
            ("SLIDER", "MAIN", "main", 1060, style),
            ("SLIDER", "INDICATOR", "indicator", 1070, indicator_style),
            ("SLIDER", "KNOB", "knob", 1080, knob_style),
        ]:
            prefix, part_name, part_label, nid, part_style = part_args
            childs = []
            if part_style:
                childs.append({
                    "strtype": "_stylestate/state", "strval": "DEFAULT",
                    "childs": part_style,
                })
            props.append(self._style_part(prefix, part_name, part_label, nid,
                                           childs=childs))

        widget = {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "SLIDER",
        }

        if on_value_changed:
            widget["properties"].append(
                self.event_handler("VALUE_CHANGED", on_value_changed))

        return widget

    def switch(self, name, align="CENTER", x_offset=0, y_offset=0,
               size=(50, 25), style=None, indicator_style=None,
               knob_style=None, on_value_changed=None):
        """
        Create a SWITCH widget.

        Args:
            name: Widget name
            align: Alignment
            x_offset, y_offset: Position offset
            size: (width, height)
            style: Optional main style
            indicator_style: Optional indicator style
            knob_style: Optional knob style
            on_value_changed: Optional action for VALUE_CHANGED

        Returns:
            Switch widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)

        for part_args in [
            ("SWITCH", "MAIN", "main", 1010, style),
            ("SWITCH", "INDICATOR", "indicator", 1020, indicator_style),
            ("SWITCH", "KNOB", "knob", 1030, knob_style),
        ]:
            prefix, part_name, part_label, nid, part_style = part_args
            childs = []
            if part_style:
                childs.append({
                    "strtype": "_stylestate/state", "strval": "DEFAULT",
                    "childs": part_style,
                })
            props.append(self._style_part(prefix, part_name, part_label, nid,
                                           childs=childs))

        widget = {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "SWITCH",
        }

        if on_value_changed:
            widget["properties"].append(
                self.event_handler("VALUE_CHANGED", on_value_changed))

        return widget

    def bar(self, name, value=50, range=(0, 100), size=(200, 20),
            align="CENTER", x_offset=0, y_offset=0, mode="NORMAL",
            style=None, indicator_style=None):
        """
        Create a BAR widget.

        Args:
            name: Widget name
            value: Current bar value
            range: (min, max) value range
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            mode: "NORMAL", "SYMMETRICAL", or "RANGE"
            style: Optional main style
            indicator_style: Optional indicator style

        Returns:
            Bar widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "BAR/Bar", "InheritedType": 1},
            {"nid": 1020, "strtype": "BAR/Value", "integer": value,
             "InheritedType": 6},
            {"nid": 1030, "strtype": "BAR/Value_start",
             "InheritedType": 6},
            {"nid": 1040, "flags": 16, "strtype": "BAR/Range",
             "intarray": list(range), "InheritedType": 7},
            {"nid": 1050, "strtype": "BAR/Mode", "strval": mode,
             "InheritedType": 3},
        ])

        for part_args in [
            ("BAR", "MAIN", "main", 1060, style),
            ("BAR", "INDICATOR", "indicator", 1070, indicator_style),
        ]:
            prefix, part_name, part_label, nid, part_style = part_args
            childs = []
            if part_style:
                childs.append({
                    "strtype": "_stylestate/state", "strval": "DEFAULT",
                    "childs": part_style,
                })
            props.append(self._style_part(prefix, part_name, part_label, nid,
                                           childs=childs))

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "BAR",
        }

    def panel(self, name, size=(200, 200), align="CENTER",
              x_offset=0, y_offset=0, flex=False, flex_flow=0,
              flex_wrap=False, style=None):
        """
        Create a PANEL widget.

        Args:
            name: Widget name
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            flex: Enable FLEX layout
            flex_flow: FLEX flow direction (0=ROW, 1=COLUMN, etc.)
            flex_wrap: Enable FLEX wrapping
            style: Optional main style

        Returns:
            Panel widget dict. Add children via add_children().
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)

        if flex:
            # Replace the layout_type with FLEX
            for i, p in enumerate(props):
                if p.get("strtype") == "OBJECT/Layout_type":
                    props[i] = self._flex_layout_type(
                        flow=flex_flow, wrap=flex_wrap)
                    break

        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state", "strval": "DEFAULT",
                "childs": style,
            })

        props.extend([
            self._style_part("PANEL", "MAIN", "main", 1010,
                              childs=style_childs),
            self._style_part("PANEL", "SCROLLBAR", "scrollbar", 1020),
        ])

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "PANEL",
        }

    def checkbox(self, name, title="Checkbox", align="CENTER",
                 x_offset=0, y_offset=0, style=None, bullet_style=None):
        """
        Create a CHECKBOX widget.

        Args:
            name: Widget name
            title: Checkbox text label
            align: Alignment
            x_offset, y_offset: Position offset
            style: Optional main style
            bullet_style: Optional bullet (indicator) style — list of
                          style state dicts for CHECKED/DEFAULT etc.

        Returns:
            Checkbox widget dict.
        """
        props = self._base_props(name, x_offset, y_offset, 100, 20, align,
                                 content_fit=True)
        props.extend([
            {"nid": 1010, "strtype": "CHECKBOX/Checkbox",
             "InheritedType": 1},
            {"nid": 1020, "strtype": "CHECKBOX/Title", "strval": title,
             "InheritedType": 10},
        ])

        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state", "strval": "DEFAULT",
                "childs": style,
            })
        props.append(self._style_part("CHECKBOX", "MAIN", "main", 1030,
                                       childs=style_childs))
        props.append(self._checkbox_bullet_part(1040,
                                                 childs=bullet_style or []))

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "CHECKBOX",
        }

    def dropdown(self, name, options=None, size=(150, 35), align="CENTER",
                 x_offset=0, y_offset=0, show_selected=True,
                 list_align="BOTTOM", style=None):
        """
        Create a DROPDOWN widget.

        Args:
            name: Widget name
            options: List of option strings (e.g. ["Option 1", "Option 2"])
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            show_selected: Show selected option text
            list_align: "BOTTOM", "TOP", "LEFT", "RIGHT"
            style: Optional main style

        Returns:
            Dropdown widget dict.
        """
        if options is None:
            options = ["Option 1", "Option 2", "Option 3"]
        # Options use literal \\n (not real newlines) — this is critical!
        options_str = "\\n".join(options)

        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "DROPDOWN/Dropdown",
             "InheritedType": 1},
            {"nid": 1020, "strtype": "DROPDOWN/Options",
             "strval": options_str, "InheritedType": 10},
            {"nid": 1030, "strtype": "DROPDOWN/Base_text", "strval": "",
             "InheritedType": 10},
            {"nid": 1040, "strtype": "DROPDOWN/Show_selected",
             "strval": "True" if show_selected else "False",
             "InheritedType": 2},
            {"nid": 1050, "strtype": "DROPDOWN/List_align",
             "strval": list_align, "InheritedType": 3},
        ])

        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state", "strval": "DEFAULT",
                "childs": style,
            })
        props.extend([
            self._style_part("DROPDOWN", "MAIN", "main", 1060,
                              childs=style_childs),
            self._style_part("DROPDOWN", "INDICATOR", "indicator", 1070),
        ])

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "DROPDOWN",
        }

    def roller(self, name, options=None, selected=0, visible_rows=3,
               size=(100, 100), align="CENTER", x_offset=0, y_offset=0,
               mode="NORMAL", style=None, selected_style=None):
        """
        Create a ROLLER widget.

        Args:
            name: Widget name
            options: List of option strings
            selected: Selected index (0-based)
            visible_rows: Number of visible rows
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            mode: "NORMAL" or "INFINITE"
            style: Optional main style
            selected_style: Optional selected row style

        Returns:
            Roller widget dict.
        """
        if options is None:
            options = ["Option 1", "Option 2", "Option 3"]
        # Same \\n convention as dropdown
        options_str = "\\n".join(options)

        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "ROLLER/Roller", "InheritedType": 1},
            {"nid": 1020, "strtype": "ROLLER/Options",
             "strval": options_str, "InheritedType": 10},
            {"nid": 1030, "strtype": "ROLLER/Selected", "integer": selected,
             "InheritedType": 6},
            {"nid": 1040, "strtype": "ROLLER/Mode", "strval": mode,
             "InheritedType": 3},
        ])

        for part_args in [
            ("ROLLER", "MAIN", "main", 1050, style),
            ("ROLLER", "SELECTED", "selected", 1060, selected_style),
        ]:
            prefix, part_name, part_label, nid, part_style = part_args
            childs = []
            if part_style:
                childs.append({
                    "strtype": "_stylestate/state", "strval": "DEFAULT",
                    "childs": part_style,
                })
            props.append(self._style_part(prefix, part_name, part_label, nid,
                                           childs=childs))

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "ROLLER",
        }

    def textarea(self, name, text="", placeholder="", max_length=98989898,
                 one_line=False, password=False, size=(200, 100),
                 align="CENTER", x_offset=0, y_offset=0, style=None):
        """
        Create a TEXTAREA widget.

        Args:
            name: Widget name
            text: Initial text content
            placeholder: Placeholder text
            max_length: Maximum text length (default: effectively unlimited)
            one_line: Single-line mode
            password: Password masking mode
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            style: Optional main style

        Returns:
            Textarea widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "TEXTAREA/TextArea",
             "InheritedType": 1},
            {"nid": 1020, "strtype": "TEXTAREA/Text", "strval": text,
             "InheritedType": 10},
            {"nid": 1030, "strtype": "TEXTAREA/Placeholder",
             "strval": placeholder, "InheritedType": 10},
            {"nid": 1040, "strtype": "TEXTAREA/Accepted_characters",
             "strval": "", "InheritedType": 10},
            {"nid": 1050, "strtype": "TEXTAREA/Max_text_length",
             "integer": max_length, "InheritedType": 6},
            {"nid": 1060, "strtype": "TEXTAREA/One_line_mode",
             "strval": "True" if one_line else "False", "InheritedType": 2},
            {"nid": 1070, "strtype": "TEXTAREA/Password_mode",
             "strval": "True" if password else "False", "InheritedType": 2},
        ])

        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state", "strval": "DEFAULT",
                "childs": style,
            })
        props.extend([
            self._style_part("TEXTAREA", "MAIN", "main", 1080,
                              childs=style_childs),
            self._style_part("TEXTAREA", "CURSOR", "cursor", 1090),
            self._style_part("TEXTAREA", "PLACEHOLDER", "placeholder", 1100),
            self._style_part("TEXTAREA", "SELECTED", "selected", 1110),
        ])

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "TEXTAREA",
        }

    def spinner(self, name, size=(100, 100), align="CENTER",
                x_offset=0, y_offset=0, style=None, indicator_style=None):
        """
        Create a SPINNER widget.

        Args:
            name: Widget name
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            style: Optional main style
            indicator_style: Optional indicator style

        Returns:
            Spinner widget dict.
        """
        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.append(
            {"nid": 1010, "strtype": "SPINNER/Spinner", "InheritedType": 1})

        for part_args in [
            ("SPINNER", "MAIN", "main", 1020, style),
            ("SPINNER", "INDICATOR", "indicator", 1030, indicator_style),
        ]:
            prefix, part_name, part_label, nid, part_style = part_args
            childs = []
            if part_style:
                childs.append({
                    "strtype": "_stylestate/state", "strval": "DEFAULT",
                    "childs": part_style,
                })
            props.append(self._style_part(prefix, part_name, part_label, nid,
                                           childs=childs))

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "SPINNER",
        }

    def tabview(self, name, tab_names=None, tab_position="TOP", tab_size=50,
                size=(300, 200), align="CENTER", x_offset=0, y_offset=0,
                style=None):
        """
        Create a TABVIEW widget with TABPAGEs.

        Args:
            name: Widget name
            tab_names: List of tab title strings
            tab_position: "TOP", "BOTTOM", "LEFT", "RIGHT"
            tab_size: Tab button height/width in px
            size: (width, height)
            align: Alignment
            x_offset, y_offset: Position offset
            style: Optional main style

        Returns:
            Tabview widget dict. Tabpages are in result["children"].
        """
        if tab_names is None:
            tab_names = ["Tab 1", "Tab 2"]

        w, h = size
        props = self._base_props(name, x_offset, y_offset, w, h, align)
        props.extend([
            {"nid": 1010, "strtype": "TABVIEW/Tabview", "InheritedType": 1},
            {"nid": 1020, "strtype": "TABVIEW/Tab_position",
             "strval": tab_position, "InheritedType": 3},
            {"nid": 1030, "strtype": "TABVIEW/Tab_size",
             "integer": tab_size, "InheritedType": 6},
            {"nid": 1040, "strtype": "TABVIEW/Tabpages",
             "InheritedType": 1},
        ])

        style_childs = []
        if style:
            style_childs.append({
                "strtype": "_stylestate/state", "strval": "DEFAULT",
                "childs": style,
            })
        props.extend([
            self._style_part("TABVIEW", "MAIN", "main", 1050,
                              childs=style_childs),
            self._style_part("TABVIEW", "MAIN", "buttons_main", 1060),
            self._style_part("TABVIEW", "ITEMS", "buttons_items", 1070),
        ])

        # Create TABPAGEs — these use TABPAGE/ prefix for everything
        tabpages = []
        for tab_title in tab_names:
            tab_name = tab_title.replace(" ", "_")
            tabpages.append(self._tabpage(tab_name, tab_title))

        return {
            "guid": self._guid(), "children": tabpages,
            "properties": props, "saved_objtypeKey": "TABVIEW",
        }

    def _tabpage(self, name, title):
        """Create a TABPAGE child widget (uses TABPAGE/ prefix)."""
        # TABPAGE uses its own prefix for ALL properties
        props = [
            {"nid": 10, "strtype": "TABPAGE/Name", "strval": name,
             "InheritedType": 10},
            {"nid": 20, "strtype": "TABPAGE/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0, "nid": 30, "strtype": "TABPAGE/Layout_type",
                "strval": "No_layout", "InheritedType": 13,
            },
            {"nid": 40, "strtype": "TABPAGE/Transform", "InheritedType": 1},
            {"nid": 90, "flags": 1048576, "strtype": "TABPAGE/Flags",
             "InheritedType": 1},
            {"nid": 225, "flags": 1048576, "strtype": "TABPAGE/Scrolling",
             "InheritedType": 1},
            {"nid": 230, "strtype": "TABPAGE/Scrollable",
             "strval": "False", "InheritedType": 2},
            {"nid": 300, "strtype": "TABPAGE/Scrollbar_mode",
             "strval": "AUTO", "InheritedType": 3},
            {"nid": 310, "strtype": "TABPAGE/Scroll_direction",
             "strval": "ALL", "InheritedType": 3},
            {"nid": 314, "strtype": "TABPAGE/Scroll_snap_x",
             "strval": "NONE", "InheritedType": 3},
            {"nid": 315, "strtype": "TABPAGE/Scroll_snap_y",
             "strval": "NONE", "InheritedType": 3},
            {"nid": 320, "flags": 1048576, "strtype": "TABPAGE/States",
             "InheritedType": 1},
            {"nid": 1010, "strtype": "TABPAGE/TabPage", "InheritedType": 1},
            {"nid": 1020, "strtype": "TABPAGE/Title", "strval": title,
             "InheritedType": 10},
            self._style_part("TABPAGE", "MAIN", "main", 1030),
            self._style_part("TABPAGE", "SCROLLBAR", "scrollbar", 1040),
        ]

        return {
            "guid": self._guid(), "children": [], "properties": props,
            "saved_objtypeKey": "TABPAGE",
        }

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------

    def add_children(self, parent, children):
        """
        Add child widgets to a parent widget's children list.

        Args:
            parent: Parent widget dict (screen, panel, button, etc.)
            children: List of child widget dicts, or a single widget dict
        """
        if isinstance(children, dict):
            children = [children]
        parent["children"].extend(children)

    def add_event(self, widget, trigger, action, event_name=None):
        """
        Add an event handler to a widget.

        Args:
            widget: Widget dict to add the event to
            trigger: Event trigger ("CLICKED", "VALUE_CHANGED", etc.)
            action: Action dict from change_screen(), call_function(), etc.
            event_name: Optional display name for the event
        """
        widget["properties"].append(
            self.event_handler(trigger, action, event_name))

    def get_guid(self, widget):
        """Get the GUID of a widget."""
        return widget["guid"]
