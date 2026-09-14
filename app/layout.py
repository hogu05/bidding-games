from dash import dcc, html
import dash_cytoscape as cyto

import colors
import ids
import styles
from components import segmented_control
from domain import AuctionKind, GameType, Mode, Phase, Side
from graph_elements import build_elements
from state import DEFAULT_BUDGET, DEFAULT_RACE_DISTANCE, DEFAULT_TOW_LENGTH, game_state

GRAPH_STYLESHEET = [
    {"selector": "node", "style": {"background-color": colors.MUTED, "overlay-opacity": 0}},
    {"selector": "core", "style": {"active-bg-opacity": 0}},
    {"selector": "edge", "style": {"overlay-opacity": 0}},
    {"selector": ".p1-target", "style": {"background-color": colors.P1}},
    {"selector": ".p2-target", "style": {"background-color": colors.P2}},
    {
        "selector": ".current",
        "style": {"background-color": colors.SUCCESS, "border-width": 3, "border-color": colors.TEXT},
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": colors.EDGE,
            "line-color": colors.EDGE,
            "width": 2,
        },
    },
]


def _build_stores() -> list:
    return [
        dcc.Store(id=ids.CURRENT_NODE, data=game_state.start_node),
        dcc.Store(id=ids.MODE, data=Mode.PVP),
        dcc.Store(id=ids.AUCTION, data=AuctionKind.POORMAN),
        dcc.Store(id=ids.PHASE, data=Phase.P1_BID),
        dcc.Store(id=ids.P1_BUDGET, data=game_state.p1_budget),
        dcc.Store(id=ids.P2_BUDGET, data=game_state.p2_budget),
        dcc.Store(id=ids.P1_BID_VALUE, data=None),
        dcc.Store(id=ids.WINNER, data=None),
        dcc.Store(id=ids.LAST_P1_BID, data=None),
        dcc.Store(id=ids.LAST_P2_BID, data=None),
        dcc.Store(id=ids.GRAPH_REFRESH_DUMMY),
        dcc.Store(id=ids.GRAPH_MIRROR_DUMMY),
        dcc.Store(id=ids.NEW_GAME_TYPE, data=GameType.TOW),
        dcc.Store(id=ids.NEW_TIEBREAKER, data=Side.P1),
    ]


def _build_top_bar() -> html.Div:
    return html.Div(
        style=styles.top_bar_style(),
        children=[
            segmented_control(
                [(ids.BTN_PVP, "PvP"), (ids.BTN_PVA, "PvA"), (ids.BTN_ANALYSIS, "Analysis")],
                active_id=ids.BTN_PVP,
            ),
            html.Button(
                "New Game",
                id=ids.BTN_NEW_GAME,
                style={**styles.BTN_BASE, "backgroundColor": colors.SUCCESS, "color": colors.TEXT},
            ),
            segmented_control(
                [(ids.BTN_POORMAN, "Poorman"), (ids.BTN_RICHMAN, "Richman")],
                active_id=ids.BTN_POORMAN,
            ),
        ],
    )


def _build_graph() -> dcc.Loading:
    return dcc.Loading(
        id=ids.GRAPH_LOADING,
        type="circle",
        style=styles.graph_loading_style(Mode.PVP),
        children=cyto.Cytoscape(
            id=ids.GRAPH,
            elements=build_elements(game_state.game, game_state.start_node),
            layout=styles.CYTOSCAPE_LAYOUT,
            userZoomingEnabled=False,
            userPanningEnabled=False,
            autoungrabify=True,
            style=styles.graph_box_style(Mode.PVP),
            stylesheet=GRAPH_STYLESHEET,
        ),
    )


def _build_analysis_panel() -> html.Div:
    return html.Div(
        id=ids.ANALYSIS_PANEL,
        style=styles.analysis_panel_style(Mode.PVP),
        children=[dcc.Loading(id=ids.ANALYSIS_LOADING, type="circle", children=html.Div(id=ids.ANALYSIS_CONTENT))],
    )


