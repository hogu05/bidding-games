#pragma once
#include "game.hpp"

namespace games
{

Game make_race(int a, int b, bool p1_wins_ties = true);
Game make_tow(int n, bool p1_wins_ties = true);
Game make_coins(const std::vector<int>& coins, bool p1_wins_ties = true);
Game make_game_sum(const std::vector<RootedGame>& rooted_games, bool p1_wins_ties = true);

} // namespace games
