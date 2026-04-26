#pragma once
#include <vector>

#include "types.hpp"

struct Game
{
    std::vector<std::vector<Node>> adj_list;
    Node p1_target{};
    Node p2_target{};
    bool p1_wins_ties{};

    Game flipped() const
    {
        return {.adj_list = adj_list,
                .p1_target = p2_target,
                .p2_target = p1_target,
                .p1_wins_ties = !p1_wins_ties};
    }
};
