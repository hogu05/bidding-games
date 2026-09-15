import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
import numpy as np
import seaborn as sns
from allpay import (
    Player,
    compute_poorman_thresholds,
    compute_poorman_values,
    get_poorman_strategy,
)

FIGSIZE = (10, 5)
MARKER = "o"
MARKERSIZE = 3
COLORMAP = cm.plasma


def show(xlabel, ylabel):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()


def plot_strategy_remaining(rooted_game, max_budget, player=Player.P1):
    values = compute_poorman_values(rooted_game.game, max_budget, max_budget)
    colors = COLORMAP(np.linspace(0, 1, max_budget))
    plt.figure(figsize=FIGSIZE)

    for b, color in zip(range(1, max_budget + 1), colors):
        strategy = get_poorman_strategy(
            rooted_game.game, rooted_game.start_node, b, b, values, player
        )
        remaining = [b - i for i, p in enumerate(strategy) if p > 0]
        probabilities = [p for p in strategy if p > 0]
        plt.plot(
            remaining,
            probabilities,
            marker=MARKER,
            markersize=MARKERSIZE,
            linestyle="none",
            color=color,
        )

    sm = cm.ScalarMappable(cmap=COLORMAP, norm=plt.Normalize(1, max_budget))
    plt.colorbar(sm, ax=plt.gca(), label="Budget")
    show("R (budget - bid)", "Bid probability")


def plot_game_values(rooted_games, max_budget):
    colors = COLORMAP(np.linspace(0, 1, len(rooted_games)))

    plt.figure(figsize=FIGSIZE)
    for (rooted_game, label), color in zip(rooted_games, colors):
        values = compute_poorman_values(rooted_game.game, max_budget, max_budget)
        data = [values[rooted_game.start_node][b][b] for b in range(max_budget + 1)]
        plt.plot(
            range(max_budget + 1),
            data,
            marker=MARKER,
            markersize=MARKERSIZE,
            linestyle="none",
            color=color,
            label=label,
        )

    plt.legend()
    show("Budget", "Game value")


def plot_values_heatmap(rooted_game, max_budget):
    values = compute_poorman_values(rooted_game.game, max_budget, max_budget)
    node = rooted_game.start_node
    data = np.array(values[node]).T
    plt.figure(figsize=FIGSIZE)
    sns.heatmap(data, vmin=0, vmax=1, cmap="coolwarm", cbar_kws={"label": "Game value"})
    plt.gca().invert_yaxis()
    show("P1 Budget", "P2 Budget")


def plot_thresholds(rooted_games, max_budget):
    colors = COLORMAP(np.linspace(0, 1, len(rooted_games)))

    plt.figure(figsize=FIGSIZE)
    for (rooted_game, label), color in zip(rooted_games, colors):
        winning_threshold = compute_poorman_thresholds(rooted_game.game, max_budget)
        winning_budgets = winning_threshold[rooted_game.start_node]
        plt.plot(
            range(len(winning_budgets)),
            winning_budgets,
            marker=MARKER,
            markersize=MARKERSIZE,
            linestyle="none",
            color=color,
            label=label,
        )

    plt.legend()
    show("P2 Budget", "Threshold")


def draw_game(game):
    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(game.adj_list)))
    for node, neighbors in enumerate(game.adj_list):
        for neighbor in neighbors:
            graph.add_edge(node, neighbor)

    colors = [
        (
            "limegreen"
            if node == game.p1_target
            else "tomato" if node == game.p2_target else "lightgray"
        )
        for node in graph.nodes
    ]

    plt.figure(figsize=(4, 2))
    nx.draw(
        graph,
        {node: (node, 0) for node in range(len(game.adj_list))},
        with_labels=True,
        node_color=colors,
        node_size=300,
        arrowsize=10,
        font_size=8,
        font_weight="bold",
    )
    plt.show()
