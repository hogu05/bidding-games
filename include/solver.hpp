#pragma once
#include "game.hpp"
#include "types.hpp"

namespace solver
{
std::vector<std::vector<Coins>> poorman_reachability(const Game& game, Coins max_p2_budget);
} // namespace solver
