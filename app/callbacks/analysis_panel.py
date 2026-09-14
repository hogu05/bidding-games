from dash import Input, Output, State, no_update

from allpay import Player

import colors
import ids
from components import strategy_panel, win_probability_row
from dash_app import app
from domain import AuctionKind, Mode
from state import game_state


@app.callback(
    Output(ids.ANALYSIS_P1_INPUT, "value"),
    Output(ids.ANALYSIS_P2_INPUT, "value"),
    Input(ids.MODE, "data"),
    State(ids.P1_BUDGET, "data"),
    State(ids.P2_BUDGET, "data"),
    prevent_initial_call=True,
)
def sync_on_mode_change(mode, p1_budget, p2_budget):
    if mode == Mode.ANALYSIS:
        return p1_budget, p2_budget
    return no_update, no_update


@app.callback(
    Output(ids.ANALYSIS_CONTENT, "children"),
    Input(ids.CURRENT_NODE, "data"),
    Input(ids.ANALYSIS_P1_INPUT, "value"),
    Input(ids.ANALYSIS_P2_INPUT, "value"),
    Input(ids.AUCTION, "data"),
    Input(ids.MODE, "data"),
)
def update_analysis(node, p1_input, p2_input, auction, mode):
    if mode != Mode.ANALYSIS or node is None:
        return []

    auction = AuctionKind(auction)
    p1_budget = max(0, int(p1_input or 0))
    p2_budget = max(0, int(p2_input or 0))

    win_probability = game_state.win_probability(auction, node, p1_budget, p2_budget)
    content = [win_probability_row(win_probability)]

    if node in (game_state.game.p1_target, game_state.game.p2_target):
        return content

    p1_strategy = game_state.strategy(auction, node, p1_budget, p2_budget, Player.P1)
    p2_strategy = game_state.strategy(auction, node, p1_budget, p2_budget, Player.P2)
    content += strategy_panel("P1 strategy", colors.P1, p1_strategy)
    content += strategy_panel("P2 strategy", colors.P2, p2_strategy, margin_top="10px")
    return content
