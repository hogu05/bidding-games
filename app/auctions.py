from abc import ABC, abstractmethod

from allpay import (
    compute_poorman_values,
    compute_richman_values,
    get_poorman_strategy,
    get_richman_strategy,
)

from domain import AuctionKind


class Auction(ABC):
    kind: AuctionKind

    @abstractmethod
    def values_table(self, game, p1_budget, p2_budget): ...

    @abstractmethod
    def win_probability(self, values, node, p1_budget, p2_budget): ...

    @abstractmethod
    def strategy(self, game, values, node, p1_budget, p2_budget, player): ...

    @abstractmethod
    def best_move(self, game, values, node, p1_budget, p2_budget): ...

    @abstractmethod
    def resolve_budgets(self, p1_budget, p2_budget, p1_bid, p2_bid): ...


class Poorman(Auction):
    kind = AuctionKind.POORMAN

    def values_table(self, game, p1_budget, p2_budget):
        return compute_poorman_values(game, p1_budget, p2_budget)

    def win_probability(self, values, node, p1_budget, p2_budget):
        return values[node][p1_budget][p2_budget]

    def strategy(self, game, values, node, p1_budget, p2_budget, player):
        return get_poorman_strategy(game, node, p1_budget, p2_budget, values, player)

    def best_move(self, game, values, node, p1_budget, p2_budget):
        return min(game.adj_list[node], key=lambda n: values[n][p1_budget][p2_budget])

    def resolve_budgets(self, p1_budget, p2_budget, p1_bid, p2_bid):
        return p1_budget - p1_bid, p2_budget - p2_bid


class Richman(Auction):
    kind = AuctionKind.RICHMAN

    def values_table(self, game, p1_budget, p2_budget):
        return compute_richman_values(game, p1_budget + p2_budget)

    def win_probability(self, values, node, p1_budget, p2_budget):
        return values[node][p1_budget]

    def strategy(self, game, values, node, p1_budget, p2_budget, player):
        return get_richman_strategy(game, node, p1_budget, values, player)

    def best_move(self, game, values, node, p1_budget, p2_budget):
        return min(game.adj_list[node], key=lambda n: values[n][p1_budget])

    def resolve_budgets(self, p1_budget, p2_budget, p1_bid, p2_bid):
        return p1_budget - p1_bid + p2_bid, p2_budget - p2_bid + p1_bid


AUCTIONS: dict[AuctionKind, Auction] = {
    AuctionKind.POORMAN: Poorman(),
    AuctionKind.RICHMAN: Richman(),
}
