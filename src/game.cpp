#include "game.hpp"

Game::Game(std::vector<std::vector<Node>> adj_list, Node p1_target, Node p2_target,
           bool p1_wins_ties)
    : adj_list(std::move(adj_list)), p1_target(p1_target), p2_target(p2_target),
      p1_wins_ties(p1_wins_ties)
{
}

Game Game::flipped() const
{
    return {adj_list, p2_target, p1_target, !p1_wins_ties};
}

const std::vector<std::vector<Node>>& Game::get_adj_list() const
{
    return adj_list;
}

int Game::get_num_nodes() const
{
    return static_cast<int>(adj_list.size());
}

Node Game::get_p1_target() const
{
    return p1_target;
}

Node Game::get_p2_target() const
{
    return p2_target;
}

const std::vector<Node>& Game::get_neighbors(Node node) const
{
    return adj_list[node];
}

bool Game::get_p1_wins_ties() const
{
    return p1_wins_ties;
}
