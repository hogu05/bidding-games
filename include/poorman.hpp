#pragma once
#include "game.hpp"
#include "types.hpp"

namespace poorman
{
std::vector<std::vector<Coins>> compute_thresholds(const Game& game, Coins max_p2_budget);
std::vector<std::vector<std::vector<double>>> compute_values(const Game& game, Coins max_p1_budget,
                                                             Coins max_p2_budget);
std::vector<double> get_strategy(const Game& game, Node node, Coins p1_budget, Coins p2_budget,
                                 const std::vector<std::vector<std::vector<double>>>& values);
} // namespace poorman
