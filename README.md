# Reachability in Discrete All-Pay Bidding Games

## Bidding games

Bidding games are two-player zero-sum graph games.
A shared token starts on a vertex of a graph.
Each round, the players place their bids at the same time.
The player with the higher bid wins the round and moves the token.
A fixed player is chosen to win the rounds that end in a tie.
In our setting, each player has a target vertex and wins when the token reaches it (reachability).

Concrete bidding mechanisms vary in three independent properties:

- **Who pays**
  - _first-price_: only the round's winner pays their bid
  - _all-pay_: both players pay their bid every round
- **Who receives the payment**
  - _Richman_: paid to the opponent
  - _poorman_: paid to the bank
- **Bid granularity**
  - _continuous_: no restrictions
  - _discrete_: bids and budgets have to be integers

## Scope

This project implements a solver for discrete all-pay bidding games, in both poorman and Richman variants.
The solver computes:

- **Threshold** - the minimum budget P1 needs to guarantee a win given P2 budget
- **Game value** - the win probability under optimal play given P1 and P2 budgets
- **Strategy** - the optimal mixed bidding strategy given P1 and P2 budgets

## Requirements

- **CMake**: 3.30+
- **Compiler**: C++23
- **Python**: 3.9+
- **OS**: Windows, macOS, Linux

## Build

From the project root:

```bash
pip install .
```

Some tools need extra dependencies:

```bash
pip install --group <tests | app | analysis | all> .
```

## Usage

The solver is used as a Python library.

### Game

`Game` is defined by a directed graph (given as an adjacency list, `adj_list`), a target for each player, and a tiebreaker rule (which player wins on equal bids).

```python
game = Game(
    adj_list=[[], [0, 2], [1, 3], []],
    p1_target=0,
    p2_target=3,
    tiebreaker=Player.P1,
)
```

`RootedGame` is defined by a `Game` and a starting node.

```python
rooted_game = RootedGame(game=game, start_node=1)
```

#### Predefined games

All start at node `0`, except `make_tow`.
All generators also accept a `tiebreaker` argument (default is `Player.P1`).

- `make_tow(n)` - Tug-of-War: a line of `n` nodes between the two targets.
- `make_race(a, b)` - P1 wins after winning `a` rounds, P2 after `b`.
- `make_coins(coins)` - Winner of each round gains the value of the current coin. The player with the higher total value in the end wins.
- `make_game_sum(rooted_games)` - Combines multiple `RootedGame`s. Winning the first round lets a player choose which sub-game to play.

### Solver

| Output      | Poorman                                                                                      | Richman                                                                                                                             |
| ----------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Thresholds  | `compute_poorman_thresholds(game, max_p2_budget) -> [node][p2_budget]`                       | `compute_richman_thresholds(game, total_budget) -> [node]`, or `compute_richman_threshold(game, node, p2_budget)` for a single node |
| Game values | `compute_poorman_values(game, max_p1_budget, max_p2_budget) -> [node][p1_budget][p2_budget]` | `compute_richman_values(game, total_budget) -> [node][p1_budget]`                                                                   |
| Strategy    | `get_poorman_strategy(game, node, p1_budget, p2_budget, values, player) -> [bid]`            | `get_richman_strategy(game, node, p1_budget, values, player) -> [bid]`                                                              |

### Example

```python
from games import make_tow
from allpay import compute_poorman_thresholds, compute_poorman_values, get_poorman_strategy, Player

game = make_tow(3)
thresholds = compute_poorman_thresholds(game, 10)
start_node = 2
for p2_budget in range(11):
    print(p2_budget, thresholds[start_node][p2_budget])

values = compute_poorman_values(game, 10, 10)
print(values[start_node][6][4])
print(get_poorman_strategy(game, start_node, 6, 4, values, Player.P1))
```

## App

Part of the project is an interactive app.
In the app, the user can play against a player (PvP) or the solver (PvA).
Additionally, there is an analysis mode to look at the solver strategy and evaluation for a specific scenario.
The user can choose from the Tug-of-War and the Race games.

Budgets under 25, Tug-of-War length under 10, and Race with the sum of distances under 10 are recommended for a fast response.

### Run

From the project root:

```bash
python app/main.py
```

## Tests

Runs `tests/test_poorman.py` and `tests/test_richman.py`, checking solver thresholds against closed-form expected values for the Tug-of-War and Race games.

```bash
pytest
```

## Documentation

- [Specification](docs/specification.md) (in Czech)
- [Developer documentation](docs/dev_docs.md)
- [Analysis](docs/analysis.md)
