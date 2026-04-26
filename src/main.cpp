#include <iostream>

#include "games.hpp"
#include "solver.hpp"
int main()
{

    Game game_1 = games::make_race(2, 1, true);
    Game game_2 = games::make_race(1, 1, true);
    Game game = games::make_game_sum(
        {{.game = game_1, .start_node = 0}, {.game = game_2, .start_node = 0}}, true);
    Coins max_p2_budget = 10;
    Node start_node = 0;

    std::vector<Coins> p1_threshold = solver::poorman_reachability(game, max_p2_budget)[start_node];
    std::vector<Coins> p2_threshold =
        solver::poorman_reachability(game.flipped(), max_p2_budget)[start_node];

    Coins p1_win_threshold = p1_threshold[max_p2_budget];

    auto it = std::ranges::upper_bound(p2_threshold, max_p2_budget);

    Coins p1_lose_threshold = std::distance(p2_threshold.begin(), std::prev(it));

    std::cout << "P2 Budget: " << max_p2_budget << std::endl;
    std::cout << "P1 Winning Threshold: " << p1_win_threshold << std::endl;
    std::cout << "P1 Losing Threshold: " << p1_lose_threshold << std::endl;

    return 0;
}
