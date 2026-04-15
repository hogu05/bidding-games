#include <iostream>

#include "games.hpp"
#include "solver.hpp"
int main()
{

    Game game = games::make_tow(2, true);
    Coins b2 = 10;
    Node start_node = 2;

    std::vector<Coins> p1_threshold = solver::poorman_reachability(game, start_node, b2);
    std::vector<Coins> p2_threshold = solver::poorman_reachability(game.flipped(), start_node, b2);

    Coins p1_win_threshold = p1_threshold[b2];

    auto it = std::ranges::upper_bound(p2_threshold, b2);

    Coins p1_lose_threshold = std::distance(p2_threshold.begin(), std::prev(it));

    std::cout << "P2 Budget: " << b2 << std::endl;
    std::cout << "P1 Winning Threshold: " << p1_win_threshold << std::endl;
    std::cout << "P1 Losing Threshold: " << p1_lose_threshold << std::endl;

    return 0;
}
