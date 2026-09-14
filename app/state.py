from dataclasses import dataclass

from allpay import Game
from games import make_tow

from auctions import AUCTIONS
from domain import AuctionKind, GameType, Side, SIDE_TO_PLAYER

DEFAULT_TOW_LENGTH = 3
DEFAULT_RACE_DISTANCE = 3
DEFAULT_BUDGET = 10


def initial_start_node(game: Game, game_type: GameType) -> int:
    return 0 if game_type == GameType.RACE else len(game.adj_list) // 2


@dataclass
class GameSetup:
    game: Game
    game_type: GameType
    tow_length: int
    race_p1_distance: int
    race_p2_distance: int
    tiebreaker: Side
    p1_budget: int
    p2_budget: int


class GameState:
    def __init__(self, setup: GameSetup):
        self._poorman_cache_budgets = (0, 0)
        self._poorman_cache_values = None
        self._richman_cache = {}
        self.apply(setup)

    def apply(self, setup: GameSetup) -> None:
        self.game = setup.game
        self.start_node = initial_start_node(setup.game, setup.game_type)
        self.game_type = setup.game_type
        self.tow_length = setup.tow_length
        self.race_p1_distance = setup.race_p1_distance
        self.race_p2_distance = setup.race_p2_distance
        self.tiebreaker = setup.tiebreaker
        self.p1_budget = setup.p1_budget
        self.p2_budget = setup.p2_budget

        self._poorman_cache_budgets = (setup.p1_budget, setup.p2_budget)
        self._poorman_cache_values = AUCTIONS[AuctionKind.POORMAN].values_table(
            self.game, setup.p1_budget, setup.p2_budget
        )
        self._richman_cache = {
            setup.p1_budget
            + setup.p2_budget: AUCTIONS[AuctionKind.RICHMAN].values_table(
                self.game, setup.p1_budget, setup.p2_budget
            )
        }

    def values_table(self, auction_kind: AuctionKind, p1_budget: int, p2_budget: int):
        if auction_kind == AuctionKind.POORMAN:
            return self._ensure_poorman_values(p1_budget, p2_budget)
        return self._ensure_richman_values(p1_budget, p2_budget)

    def win_probability(self, auction_kind, node, p1_budget, p2_budget):
        values = self.values_table(auction_kind, p1_budget, p2_budget)
        return AUCTIONS[auction_kind].win_probability(values, node, p1_budget, p2_budget)

    def strategy(self, auction_kind, node, p1_budget, p2_budget, player):
        values = self.values_table(auction_kind, p1_budget, p2_budget)
        return AUCTIONS[auction_kind].strategy(
            self.game, values, node, p1_budget, p2_budget, player
        )

    def best_move(self, auction_kind, node, p1_budget, p2_budget):
        values = self.values_table(auction_kind, p1_budget, p2_budget)
        return AUCTIONS[auction_kind].best_move(self.game, values, node, p1_budget, p2_budget)

    def _ensure_poorman_values(self, p1_budget: int, p2_budget: int):
        cached_p1, cached_p2 = self._poorman_cache_budgets
        if p1_budget > cached_p1 or p2_budget > cached_p2:
            new_p1 = max(p1_budget, cached_p1)
            new_p2 = max(p2_budget, cached_p2)
            self._poorman_cache_values = AUCTIONS[AuctionKind.POORMAN].values_table(
                self.game, new_p1, new_p2
            )
            self._poorman_cache_budgets = (new_p1, new_p2)
        return self._poorman_cache_values

    def _ensure_richman_values(self, p1_budget: int, p2_budget: int):
        total = p1_budget + p2_budget
        if total not in self._richman_cache:
            self._richman_cache[total] = AUCTIONS[AuctionKind.RICHMAN].values_table(
                self.game, p1_budget, p2_budget
            )
        return self._richman_cache[total]


def _default_setup() -> GameSetup:
    game = make_tow(DEFAULT_TOW_LENGTH, tiebreaker=SIDE_TO_PLAYER[Side.P1])
    return GameSetup(
        game=game,
        game_type=GameType.TOW,
        tow_length=DEFAULT_TOW_LENGTH,
        race_p1_distance=DEFAULT_RACE_DISTANCE,
        race_p2_distance=DEFAULT_RACE_DISTANCE,
        tiebreaker=Side.P1,
        p1_budget=DEFAULT_BUDGET,
        p2_budget=DEFAULT_BUDGET,
    )


game_state = GameState(_default_setup())