def _build_game_controls() -> html.Div:
    return html.Div(
        id=ids.GAME_CONTROLS,
        style=styles.controls_bar_style(visible=True),
        children=[
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "8px"},
                children=[
                    html.Span(id=ids.P1_BUDGET_DISPLAY, style={"color": colors.P1, "fontSize": styles.FONT_SIZE, "marginRight": "24px"}),
                    dcc.Input(id=ids.P1_BID_INPUT, type="number", value=0, style=styles.INPUT_STYLE),
                    html.Button("Lock", id=ids.P1_LOCK_BTN, style=styles.LOCK_BTN),
                ],
            ),
            html.Div(
                style={
                    "position": "absolute",
                    "left": "50%",
                    "transform": "translateX(-50%)",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "gap": "4px",
                },
                children=[html.Span(id=ids.STATUS_MSG, style={"color": colors.MUTED, "fontSize": styles.FONT_SIZE})],
            ),
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "8px"},
                children=[
                    html.Span(id=ids.P2_BUDGET_DISPLAY, style={"color": colors.P2, "fontSize": styles.FONT_SIZE, "marginRight": "24px"}),
                    html.Div(
                        id=ids.P2_BID_CONTROLS,
                        style=styles.P2_BID_CONTROLS_VISIBLE,
                        children=[
                            dcc.Input(id=ids.P2_BID_INPUT, type="number", value=0, style=styles.INPUT_STYLE),
                            html.Button("Lock", id=ids.P2_LOCK_BTN, style=styles.LOCK_BTN),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_analysis_controls() -> html.Div:
    return html.Div(
        id=ids.ANALYSIS_CONTROLS,
        style=styles.controls_bar_style(visible=False),
        children=[
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "8px"},
                children=[
                    html.Span("P1:", style={"color": colors.P1, "fontSize": styles.FONT_SIZE}),
                    dcc.Input(id=ids.ANALYSIS_P1_INPUT, type="number", value=game_state.p1_budget // 2, style=styles.INPUT_STYLE),
                ],
            ),
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "8px"},
                children=[
                    html.Span("P2:", style={"color": colors.P2, "fontSize": styles.FONT_SIZE}),
                    dcc.Input(id=ids.ANALYSIS_P2_INPUT, type="number", value=game_state.p2_budget // 2, style=styles.INPUT_STYLE),
                ],
            ),
        ],
    )


def _build_bottom_bar() -> html.Div:
    return html.Div(
        style=styles.bottom_bar_style(),
        children=[_build_game_controls(), _build_analysis_controls()],
    )


def _build_new_game_modal() -> html.Div:
    return html.Div(
        id=ids.GAME_MODAL,
        style=styles.MODAL_OVERLAY_HIDDEN,
        children=[
            html.Div(
                style=styles.MODAL_BOX,
                children=[
                    html.Div("New Game", style=styles.MODAL_TITLE),
                    html.Div("Game type", style=styles.MODAL_LABEL),
                    segmented_control(
                        [(ids.BTN_TOW, "Tug of War"), (ids.BTN_RACE, "Race")],
                        active_id=ids.BTN_TOW,
                        margin_bottom="16px",
                    ),
                    html.Div(
                        id=ids.TOW_PARAMS,
                        children=[
                            html.Div("Length", style=styles.MODAL_LABEL),
                            dcc.Input(
                                id=ids.TOW_LENGTH_INPUT,
                                type="number",
                                value=DEFAULT_TOW_LENGTH,
                                style={**styles.MODAL_INPUT, "marginBottom": "16px"},
                            ),
                        ],
                    ),
                    html.Div(
                        id=ids.RACE_PARAMS,
                        style=styles.DISPLAY_NONE,
                        children=[
                            html.Div(
                                style={"display": "flex", "gap": "12px", "marginBottom": "16px"},
                                children=[
                                    html.Div(
                                        style={"flex": 1},
                                        children=[
                                            html.Div("P1 distance", style=styles.MODAL_LABEL),
                                            dcc.Input(id=ids.RACE_A_INPUT, type="number", value=DEFAULT_RACE_DISTANCE, style=styles.MODAL_INPUT),
                                        ],
                                    ),
                                    html.Div(
                                        style={"flex": 1},
                                        children=[
                                            html.Div("P2 distance", style=styles.MODAL_LABEL),
                                            dcc.Input(id=ids.RACE_B_INPUT, type="number", value=DEFAULT_RACE_DISTANCE, style=styles.MODAL_INPUT),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div("Tiebreaker", style=styles.MODAL_LABEL),
                    segmented_control(
                        [(ids.BTN_TIEBREAKER_P1, "P1"), (ids.BTN_TIEBREAKER_P2, "P2")],
                        active_id=ids.BTN_TIEBREAKER_P1,
                        margin_bottom="16px",
                    ),
                    html.Div(
                        style={"display": "flex", "gap": "12px", "marginBottom": "24px"},
                        children=[
                            html.Div(
                                style={"flex": 1},
                                children=[
                                    html.Div("P1 budget", style={**styles.MODAL_LABEL, "color": colors.P1}),
                                    dcc.Input(id=ids.NEW_P1_BUDGET, type="number", value=DEFAULT_BUDGET, style=styles.MODAL_INPUT),
                                ],
                            ),
                            html.Div(
                                style={"flex": 1},
                                children=[
                                    html.Div("P2 budget", style={**styles.MODAL_LABEL, "color": colors.P2}),
                                    dcc.Input(id=ids.NEW_P2_BUDGET, type="number", value=DEFAULT_BUDGET, style=styles.MODAL_INPUT),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        style={"display": "flex", "gap": "8px", "justifyContent": "flex-end"},
                        children=[
                            html.Button(
                                "Cancel",
                                id=ids.BTN_CANCEL_GAME,
                                style={**styles.BTN_BASE, "backgroundColor": colors.SURFACE, "color": colors.MUTED},
                            ),
                            html.Button("Start Game", id=ids.BTN_START_GAME, style=styles.START_GAME_BTN),
                        ],
                    ),
                ],
            )
        ],
    )


def build_layout() -> html.Div:
    return html.Div(
        style={"overflow": "hidden", "margin": 0, "padding": 0, "fontFamily": styles.FONT_FAMILY, "fontSize": styles.FONT_SIZE},
        children=[
            *_build_stores(),
            _build_top_bar(),
            _build_graph(),
            _build_analysis_panel(),
            _build_bottom_bar(),
            _build_new_game_modal(),
        ],
    )


layout = build_layout()
