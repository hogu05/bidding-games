from domain import Side


def resolve_bid_winner(p1_bid: int, p2_bid: int, tiebreaker: Side) -> Side:
    if p1_bid != p2_bid:
        return Side.P1 if p1_bid > p2_bid else Side.P2
    return tiebreaker
