#include <iostream>

#include "games.hpp"
#include "solver.hpp"

int main()
{
    Game game = games::make_tow(2);

    Coins threshold = solver::poorman_reachability(game, 1, 10);

    std::cout << threshold << std::endl;

    return 0;
}
