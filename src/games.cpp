#include "games.hpp"

namespace games
{

Game make_wnr(int n)
{
    int num_nodes = n + 2;
    Node p1_target = num_nodes - 1;
    Node p2_target = 0;

    Game game(num_nodes, p1_target, p2_target);

    for (int i = 1; i <= n; ++i)
    {
        game.add_edge(i, i + 1);
        game.add_edge(i, p2_target);
    }

    return game;
}

Game make_tow(int n)
{
    int num_nodes = n + 2;

    Node p1_target = num_nodes - 1;
    Node p2_target = 0;

    Game game(num_nodes, p1_target, p2_target);

    for (Node i = 1; i <= n; ++i)
    {
        game.add_edge(i, i + 1);
        game.add_edge(i, i - 1);
    }

    return game;
}

} // namespace games
