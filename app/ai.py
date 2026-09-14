import random

from domain import AuctionKind, Side, SIDE_TO_PLAYER
from state import game_state

_AI_SIDE = SIDE_TO_PLAYER[Side.P2]


def computer_bid(node: int, p1_budget: int, p2_budget: int, auction: AuctionKind) -> int:
    strategy = game_state.strategy(auction, node, p1_budget, p2_budget, _AI_SIDE)
    return random.choices(range(len(strategy)), weights=strategy)[0]


def computer_move(node: int, p1_budget: int, p2_budget: int, auction: AuctionKind) -> int:
    return game_state.best_move(auction, node, p1_budget, p2_budget)
