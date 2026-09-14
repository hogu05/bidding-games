from dash import Input, Output, State, no_update

import ids
import styles
from dash_app import app
from domain import Mode, Phase, Side
from validation import bid_is_valid


def _lock_style(disabled: bool) -> dict:
    return styles.LOCK_BTN_DISABLED if disabled else styles.LOCK_BTN


def _side_label(side: Side, mode: Mode) -> str:
    if side == Side.P1:
        return "P1"
    return "AI" if mode == Mode.PVA else "P2"


@app.callback(
    Output(ids.P1_BUDGET_DISPLAY, "children"),
    Output(ids.P2_BUDGET_DISPLAY, "children"),
    Output(ids.STATUS_MSG, "children"),
    Output(ids.P1_BID_INPUT, "disabled"),
    Output(ids.P2_BID_INPUT, "disabled"),
    Output(ids.P1_LOCK_BTN, "disabled"),
    Output(ids.P2_LOCK_BTN, "disabled"),
    Output(ids.P1_LOCK_BTN, "style"),
    Output(ids.P2_LOCK_BTN, "style"),
    Output(ids.P1_BID_INPUT, "value"),
    Output(ids.P2_BID_INPUT, "value"),
    Input(ids.PHASE, "data"),
    Input(ids.P1_BUDGET, "data"),
    Input(ids.P2_BUDGET, "data"),
    Input(ids.MODE, "data"),
    State(ids.WINNER, "data"),
    State(ids.LAST_P1_BID, "data"),
    State(ids.LAST_P2_BID, "data"),
)
def update_ui(phase, p1_budget, p2_budget, mode, winner, last_p1_bid, last_p2_bid):
    p1_label = f"P1: {p1_budget}"
    p2_label = f"{'AI' if mode == Mode.PVA else 'P2'}: {p2_budget}"

    if phase == Phase.P1_BID:
        p1_locked, p2_locked = False, True
        status = "P1: enter your bid"
    elif phase == Phase.P2_BID:
        p1_locked, p2_locked = True, False
        status = "P2: enter your bid"
    elif phase == Phase.GAME_OVER:
        p1_locked, p2_locked = True, True
        status = f"{_side_label(winner, mode)} wins! Press New Game to play again."
    else:
        p1_locked, p2_locked = True, True
        score = f"{last_p1_bid} vs {last_p2_bid}"
        status = f"{_side_label(winner, mode)} won the bid ({score}) - click a neighbor to move"

    return (
        p1_label,
        p2_label,
        status,
        p1_locked,
        p2_locked,
        p1_locked,
        p2_locked,
        _lock_style(p1_locked),
        _lock_style(p2_locked),
        0 if mode != Mode.ANALYSIS else no_update,
        0 if mode != Mode.ANALYSIS else no_update,
    )


@app.callback(
    Output(ids.P1_LOCK_BTN, "disabled", allow_duplicate=True),
    Output(ids.P2_LOCK_BTN, "disabled", allow_duplicate=True),
    Output(ids.P1_LOCK_BTN, "style", allow_duplicate=True),
    Output(ids.P2_LOCK_BTN, "style", allow_duplicate=True),
    Input(ids.P1_BID_INPUT, "value"),
    Input(ids.P2_BID_INPUT, "value"),
    State(ids.PHASE, "data"),
    State(ids.MODE, "data"),
    State(ids.P1_BUDGET, "data"),
    State(ids.P2_BUDGET, "data"),
    prevent_initial_call=True,
)
def validate_bid_inputs(p1_input, p2_input, phase, mode, p1_budget, p2_budget):
    p1_ok = phase == Phase.P1_BID and bid_is_valid(p1_input, p1_budget)
    p2_ok = mode == Mode.PVP and phase == Phase.P2_BID and bid_is_valid(p2_input, p2_budget)
    return not p1_ok, not p2_ok, _lock_style(not p1_ok), _lock_style(not p2_ok)
