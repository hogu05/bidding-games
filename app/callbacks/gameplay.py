from dash import Input, Output, State, ctx, no_update

from ai import computer_bid, computer_move
from auctions import AUCTIONS
from bidding import resolve_bid_winner
import ids
from dash_app import app
from domain import AuctionKind, Mode, PLAYER_TO_SIDE, Phase, Side
from graph_elements import build_elements
from state import game_state
from validation import bid_is_valid


def _target_outcome(node: int) -> tuple[Phase, Side | None]:
    if node == game_state.game.p1_target:
        return Phase.GAME_OVER, Side.P1
    if node == game_state.game.p2_target:
        return Phase.GAME_OVER, Side.P2
    return Phase.P1_BID, None


def _no_change(phase, p1_bid_val, p1_budget, p2_budget, node):
    return (
        phase,
        p1_bid_val,
        None,
        p1_budget,
        p2_budget,
        node,
        build_elements(game_state.game, node),
        no_update,
        no_update,
    )


def _lock_pvp(triggered_id, phase, p1_input, p2_input, p1_bid_val, p1_budget, p2_budget, auction, node):
    if triggered_id == ids.P1_LOCK_BTN and phase == Phase.P1_BID:
        if not bid_is_valid(p1_input, p1_budget):
            return None
        p1_bid = int(p1_input or 0)
        return (
            Phase.P2_BID,
            p1_bid,
            None,
            p1_budget,
            p2_budget,
            node,
            build_elements(game_state.game, node),
            no_update,
            no_update,
        )

    if triggered_id == ids.P2_LOCK_BTN and phase == Phase.P2_BID:
        if not bid_is_valid(p2_input, p2_budget):
            return None
        p1_bid = p1_bid_val or 0
        p2_bid = int(p2_input or 0)
        winner = resolve_bid_winner(p1_bid, p2_bid, PLAYER_TO_SIDE[game_state.game.tiebreaker])
        new_p1_budget, new_p2_budget = AUCTIONS[auction].resolve_budgets(p1_budget, p2_budget, p1_bid, p2_bid)
        return (
            Phase.MOVING,
            None,
            winner,
            new_p1_budget,
            new_p2_budget,
            node,
            build_elements(game_state.game, node),
            p1_bid,
            p2_bid,
        )

    return None


def _lock_pva(triggered_id, phase, p1_input, _p2_input, _p1_bid_val, p1_budget, p2_budget, auction, node):
    if triggered_id != ids.P1_LOCK_BTN or phase != Phase.P1_BID:
        return None
    if not bid_is_valid(p1_input, p1_budget):
        return None

    p1_bid = int(p1_input or 0)
    p2_bid = computer_bid(node, p1_budget, p2_budget, auction)
    winner = resolve_bid_winner(p1_bid, p2_bid, PLAYER_TO_SIDE[game_state.game.tiebreaker])
    new_p1_budget, new_p2_budget = AUCTIONS[auction].resolve_budgets(p1_budget, p2_budget, p1_bid, p2_bid)

    if winner == Side.P1:
        return (
            Phase.MOVING,
            None,
            Side.P1,
            new_p1_budget,
            new_p2_budget,
            node,
            build_elements(game_state.game, node),
            p1_bid,
            p2_bid,
        )

    new_node = computer_move(node, new_p1_budget, new_p2_budget, auction)
    new_phase, side_winner = _target_outcome(new_node)
    return (
        new_phase,
        None,
        side_winner,
        new_p1_budget,
        new_p2_budget,
        new_node,
        build_elements(game_state.game, new_node),
        p1_bid,
        p2_bid,
    )


_LOCK_HANDLERS = {Mode.PVP: _lock_pvp, Mode.PVA: _lock_pva}


@app.callback(
    Output(ids.PHASE, "data"),
    Output(ids.P1_BID_VALUE, "data"),
    Output(ids.WINNER, "data"),
    Output(ids.P1_BUDGET, "data"),
    Output(ids.P2_BUDGET, "data"),
    Output(ids.CURRENT_NODE, "data", allow_duplicate=True),
    Output(ids.GRAPH, "elements", allow_duplicate=True),
    Output(ids.LAST_P1_BID, "data"),
    Output(ids.LAST_P2_BID, "data"),
    Input(ids.P1_LOCK_BTN, "n_clicks"),
    Input(ids.P2_LOCK_BTN, "n_clicks"),
    State(ids.PHASE, "data"),
    State(ids.P1_BID_INPUT, "value"),
    State(ids.P2_BID_INPUT, "value"),
    State(ids.P1_BID_VALUE, "data"),
    State(ids.P1_BUDGET, "data"),
    State(ids.P2_BUDGET, "data"),
    State(ids.AUCTION, "data"),
    State(ids.MODE, "data"),
    State(ids.CURRENT_NODE, "data"),
    prevent_initial_call=True,
)
def handle_lock(_, __, phase, p1_input, p2_input, p1_bid_val, p1_budget, p2_budget, auction, mode, node):
    handler = _LOCK_HANDLERS.get(Mode(mode))
    result = None
    if handler is not None:
        result = handler(
            ctx.triggered_id, phase, p1_input, p2_input, p1_bid_val, p1_budget, p2_budget, AuctionKind(auction), node
        )
    return result if result is not None else _no_change(phase, p1_bid_val, p1_budget, p2_budget, node)


@app.callback(
    Output(ids.CURRENT_NODE, "data"),
    Output(ids.GRAPH, "elements"),
    Output(ids.PHASE, "data", allow_duplicate=True),
    Output(ids.WINNER, "data", allow_duplicate=True),
    Input(ids.GRAPH, "tapNodeData"),
    State(ids.CURRENT_NODE, "data"),
    State(ids.PHASE, "data"),
    State(ids.MODE, "data"),
    prevent_initial_call=True,
)
def on_node_click(tap_data, current_node, phase, mode):
    if tap_data is None:
        return current_node, build_elements(game_state.game, current_node), phase, no_update

    clicked = int(tap_data["id"])

    if mode == Mode.ANALYSIS:
        return clicked, build_elements(game_state.game, clicked), phase, no_update

    if phase != Phase.MOVING or clicked not in game_state.game.adj_list[current_node]:
        return current_node, build_elements(game_state.game, current_node), phase, no_update

    new_phase, winner = _target_outcome(clicked)
    return clicked, build_elements(game_state.game, clicked), new_phase, winner
