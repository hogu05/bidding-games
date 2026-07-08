#pragma once
#include "game.hpp"
#include "types.hpp"

namespace richman
{
std::vector<Coins> compute_thresholds(const Game& game, Coins total_budget);
std::vector<std::vector<double>> compute_values(const Game& game, Coins total_budget);
std::vector<double> get_strategy(const Game& game, Node node, Coins p1_budget,
                                 const std::vector<std::vector<double>>& values, Player player);
} // namespace richman
