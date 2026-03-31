#include "games.hpp"

namespace games
{
Game make_tow(int n, bool p1_wins_ties)
{
    int num_nodes = n + 2;

    Node p1_target = num_nodes - 1;
    Node p2_target = 0;

    Game game(num_nodes, p1_target, p2_target, p1_wins_ties);

    for (Node i = 1; i <= n; ++i)
    {
        game.add_edge(i, i + 1);
        game.add_edge(i, i - 1);
    }

    return game;
}

Game make_race(int a, int b, bool p1_wins_ties)
{
    int num_nodes = (a * b) + 2;

    Node p1_target = a * b;
    Node p2_target = (a * b) + 1;

    Game game(num_nodes, p1_target, p2_target, p1_wins_ties);

    auto get_node = [&](int x, int y) -> Node
    {
        if (x == a)
        {
            return p1_target;
        }
        if (y == b)
        {
            return p2_target;
        }

        return (x * b) + y;
    };

    for (int x = 0; x < a; ++x)
    {
        for (int y = 0; y < b; ++y)
        {
            Node node = get_node(x, y);

            game.add_edge(node, get_node(x + 1, y));
            game.add_edge(node, get_node(x, y + 1));
        }
    }

    return game;
}

} // namespace games
