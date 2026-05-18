#include "poorman.hpp"

#include <Highs.h>
#include <algorithm>
#include <vector>

namespace poorman
{
static Coins compute_configuration_threshold(const Game& game, Node node, Coins p2_budget,
                                             const std::vector<std::vector<Coins>>& thresholds)
{
    Coins max_p1_bid = game.p1_wins_ties ? p2_budget : p2_budget + 1;

    Coins p1_win_branch_threshold = INF_COINS;
    for (Node neighbor : game.adj_list[node])
    {
        p1_win_branch_threshold =
            std::min(p1_win_branch_threshold, thresholds[neighbor][p2_budget]);
    }

    auto calculate_bid_threshold = [&](Coins p1_bid) -> std::pair<Coins, bool>
    {
        Coins p2_win_bid = game.p1_wins_ties ? p1_bid + 1 : p1_bid;
        Coins p1_win_threshold =
            (p1_win_branch_threshold == INF_COINS) ? INF_COINS : p1_bid + p1_win_branch_threshold;

        if (p2_win_bid > p2_budget)
        {

            return {p1_win_threshold, true};
        }

        Coins p2_win_branch_threshold = 0;
        for (Node neighbor : game.adj_list[node])
        {
            p2_win_branch_threshold =
                std::max(p2_win_branch_threshold, thresholds[neighbor][p2_budget - p2_win_bid]);
        }
        Coins p2_win_threshold = (p2_win_branch_threshold == INF_COINS)
                                     ? INF_COINS
                                     : p1_bid + p2_win_branch_threshold; // Make function for this

        bool p1_wins = (p2_win_bid != 0) && (p1_win_threshold >= p2_win_threshold);
        return {p1_wins ? p1_win_threshold : p2_win_threshold, p1_wins};
    };
    Coins low = 0;
    Coins high = max_p1_bid;
    Coins threshold = INF_COINS;

    while (low <= high)
    {
        Coins mid = low + ((high - low) / 2);

        auto [current_bid_threshold, p1_wins] = calculate_bid_threshold(mid);

        threshold = std::min(threshold, current_bid_threshold);

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

                Coins new_threshold =
                    compute_configuration_threshold(game, node, p2_budget, thresholds);

                if (new_threshold < thresholds[node][p2_budget])
                {
                    thresholds[node][p2_budget] = new_threshold;
                    changed = true;
                }
            }
        }
    }
    return thresholds;
}

static double compute_matrix_value(const std::vector<std::vector<double>>& payoff_matrix)
{
    auto max_p1_bid = static_cast<Coins>(payoff_matrix.size());
    auto max_p2_bid = static_cast<Coins>(payoff_matrix[0].size());

    Highs highs;
    highs.setOptionValue("output_flag", false);

    highs.changeObjectiveSense(ObjSense::kMaximize);

    for (Coins _ = 0; _ < max_p1_bid; ++_)
    {
        highs.addVar(0.0, 1.0);
    }

    highs.addVar(0.0, 1.0);
    int value_index = max_p1_bid;

    highs.changeColCost(value_index, 1.0);

    std::vector<int> sum_indices(max_p1_bid);
    std::iota(sum_indices.begin(), sum_indices.end(), 0);
    std::vector<double> sum_values(max_p1_bid, 1.0);
    highs.addRow(1.0, 1.0, max_p1_bid, sum_indices.data(), sum_values.data());

    for (Coins p2_bid = 0; p2_bid < max_p2_bid; ++p2_bid)
    {
        std::vector<int> value_indices;
        std::vector<double> value_values;

        for (Coins p1_bid = 0; p1_bid < max_p1_bid; ++p1_bid)
        {
            value_indices.push_back(p1_bid);
            value_values.push_back(payoff_matrix[p1_bid][p2_bid]);
        }

        value_indices.push_back(value_index);
        value_values.push_back(-1.0);

        highs.addRow(0.0, kHighsInf, max_p1_bid + 1, value_indices.data(), value_values.data());
    }

    highs.run();
    const HighsSolution& solution = highs.getSolution();
    return solution.col_value[value_index] + 0.0;
}

static double
compute_configuration_value(const Game& game, Node node, Coins p1_budget, Coins p2_budget,
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

            if (p1_bid >= p2_bid)
            {
                double p1_win_value = 0.0;
                for (Node neighbor : game.adj_list[node])
                {
                    p1_win_value =
                        std::max(p1_win_value, values[neighbor][new_p1_budget][new_p2_budget]);
                }
                payoff_matrix[p1_bid][p2_bid] = p1_win_value;
            }
            else
            {
                double p2_win_value = 1.0;
                for (Node neighbor : game.adj_list[node])
                {
                    p2_win_value =
                        std::min(p2_win_value, values[neighbor][new_p1_budget][new_p2_budget]);
                }
                payoff_matrix[p1_bid][p2_bid] = p2_win_value;
            }
        }
    }

    return compute_matrix_value(payoff_matrix);
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

    auto winning_thresholds = compute_thresholds(game, max_p2_budget);
    auto losing_thresholds = compute_thresholds(game.flipped(), max_p1_budget);

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
                if (p1_budget >= winning_thresholds[node][p2_budget])
                {
                    values[node][p1_budget][p2_budget] = 1.0;
                }
                else if (p2_budget >= losing_thresholds[node][p1_budget])
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

                    if (p1_budget >= winning_thresholds[node][p2_budget] ||
                        p2_budget >= losing_thresholds[node][p1_budget])
                    {
                        continue;
                    }

                    double new_value =
                        compute_configuration_value(game, node, p1_budget, p2_budget, values);
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

} // namespace poorman
