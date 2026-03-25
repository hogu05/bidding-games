#include "game.hpp"

Game::Game(int num_nodes, Node p1_target, Node p2_target)
    : num_nodes(num_nodes), p1_target(p1_target), p2_target(p2_target)
{
    adj_list.resize(num_nodes);
}

void Game::add_edge(Node from, Node to)
{
    adj_list[from].push_back(to);
}

int Game::get_num_nodes() const
{
    return num_nodes;
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
