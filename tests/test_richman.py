import pytest
from games import make_tow, make_race
from allpay import Player
from checks import assert_richman_thresholds

BUDGET = 10000


@pytest.mark.parametrize(
    "game,node,expected",
    [
        (make_tow(1), 1, lambda b2: b2),
        (make_tow(1, tiebreaker=Player.P2), 1, lambda b2: b2 + 1),
        (make_tow(2), 1, lambda b2: 3 * b2),
        (make_tow(2, tiebreaker=Player.P2), 1, lambda b2: 3 * b2 + 3),
        (make_tow(2), 2, lambda b2: b2 if b2 >= 2 else 0),
        (make_tow(2, tiebreaker=Player.P2), 2, lambda b2: b2 + 1),
        (make_race(10, 1), 0, lambda b2: (2**10 - 1) * b2),
        (make_race(10, 1, tiebreaker=Player.P2), 0, lambda b2: (2**10 - 1) * (b2 + 1)),
    ],
)
def test_richman_threshold(game, node, expected):
    assert_richman_thresholds(game, node, expected, BUDGET)
