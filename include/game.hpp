#pragma once
#include <vector>

#include "types.hpp"

struct Game
{
    std::vector<std::vector<Node>> adj_list;
    Node p1_target{};
    Node p2_target{};
    Player tiebreaker{};

    Game flipped() const
    {
        return {.adj_list = adj_list,
                .p1_target = p2_target,
                .p2_target = p1_target,
                .tiebreaker = (tiebreaker == Player::P1 ? Player::P2 : Player::P1)};
    }
};

struct RootedGame
{
    Game game;
    Node start_node{};
};
