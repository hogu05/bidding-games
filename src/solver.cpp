#include "solver.hpp"

#include <algorithm>
#include <vector>

namespace solver
{

const Coins INF = 1e9;

static Coins compute_node_threshold(Node node, Coins p2_budget, const Game& game,
                                    const std::vector<std::vector<Coins>>& threshold)
{
    const std::vector<Node>& neighbors = game.get_neighbors(node);
    Coins min_threshold = INF;

    std::vector<Coins> p1_win_threshold(p2_budget + 1, INF);
    std::vector<Coins> p2_win_threshold(p2_budget + 1, 0);
    for (Coins p2_bid = 0; p2_bid <= p2_budget; ++p2_bid)
    {
        for (Node neighbor : neighbors)
        {
            Coins neighbor_threshold = threshold[neighbor][p2_budget - p2_bid];
            p1_win_threshold[p2_bid] = std::min(p1_win_threshold[p2_bid], neighbor_threshold);
            p2_win_threshold[p2_bid] = std::max(p2_win_threshold[p2_bid], neighbor_threshold);
        }
    }

    for (Coins p1_bid = 0; p1_bid <= p2_budget; ++p1_bid)
    {
        Coins max_threshold = 0;

        for (Coins p2_bid = 0; p2_bid <= p2_budget; ++p2_bid)
        {
            Coins next_threshold =
                (p1_bid >= p2_bid) ? p1_win_threshold[p2_bid] : p2_win_threshold[p2_bid];
            Coins total_threshold = (next_threshold == INF) ? INF : p1_bid + next_threshold;
            max_threshold = std::max(max_threshold, total_threshold);
        }
        min_threshold = std::min(min_threshold, max_threshold);
    }

    return min_threshold;
}

Coins poorman_reachability(const Game& game, Node start_node, Coins start_p2_budget)
{
    int num_nodes = game.get_num_nodes();
    Node p1_target = game.get_p1_target();
    Node p2_target = game.get_p2_target();

    std::vector<std::vector<Coins>> threshold(num_nodes,
                                              std::vector<Coins>(start_p2_budget + 1, INF));

    for (Coins p2_budget = 0; p2_budget <= start_p2_budget; ++p2_budget)
    {
        for (int step = 0; step < num_nodes; ++step)
        {
            for (Node node = 0; node < num_nodes; ++node)
            {

                if (node == p1_target)
                {
                    threshold[node][p2_budget] = 0;
                    continue;
                }
                if (node == p2_target)
                {
                    threshold[node][p2_budget] = INF;
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
