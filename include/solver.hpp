#pragma once
#include "game.hpp"
#include "types.hpp"

namespace solver
{
std::vector<Coins> poorman_reachability(const Game& game, Node start_node, Coins start_p2_budget);
} // namespace solver
