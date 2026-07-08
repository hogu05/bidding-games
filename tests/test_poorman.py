import pytest
from games import make_tow, make_race
from allpay import Player, compute_poorman_thresholds

BUDGET = 10000


@pytest.mark.parametrize(
    "game,node,expected",
    [
        (make_tow(1), 1, lambda b2: b2),
        (make_tow(1, tiebreaker=Player.P2), 1, lambda b2: b2 + 1),
        (make_tow(2), 1, lambda b2: max(0, 2 * b2 - 1)),
        (make_tow(2, tiebreaker=Player.P2), 1, lambda b2: 2 * b2 + 2),
        (make_tow(2), 2, lambda b2: max(0, b2 - 1)),
        (make_tow(2, tiebreaker=Player.P2), 2, lambda b2: b2 + 1),
        (make_race(10, 1), 0, lambda b2: 10 * b2),
        (make_race(10, 1, tiebreaker=Player.P2), 0, lambda b2: 10 * b2 + 10),
    ],
)
def test_threshold(game, node, expected):
    thresholds = compute_poorman_thresholds(game, BUDGET)
    for p2_budget in range(BUDGET + 1):
        assert thresholds[node][p2_budget] == expected(p2_budget)
