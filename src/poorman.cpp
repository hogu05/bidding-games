#include "poorman.hpp"

#include <algorithm>
#include <queue>
#include <utility>
#include <vector>

#include "lp.hpp"

namespace poorman
{

static std::pair<Coins, bool> try_bid(const Game& game, Node node, Coins p2_budget, Coins p1_bid,
                                      Coins win_threshold,
                                      const std::vector<std::vector<Coins>>& thresholds)
{
    Coins p2_win_bid = game.tiebreaker == Player::P1 ? p1_bid + 1 : p1_bid;
    Coins win_bid_threshold = (win_threshold == INF_COINS) ? INF_COINS : p1_bid + win_threshold;

    if (p2_win_bid > p2_budget)
    {
        return {win_bid_threshold, true};
    }

    Coins lose_threshold = 0;
    for (Node neighbor : game.adj_list[node])
    {
        lose_threshold = std::max(lose_threshold, thresholds[neighbor][p2_budget - p2_win_bid]);
    }
    Coins lose_bid_threshold = (lose_threshold == INF_COINS) ? INF_COINS : p1_bid + lose_threshold;

    bool p1_wins = (p2_win_bid != 0) && (win_bid_threshold >= lose_bid_threshold);
    return {p1_wins ? win_bid_threshold : lose_bid_threshold, p1_wins};
}

static Coins get_threshold(const Game& game, Node node, Coins p2_budget, Coins win_threshold,
                           const std::vector<std::vector<Coins>>& thresholds)
{
    Coins low = game.tiebreaker == Player::P1 ? 0 : 1;
    Coins high = game.tiebreaker == Player::P1 ? p2_budget : p2_budget + 1;
    Coins threshold = INF_COINS;

    while (low <= high)
    {
        Coins mid = low + ((high - low) / 2);
        auto [current_threshold, p1_wins] =
            try_bid(game, node, p2_budget, mid, win_threshold, thresholds);
        threshold = std::min(threshold, current_threshold);
        if (p1_wins)
        {
            high = mid - 1;
        }
        else
        {
            low = mid + 1;
        }
    }
    return threshold;
}

static void compute_budget_thresholds(const Game& game, Coins p2_budget,
                                      const std::vector<std::vector<Node>>& adj_list_transpose,
                                      std::vector<std::vector<Coins>>& thresholds)
{
    int num_nodes = static_cast<int>(game.adj_list.size());
    Node p1_target = game.p1_target;
    Node p2_target = game.p2_target;

    std::vector<bool> done(num_nodes);
    done[p2_target] = true;
    std::vector<int> not_done_neighbors(num_nodes);
    for (Node node = 0; node < num_nodes; ++node)
    {
        not_done_neighbors[node] = static_cast<int>(game.adj_list[node].size());
    }

    std::vector<Coins> win_threshold(num_nodes, INF_COINS);

    std::priority_queue<std::pair<Coins, Node>, std::vector<std::pair<Coins, Node>>, std::greater<>>
        queue;

    queue.emplace(0, p1_target);

    while (!queue.empty())
    {
        auto [threshold, node] = queue.top();
        queue.pop();
        if (done[node])
        {
            continue;
        }
        done[node] = true;
        thresholds[node][p2_budget] = threshold;

        for (Node in_neighbor : adj_list_transpose[node])
        {
            if (done[in_neighbor])
            {
                continue;
            }
            if (win_threshold[in_neighbor] == INF_COINS)
            {
                win_threshold[in_neighbor] = threshold;
                Coins in_neighbor_threshold =
                    get_threshold(game, in_neighbor, p2_budget, win_threshold[in_neighbor], thresholds);
                if (in_neighbor_threshold < INF_COINS)
                {
                    queue.emplace(in_neighbor_threshold, in_neighbor);
                }
            }
            if (game.tiebreaker == Player::P2 && --not_done_neighbors[in_neighbor] == 0)
            {
                queue.emplace(threshold, in_neighbor);
            }
        }
    }
}

static std::vector<std::vector<Node>> transpose(const Game& game)
{
    int num_nodes = static_cast<int>(game.adj_list.size());
    std::vector<std::vector<Node>> adj_list_transpose(num_nodes);
    for (Node node_1 = 0; node_1 < num_nodes; ++node_1)
    {
        for (Node node_2 : game.adj_list[node_1])
        {
            adj_list_transpose[node_2].push_back(node_1);
        }
    }
    return adj_list_transpose;
}

std::vector<std::vector<Coins>> compute_thresholds(const Game& game, Coins max_p2_budget)
{
    int num_nodes = static_cast<int>(game.adj_list.size());
    Node p1_target = game.p1_target;
    Node p2_target = game.p2_target;

    std::vector<std::vector<Coins>> thresholds(num_nodes,
                                               std::vector<Coins>(max_p2_budget + 1, INF_COINS));
    for (Coins p2_budget = 0; p2_budget <= max_p2_budget; ++p2_budget)
    {
        thresholds[p1_target][p2_budget] = 0;
        thresholds[p2_target][p2_budget] = INF_COINS;
    }

    auto adj_list_transpose = transpose(game);
    for (Coins p2_budget = 0; p2_budget <= max_p2_budget; ++p2_budget)
    {
        compute_budget_thresholds(game, p2_budget, adj_list_transpose, thresholds);
    }

    return thresholds;
}

static std::vector<std::vector<double>>
build_payoff_matrix(const Game& game, Node node, Coins p1_budget, Coins p2_budget,
                    const std::vector<std::vector<std::vector<double>>>& values)
{
    std::vector<std::vector<double>> payoff_matrix(p1_budget + 1,
                                                   std::vector<double>(p2_budget + 1, 0.0));
    for (Coins p1_bid = 0; p1_bid <= p1_budget; ++p1_bid)
    {
        for (Coins p2_bid = 0; p2_bid <= p2_budget; ++p2_bid)
        {
            Coins new_p1_budget = p1_budget - p1_bid;
            Coins new_p2_budget = p2_budget - p2_bid;

            bool p1_wins = (p1_bid > p2_bid) || (p1_bid == p2_bid && game.tiebreaker == Player::P1);

            if (p1_wins)
            {
                double win_value = 0.0;
                for (Node neighbor : game.adj_list[node])
                {
                    win_value = std::max(win_value, values[neighbor][new_p1_budget][new_p2_budget]);
                }
                payoff_matrix[p1_bid][p2_bid] = win_value;
            }
            else
            {
                double lose_value = 1.0;
                for (Node neighbor : game.adj_list[node])
                {
                    lose_value =
                        std::min(lose_value, values[neighbor][new_p1_budget][new_p2_budget]);
                }
                payoff_matrix[p1_bid][p2_bid] = lose_value;
            }
        }
    }
    return payoff_matrix;
}

std::vector<std::vector<std::vector<double>>> compute_values(const Game& game, Coins max_p1_budget,
                                                             Coins max_p2_budget)
{
    int num_nodes = static_cast<int>(game.adj_list.size());
    Node p1_target = game.p1_target;
    Node p2_target = game.p2_target;

    std::vector<std::vector<std::vector<double>>> values(
        num_nodes, std::vector<std::vector<double>>(max_p1_budget + 1,
                                                    std::vector<double>(max_p2_budget + 1, 0.0)));

    for (Coins p1_budget = 0; p1_budget <= max_p1_budget; ++p1_budget)
    {
        for (Coins p2_budget = 0; p2_budget <= max_p2_budget; ++p2_budget)
        {
            values[p1_target][p1_budget][p2_budget] = 1.0;
            values[p2_target][p1_budget][p2_budget] = 0.0;
        }
    }

    auto win_thresholds = compute_thresholds(game, max_p2_budget);
    auto lose_thresholds = compute_thresholds(game.flipped(), max_p1_budget);

    for (Node node = 0; node < num_nodes; ++node)
    {
        if (node == p1_target || node == p2_target)
        {
            continue;
        }
        for (Coins p1_budget = 0; p1_budget <= max_p1_budget; ++p1_budget)
        {
            for (Coins p2_budget = 0; p2_budget <= max_p2_budget; ++p2_budget)
            {
                if (p1_budget >= win_thresholds[node][p2_budget])
                {
                    values[node][p1_budget][p2_budget] = 1.0;
                }
                else if (p2_budget >= lose_thresholds[node][p1_budget])
                {
                    values[node][p1_budget][p2_budget] = 0.0;
                }
            }
        }
    }

    const double EPSILON = 1e-6;

    for (Coins p1_budget = 0; p1_budget <= max_p1_budget; ++p1_budget)
    {
        for (Coins p2_budget = 0; p2_budget <= max_p2_budget; ++p2_budget)
        {
            while (true)
            {
                double max_diff = 0.0;

                for (Node node = 0; node < num_nodes; ++node)
                {
                    if (node == p1_target || node == p2_target)
                    {
                        continue;
                    }

                    if (p1_budget >= win_thresholds[node][p2_budget] ||
                        p2_budget >= lose_thresholds[node][p1_budget])
                    {
                        continue;
                    }

                    double new_value = lp::compute_matrix_value(
                        build_payoff_matrix(game, node, p1_budget, p2_budget, values));
                    max_diff = std::max(max_diff,
                                        std::abs(new_value - values[node][p1_budget][p2_budget]));
                    values[node][p1_budget][p2_budget] = new_value;
                }

                if (max_diff < EPSILON)
                {
                    break;
                }
            }
        }
    }
    return values;
}

std::vector<double> get_strategy(const Game& game, Node node, Coins p1_budget, Coins p2_budget,
                                 const std::vector<std::vector<std::vector<double>>>& values,
                                 Player player)
{
    return lp::get_strategy(build_payoff_matrix(game, node, p1_budget, p2_budget, values), player);
}

} // namespace poorman
