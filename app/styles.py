import colors
from domain import Mode

TOP_BAR_HEIGHT = "80px"
BOTTOM_BAR_HEIGHT = "80px"
PANEL_WIDTH = "420px"

FONT_FAMILY = (
    "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, "
    "Arial, sans-serif"
)
FONT_SIZE = "24px"

CYTOSCAPE_LAYOUT = {"name": "breadthfirst", "directed": True}

DISPLAY_BLOCK = {"display": "block"}
DISPLAY_NONE = {"display": "none"}

BTN_BASE = {
    "border": "none",
    "padding": "4px 14px",
    "borderRadius": "4px",
    "cursor": "pointer",
    "fontSize": FONT_SIZE,
    "fontFamily": FONT_FAMILY,
    "fontWeight": "500",
}
BTN_ACTIVE = {**BTN_BASE, "backgroundColor": colors.ACTIVE, "color": colors.TEXT}
BTN_INACTIVE = {**BTN_BASE, "backgroundColor": "transparent", "color": colors.MUTED}

INPUT_STYLE = {
    "width": "80px",
    "padding": "4px 8px",
    "borderRadius": "4px",
    "border": f"1px solid {colors.ACTIVE}",
    "backgroundColor": colors.SURFACE,
    "color": colors.TEXT,
    "fontSize": FONT_SIZE,
    "fontFamily": FONT_FAMILY,
    "textAlign": "center",
}

LOCK_BTN = {
    **BTN_BASE,
    "backgroundColor": colors.SUCCESS,
    "color": colors.TEXT,
    "padding": "4px 12px",
}
LOCK_BTN_DISABLED = {**LOCK_BTN, "backgroundColor": colors.ACTIVE, "color": colors.MUTED, "cursor": "not-allowed"}

START_GAME_BTN = {**BTN_BASE, "backgroundColor": colors.SUCCESS, "color": colors.TEXT}
START_GAME_BTN_DISABLED = {
    **BTN_BASE,
    "backgroundColor": colors.ACTIVE,
    "color": colors.MUTED,
    "cursor": "not-allowed",
}

MODAL_LABEL = {"color": colors.MUTED, "fontSize": FONT_SIZE, "fontFamily": FONT_FAMILY, "marginBottom": "6px"}
MODAL_INPUT = {**INPUT_STYLE, "width": "100%", "boxSizing": "border-box"}
MODAL_TITLE = {"color": colors.TEXT, "fontSize": FONT_SIZE, "fontWeight": "600", "marginBottom": "20px"}
MODAL_BOX = {
    "backgroundColor": colors.BACKGROUND,
    "border": f"1px solid {colors.BORDER}",
    "borderRadius": "8px",
    "padding": "24px",
    "width": "320px",
}
MODAL_OVERLAY_HIDDEN = {"display": "none"}
MODAL_OVERLAY_VISIBLE = {
    "display": "flex",
    "position": "fixed",
    "top": 0,
    "left": 0,
    "width": "100vw",
    "height": "100vh",
    "backgroundColor": colors.OVERLAY,
    "zIndex": 300,
    "alignItems": "center",
    "justifyContent": "center",
}

SEGMENTED_GROUP = {
    "display": "flex",
    "gap": "4px",
    "backgroundColor": colors.SURFACE,
    "borderRadius": "6px",
    "padding": "4px",
}


def segmented_group_style(margin_bottom: str | None = None) -> dict:
    if margin_bottom is None:
        return SEGMENTED_GROUP
    return {**SEGMENTED_GROUP, "marginBottom": margin_bottom}


CONTROLS_BAR = {"display": "flex", "width": "100%", "alignItems": "center", "justifyContent": "space-between"}
CONTROLS_BAR_HIDDEN = {**CONTROLS_BAR, "display": "none"}


def controls_bar_style(visible: bool) -> dict:
    return CONTROLS_BAR if visible else CONTROLS_BAR_HIDDEN


P2_BID_CONTROLS_VISIBLE = {"display": "flex", "gap": "8px"}
P2_BID_CONTROLS_HIDDEN = {"display": "none"}


def _bar_style(edge: str, height: str) -> dict:
    return {
        "position": "fixed",
        edge: 0,
        "left": 0,
        "width": "100%",
        "height": height,
        "backgroundColor": colors.BACKGROUND,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "padding": "0 16px",
        "boxSizing": "border-box",
        "zIndex": 100,
    }


def top_bar_style() -> dict:
    return _bar_style("top", TOP_BAR_HEIGHT)


def bottom_bar_style() -> dict:
    return _bar_style("bottom", BOTTOM_BAR_HEIGHT)


def content_height() -> str:
    return f"calc(100vh - {TOP_BAR_HEIGHT} - {BOTTOM_BAR_HEIGHT})"


def graph_width(mode: Mode) -> str:
    return f"calc(100vw - {PANEL_WIDTH})" if mode == Mode.ANALYSIS else "100vw"


def graph_box_style(mode: Mode) -> dict:
    return {
        "position": "fixed",
        "top": TOP_BAR_HEIGHT,
        "left": 0,
        "width": graph_width(mode),
        "height": content_height(),
    }


def graph_loading_style(mode: Mode) -> dict:
    return {**graph_box_style(mode), "zIndex": 200}


def analysis_panel_style(mode: Mode) -> dict:
    return {
        "position": "fixed",
        "top": TOP_BAR_HEIGHT,
        "right": 0,
        "width": PANEL_WIDTH,
        "height": content_height(),
        "backgroundColor": colors.BACKGROUND,
        "borderLeft": f"1px solid {colors.BORDER}",
        "padding": "12px",
        "boxSizing": "border-box",
        "overflowY": "auto",
        "zIndex": 50,
        "display": "block" if mode == Mode.ANALYSIS else "none",
    }
