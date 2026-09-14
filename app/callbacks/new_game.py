from dash import Input, Output, State, ctx, no_update

from games import make_race, make_tow

import ids
import styles
from dash_app import app
from domain import GameType, Phase, Side, SIDE_TO_PLAYER
from graph_elements import build_elements
from state import GameSetup, game_state
from validation import is_natural_number, is_positive_natural_number


def _new_game_inputs_valid(game_type, tow_length, race_p1_distance, race_p2_distance, new_p1_budget, new_p2_budget):
    if game_type == GameType.TOW:
        size_ok = is_positive_natural_number(tow_length)
    else:
        size_ok = is_positive_natural_number(race_p1_distance) and is_positive_natural_number(race_p2_distance)
    budgets_ok = is_natural_number(new_p1_budget) and is_natural_number(new_p2_budget)
    return size_ok and budgets_ok


@app.callback(
    Output(ids.GAME_MODAL, "style"),
    Input(ids.BTN_NEW_GAME, "n_clicks"),
    Input(ids.BTN_CANCEL_GAME, "n_clicks"),
    Input(ids.BTN_START_GAME, "n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal(*_):
    if ctx.triggered_id == ids.BTN_NEW_GAME:
        return styles.MODAL_OVERLAY_VISIBLE
    return styles.MODAL_OVERLAY_HIDDEN


@app.callback(
    Output(ids.NEW_GAME_TYPE, "data"),
    Output(ids.BTN_TOW, "style"),
    Output(ids.BTN_RACE, "style"),
    Output(ids.TOW_PARAMS, "style"),
    Output(ids.RACE_PARAMS, "style"),
    Input(ids.BTN_TOW, "n_clicks"),
    Input(ids.BTN_RACE, "n_clicks"),
    prevent_initial_call=True,
)
def select_game_type(_, __):
    is_tow = ctx.triggered_id == ids.BTN_TOW
    return (
        GameType.TOW if is_tow else GameType.RACE,
        styles.BTN_ACTIVE if is_tow else styles.BTN_INACTIVE,
        styles.BTN_INACTIVE if is_tow else styles.BTN_ACTIVE,
        styles.DISPLAY_BLOCK if is_tow else styles.DISPLAY_NONE,
        styles.DISPLAY_NONE if is_tow else styles.DISPLAY_BLOCK,
    )


@app.callback(
    Output(ids.NEW_TIEBREAKER, "data"),
    Output(ids.BTN_TIEBREAKER_P1, "style"),
    Output(ids.BTN_TIEBREAKER_P2, "style"),
    Input(ids.BTN_TIEBREAKER_P1, "n_clicks"),
    Input(ids.BTN_TIEBREAKER_P2, "n_clicks"),
    prevent_initial_call=True,
)
def select_tiebreaker(_, __):
    is_p1 = ctx.triggered_id == ids.BTN_TIEBREAKER_P1
    return (
        Side.P1 if is_p1 else Side.P2,
        styles.BTN_ACTIVE if is_p1 else styles.BTN_INACTIVE,
        styles.BTN_INACTIVE if is_p1 else styles.BTN_ACTIVE,
    )


@app.callback(
    Output(ids.CURRENT_NODE, "data", allow_duplicate=True),
    Output(ids.GRAPH, "elements", allow_duplicate=True),
    Output(ids.PHASE, "data", allow_duplicate=True),
    Output(ids.P1_BUDGET, "data", allow_duplicate=True),
    Output(ids.P2_BUDGET, "data", allow_duplicate=True),
    Output(ids.P1_BID_VALUE, "data", allow_duplicate=True),
    Output(ids.WINNER, "data", allow_duplicate=True),
    Output(ids.P1_BID_INPUT, "value", allow_duplicate=True),
    Output(ids.P2_BID_INPUT, "value", allow_duplicate=True),
    Input(ids.BTN_START_GAME, "n_clicks"),
    State(ids.NEW_GAME_TYPE, "data"),
    State(ids.TOW_LENGTH_INPUT, "value"),
    State(ids.RACE_A_INPUT, "value"),
    State(ids.RACE_B_INPUT, "value"),
    State(ids.NEW_TIEBREAKER, "data"),
    State(ids.NEW_P1_BUDGET, "value"),
    State(ids.NEW_P2_BUDGET, "value"),
    prevent_initial_call=True,
)
def start_game(_, game_type, tow_length, race_p1_distance, race_p2_distance, tiebreaker, new_p1_budget, new_p2_budget):
    game_type = GameType(game_type)
    tiebreaker = Side(tiebreaker)

    if not _new_game_inputs_valid(game_type, tow_length, race_p1_distance, race_p2_distance, new_p1_budget, new_p2_budget):
        return (no_update,) * 9

    new_p1_budget = int(new_p1_budget)
    new_p2_budget = int(new_p2_budget)

    final_tow_length = game_state.tow_length
    final_race_p1_distance = game_state.race_p1_distance
    final_race_p2_distance = game_state.race_p2_distance

    if game_type == GameType.TOW:
        final_tow_length = int(tow_length)
        game = make_tow(final_tow_length, tiebreaker=SIDE_TO_PLAYER[tiebreaker])
    else:
        final_race_p1_distance = int(race_p1_distance)
        final_race_p2_distance = int(race_p2_distance)
        game = make_race(final_race_p1_distance, final_race_p2_distance, tiebreaker=SIDE_TO_PLAYER[tiebreaker])

    setup = GameSetup(
        game=game,
        game_type=game_type,
        tow_length=final_tow_length,
        race_p1_distance=final_race_p1_distance,
        race_p2_distance=final_race_p2_distance,
        tiebreaker=tiebreaker,
        p1_budget=new_p1_budget,
        p2_budget=new_p2_budget,
    )
    game_state.apply(setup)

    return (
        game_state.start_node,
        build_elements(game_state.game, game_state.start_node),
        Phase.P1_BID,
        game_state.p1_budget,
        game_state.p2_budget,
        None,
        None,
        0,
        0,
    )


@app.callback(
    Output(ids.NEW_GAME_TYPE, "data", allow_duplicate=True),
    Output(ids.BTN_TOW, "style", allow_duplicate=True),
    Output(ids.BTN_RACE, "style", allow_duplicate=True),
    Output(ids.TOW_PARAMS, "style", allow_duplicate=True),
    Output(ids.RACE_PARAMS, "style", allow_duplicate=True),
    Output(ids.TOW_LENGTH_INPUT, "value"),
    Output(ids.RACE_A_INPUT, "value"),
    Output(ids.RACE_B_INPUT, "value"),
    Output(ids.NEW_TIEBREAKER, "data", allow_duplicate=True),
    Output(ids.BTN_TIEBREAKER_P1, "style", allow_duplicate=True),
    Output(ids.BTN_TIEBREAKER_P2, "style", allow_duplicate=True),
    Output(ids.NEW_P1_BUDGET, "value"),
    Output(ids.NEW_P2_BUDGET, "value"),
    Input(ids.BTN_NEW_GAME, "n_clicks"),
    prevent_initial_call=True,
)
def prefill_new_game_modal(_):
    is_tow = game_state.game_type == GameType.TOW
    is_p1_tiebreaker = game_state.tiebreaker == Side.P1
    return (
        game_state.game_type,
        styles.BTN_ACTIVE if is_tow else styles.BTN_INACTIVE,
        styles.BTN_INACTIVE if is_tow else styles.BTN_ACTIVE,
        styles.DISPLAY_BLOCK if is_tow else styles.DISPLAY_NONE,
        styles.DISPLAY_NONE if is_tow else styles.DISPLAY_BLOCK,
        game_state.tow_length,
        game_state.race_p1_distance,
        game_state.race_p2_distance,
        game_state.tiebreaker,
        styles.BTN_ACTIVE if is_p1_tiebreaker else styles.BTN_INACTIVE,
        styles.BTN_INACTIVE if is_p1_tiebreaker else styles.BTN_ACTIVE,
        game_state.p1_budget,
        game_state.p2_budget,
    )


@app.callback(
    Output(ids.BTN_START_GAME, "disabled"),
    Output(ids.BTN_START_GAME, "style"),
    Input(ids.NEW_GAME_TYPE, "data"),
    Input(ids.TOW_LENGTH_INPUT, "value"),
    Input(ids.RACE_A_INPUT, "value"),
    Input(ids.RACE_B_INPUT, "value"),
    Input(ids.NEW_P1_BUDGET, "value"),
    Input(ids.NEW_P2_BUDGET, "value"),
)
def validate_new_game_inputs(game_type, tow_length, race_p1_distance, race_p2_distance, new_p1_budget, new_p2_budget):
    game_type = GameType(game_type)
    ok = _new_game_inputs_valid(game_type, tow_length, race_p1_distance, race_p2_distance, new_p1_budget, new_p2_budget)
    return not ok, (styles.START_GAME_BTN if ok else styles.START_GAME_BTN_DISABLED)
