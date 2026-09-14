from dash import Input, Output, State, ctx, no_update

import ids
import styles
from dash_app import app
from domain import AuctionKind, Mode, Phase


@app.callback(
    Output(ids.MODE, "data"),
    Output(ids.BTN_PVP, "style"),
    Output(ids.BTN_PVA, "style"),
    Output(ids.BTN_ANALYSIS, "style"),
    Output(ids.P1_BUDGET, "data", allow_duplicate=True),
    Output(ids.P2_BUDGET, "data", allow_duplicate=True),
    Output(ids.PHASE, "data", allow_duplicate=True),
    Output(ids.P1_BID_VALUE, "data", allow_duplicate=True),
    Output(ids.WINNER, "data", allow_duplicate=True),
    Output(ids.P1_BID_INPUT, "value", allow_duplicate=True),
    Output(ids.P2_BID_INPUT, "value", allow_duplicate=True),
    Input(ids.BTN_PVP, "n_clicks"),
    Input(ids.BTN_PVA, "n_clicks"),
    Input(ids.BTN_ANALYSIS, "n_clicks"),
    State(ids.MODE, "data"),
    State(ids.ANALYSIS_P1_INPUT, "value"),
    State(ids.ANALYSIS_P2_INPUT, "value"),
    prevent_initial_call=True,
)
def select_mode(_, __, ___, previous_mode, analysis_p1, analysis_p2):
    mode = Mode(ctx.triggered_id.removeprefix("btn-"))

    if previous_mode == Mode.ANALYSIS and mode != Mode.ANALYSIS:
        new_p1_budget = max(0, int(analysis_p1 or 0))
        new_p2_budget = max(0, int(analysis_p2 or 0))
    else:
        new_p1_budget = no_update
        new_p2_budget = no_update

    if mode == Mode.ANALYSIS:
        new_p1_bid_input, new_p2_bid_input = no_update, no_update
    else:
        new_p1_bid_input, new_p2_bid_input = 0, 0

    return (
        mode,
        *(styles.BTN_ACTIVE if m == mode else styles.BTN_INACTIVE for m in Mode),
        new_p1_budget,
        new_p2_budget,
        Phase.P1_BID,
        None,
        None,
        new_p1_bid_input,
        new_p2_bid_input,
    )


@app.callback(
    Output(ids.AUCTION, "data"),
    Output(ids.BTN_POORMAN, "style"),
    Output(ids.BTN_RICHMAN, "style"),
    Input(ids.BTN_POORMAN, "n_clicks"),
    Input(ids.BTN_RICHMAN, "n_clicks"),
    prevent_initial_call=True,
)
def select_auction(_, __):
    auction = AuctionKind(ctx.triggered_id.removeprefix("btn-"))
    return (
        auction,
        *(styles.BTN_ACTIVE if a == auction else styles.BTN_INACTIVE for a in AuctionKind),
    )


@app.callback(
    Output(ids.GAME_CONTROLS, "style"),
    Output(ids.ANALYSIS_CONTROLS, "style"),
    Output(ids.ANALYSIS_PANEL, "style"),
    Output(ids.GRAPH_LOADING, "style"),
    Output(ids.GRAPH, "style"),
    Output(ids.GRAPH, "layout"),
    Input(ids.MODE, "data"),
    prevent_initial_call=True,
)
def toggle_controls(mode):
    mode = Mode(mode)
    return (
        styles.controls_bar_style(visible=mode != Mode.ANALYSIS),
        styles.controls_bar_style(visible=mode == Mode.ANALYSIS),
        styles.analysis_panel_style(mode),
        styles.graph_loading_style(mode),
        styles.graph_box_style(mode),
        styles.CYTOSCAPE_LAYOUT,
    )


@app.callback(
    Output(ids.P2_BID_CONTROLS, "style"),
    Input(ids.MODE, "data"),
)
def toggle_p2_controls(mode):
    return styles.P2_BID_CONTROLS_HIDDEN if mode == Mode.PVA else styles.P2_BID_CONTROLS_VISIBLE
