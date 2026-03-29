#include "solver.hpp"

#include <algorithm>
#include <vector>

namespace solver
{

static Coins compute_node_threshold(Node node, Coins p2_budget, const Game& game,
                                    const std::vector<std::vector<Coins>>& threshold)
{
    const std::vector<Node>& neighbors = game.get_neighbors(node);
    Coins min_threshold = INF_COINS;

    std::vector<Coins> p1_win_threshold(p2_budget + 1, 0);
    Coins p1_win_threshold_max = 0;

    for (Coins p2_bid = 0; p2_bid <= p2_budget; ++p2_bid)
    {
        Coins p2_bid_threshold = INF_COINS;
        for (Node neighbor : neighbors)
        {
            p2_bid_threshold = std::min(p2_bid_threshold, threshold[neighbor][p2_budget - p2_bid]);
        }

        p1_win_threshold_max = std::max(p1_win_threshold_max, p2_bid_threshold);

        p1_win_threshold[p2_bid] = p1_win_threshold_max;
    }

    std::vector<Coins> p2_win_threshold(p2_budget + 2, 0);
    Coins p2_win_threshold_max = 0;

    for (int p2_bid = p2_budget; p2_bid >= 0; --p2_bid)
    {
        Coins p2_bid_threshold = 0;
        for (Node neighbor : neighbors)
        {
            p2_bid_threshold = std::max(p2_bid_threshold, threshold[neighbor][p2_budget - p2_bid]);
        }

        p2_win_threshold_max = std::max(p2_win_threshold_max, p2_bid_threshold);

        p2_win_threshold[p2_bid] = p2_win_threshold_max;
    }

    for (Coins p1_bid = 0; p1_bid <= p2_budget; ++p1_bid)
    {
        Coins max_threshold = std::max(p1_win_threshold[p1_bid], p2_win_threshold[p1_bid + 1]);

        Coins total_threshold = (max_threshold == INF_COINS) ? INF_COINS : p1_bid + max_threshold;
        min_threshold = std::min(min_threshold, total_threshold);
    }

    return min_threshold;
}

Coins poorman_reachability(const Game& game, Node start_node, Coins start_p2_budget)
{
    int num_nodes = game.get_num_nodes();
    Node p1_target = game.get_p1_target();
    Node p2_target = game.get_p2_target();

    std::vector<std::vector<Coins>> threshold(num_nodes,
                                              std::vector<Coins>(start_p2_budget + 1, INF_COINS));
    for (Coins p2_budget = 0; p2_budget <= start_p2_budget; ++p2_budget)
    {
        threshold[p1_target][p2_budget] = 0;
        threshold[p2_target][p2_budget] = INF_COINS;
        for (int step = 0; step < num_nodes; ++step)
        {
            for (Node node = 0; node < num_nodes; ++node)
            {
                if (node == p1_target || node == p2_target)
                {
                    continue;
                }

                Coins new_threshold = compute_node_threshold(node, p2_budget, game, threshold);

                threshold[node][p2_budget] = std::min(threshold[node][p2_budget], new_threshold);
            }
        }
    }
    return threshold[start_node][start_p2_budget];
}
} // end namespace solver
