#include "richman.hpp"

#include <algorithm>
#include <vector>

#include "lp.hpp"

namespace richman
{

std::vector<Coins> compute_thresholds(const Game& game, Coins total_budget)
{
    int num_nodes = static_cast<int>(game.adj_list.size());
    Node p1_target = game.p1_target;
    Node p2_target = game.p2_target;

    std::vector<Coins> thresholds(num_nodes, INF_COINS);
    thresholds[p1_target] = 0;

    bool changed = true;
    while (changed)
    {
        changed = false;
        for (Node node = 0; node < num_nodes; ++node)
        {
            if (node == p1_target || node == p2_target)
            {
                continue;
            }

            Coins best_neighbor = INF_COINS;
            Coins worst_neighbor = 0;
            for (Node neighbor : game.adj_list[node])
            {
                best_neighbor = std::min(best_neighbor, thresholds[neighbor]);
                worst_neighbor = std::max(worst_neighbor, thresholds[neighbor]);
            }

            Coins threshold = 0;
            if (best_neighbor == INF_COINS)
            {
                threshold = INF_COINS;
            }
            else
            {
                Coins passive = (game.tiebreaker == Player::P1)
                                    ? std::max(best_neighbor, worst_neighbor - 1)
                                    : std::max(best_neighbor, worst_neighbor);
                Coins active = (game.tiebreaker == Player::P1)
                                   ? (total_budget + best_neighbor + 1) / 2
                                   : (total_budget + best_neighbor + 2) / 2;
                threshold = std::min(passive, active);
            }

            if (threshold < thresholds[node])
            {
                thresholds[node] = threshold;
                changed = true;
            }
        }
    }

    return thresholds;
}

Coins compute_threshold(const Game& game, Node node, Coins p2_budget)
{
    if (node == game.p1_target)
    {
        return 0;
    }
    if (node == game.p2_target)
    {
        return INF_COINS;
    }

    Coins low = 0;
    Coins high = 1;
    while (high < compute_thresholds(game, high + p2_budget)[node])
    {
        high *= 2;
    }

    Coins threshold = INF_COINS;
    while (low <= high)
    {
        Coins mid = low + ((high - low) / 2);
        bool p1_wins = mid >= compute_thresholds(game, mid + p2_budget)[node];

        if (p1_wins)
        {
            threshold = std::min(threshold, mid);
            high = mid - 1;
        }
        else
        {
            low = mid + 1;
        }
    }

    return threshold;
}

static std::vector<std::vector<double>>
build_payoff_matrix(const Game& game, Node node, Coins p1_budget,
                    const std::vector<std::vector<double>>& values)
{
    Coins total = static_cast<Coins>(values[0].size()) - 1;
    Coins p2_budget = total - p1_budget;

    std::vector<std::vector<double>> payoff_matrix(p1_budget + 1,
                                                   std::vector<double>(p2_budget + 1, 0.0));
    for (Coins p1_bid = 0; p1_bid <= p1_budget; ++p1_bid)
    {
        for (Coins p2_bid = 0; p2_bid <= p2_budget; ++p2_bid)
        {
            bool p1_wins = (p1_bid > p2_bid) || (p1_bid == p2_bid && game.tiebreaker == Player::P1);
            Coins new_p1_budget = p1_budget - p1_bid + p2_bid;

            if (p1_wins)
            {
                double p1_win_value = 0.0;
                for (Node neighbor : game.adj_list[node])
                {
                    p1_win_value = std::max(p1_win_value, values[neighbor][new_p1_budget]);
                }
                payoff_matrix[p1_bid][p2_bid] = p1_win_value;
            }
            else
            {
                double p2_win_value = 1.0;
                for (Node neighbor : game.adj_list[node])
                {
                    p2_win_value = std::min(p2_win_value, values[neighbor][new_p1_budget]);
                }
                payoff_matrix[p1_bid][p2_bid] = p2_win_value;
            }
        }
    }
    return payoff_matrix;
}

std::vector<std::vector<double>> compute_values(const Game& game, Coins total_budget)
{
    int num_nodes = static_cast<int>(game.adj_list.size());
    Node p1_target = game.p1_target;
    Node p2_target = game.p2_target;

    constexpr double INITIAL_VALUE = 0.5;
    std::vector<std::vector<double>> values(num_nodes,
                                            std::vector<double>(total_budget + 1, INITIAL_VALUE));
    for (Coins p1_budget = 0; p1_budget <= total_budget; ++p1_budget)
    {
        values[p1_target][p1_budget] = 1.0;
        values[p2_target][p1_budget] = 0.0;
    }

    auto winning_thresholds = compute_thresholds(game, total_budget);
    auto losing_thresholds = compute_thresholds(game.flipped(), total_budget);

    for (Node node = 0; node < num_nodes; ++node)
    {
        if (node == p1_target || node == p2_target)
        {
            continue;
        }
        for (Coins p1_budget = 0; p1_budget <= total_budget; ++p1_budget)
        {
            if (p1_budget >= winning_thresholds[node])
            {
                values[node][p1_budget] = 1.0;
            }
            else if (total_budget - p1_budget >= losing_thresholds[node])
            {
                values[node][p1_budget] = 0.0;
            }
        }
    }

    const double EPSILON = 1e-6;

    while (true)
    {
        double max_diff = 0.0;

        for (Node node = 0; node < num_nodes; ++node)
        {
            if (node == p1_target || node == p2_target)
            {
                continue;
            }

            for (Coins p1_budget = 0; p1_budget <= total_budget; ++p1_budget)
            {
                if (p1_budget >= winning_thresholds[node] ||
                    total_budget - p1_budget >= losing_thresholds[node])
                {
                    continue;
                }
                double new_value =
                    lp::compute_matrix_value(build_payoff_matrix(game, node, p1_budget, values));
                max_diff = std::max(max_diff, std::abs(new_value - values[node][p1_budget]));
                values[node][p1_budget] = new_value;
            }
        }

        if (max_diff < EPSILON)
        {
            break;
        }
    }

    return values;
}

std::vector<double> get_strategy(const Game& game, Node node, Coins p1_budget,
                                 const std::vector<std::vector<double>>& values, Player player)
{
    return lp::get_strategy(build_payoff_matrix(game, node, p1_budget, values), player);
}

} // namespace richman
