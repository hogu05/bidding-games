# Developer Documentation

## Architecture

- `include/`, `src/` - C++23 solver
- `src/bindings.cpp` - nanobind module `allpay`
- `python/games.py` - game generators
- `python/analysis.py` - research/plotting tools
- `app/` - interactive app

## Data Representation

### Types (`types.hpp`)

- `Node = int` - node index into `Game::adj_list`
- `Coins = int` - a budget/bid amount
- `INF_COINS` - `INT_MAX`, used as an arbitrarily large budget meaning none suffices
- `Player` - `P1` or `P2`

### Game

```
struct Game {
    std::vector<std::vector<Node>> adj_list;
    Node p1_target{};
    Node p2_target{};
    Player tiebreaker{};
};
```

`Game::flipped()` returns the same graph with `p1_target`/`p2_target` and `tiebreaker` swapped.
It is used to compute P2's winning thresholds.

`RootedGame` pairs a `Game` with a `start_node`.
It is used as the specific scenario for the actual game.

## Poorman

In poorman, payments leave the game, so the players' budgets are independent.
The solver tracks both budgets as separate dimensions.

### `compute_thresholds`

For every P2 budget from `0` to `max_p2_budget`, computes every node's threshold in Dijkstra-style.
The threshold of a node is computed by finding the optimal bid.
The optimal bid is found with binary search.
When P1 wins ties, the search suffices.
When P2 wins ties, bidding 0 must also be considered once every neighboring threshold is known, since its cost depends on the worst neighbor.
The time complexity of the solver is `O(|E| B log(B))` where `B` is `max_p2_budget`.

### `compute_values`

Computes the game value for every `(node, p1_budget, p2_budget)` state, up to `max_p1_budget` and `max_p2_budget`.
States already past their winning/losing threshold are set directly.
The remaining states are solved as a zero-sum matrix game with Linear Programming.
The computation repeats until it reaches a fixed point - a state's value can depend on other unresolved states.

### `get_strategy`

Computes the optimal mixed strategy for a state and player using `values`.

## Richman

Richman payments go to the opponent, so the total `p1_budget + p2_budget` is conserved.
The solver only needs to track `p1_budget` and derives `p2_budget = total_budget - p1_budget`.

### `compute_thresholds`

Given the total budget, computes the threshold for each node.
Computes each node's threshold by choosing either to actively win the bid, or to bid nothing and let P2 decide the outcome.
The computation repeats until it reaches a fixed point - a node's threshold can depend on other unresolved thresholds.

### `compute_threshold`

Computes the threshold for a single `(node, p2_budget)` pair, without a given total budget.
Starts with a small `total_budget` and keeps doubling it until P1 can assure a win.
Then uses binary search to find the threshold.

### `compute_values`

Given the `total_budget`, computes the game value of each state with that budget.
Same structure as in poorman.

### `get_strategy`

Computes the optimal mixed strategy for a state and player using `values`.

## Linear Programming

Solves the payoff matrix as a zero-sum matrix game via [HiGHS](https://github.com/ERGO-Code/HiGHS).

## Python Bindings

nanobind module `allpay`.
Python names mirror the C++ ones directly: `compute_<variant>_<name>`/`get_<variant>_<name>` calls `<variant>::<name>` (e.g. `compute_poorman_thresholds` calls `poorman::compute_thresholds`).
`Player`, `Game`, and `RootedGame` keep their C++ names unchanged.
`Game` exposes its fields as read-only and a `flipped()` method.

## Game Generators

Each generator builds an `adj_list` and returns a `Game`.
To add a new game, write a function that returns `Game(adj_list, p1_target, p2_target, tiebreaker)`.

## Build

`build.sh` builds just the core C++ solver inside the `build/` folder.
