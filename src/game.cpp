#include "game.hpp"

Game::Game(std::vector<std::vector<Node>> edges, Node p1_target, Node p2_target, bool p1_wins_ties)
    : adj_list(std::move(edges)), p1_target(p1_target), p2_target(p2_target),
      p1_wins_ties(p1_wins_ties)
{
}

Game Game::flipped() const
{
    Game flipped_game = *this;
    std::swap(flipped_game.p1_target, flipped_game.p2_target);
    flipped_game.p1_wins_ties = !this->p1_wins_ties;
    return flipped_game;
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
