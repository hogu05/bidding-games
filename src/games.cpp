#include "games.hpp"

#include <functional>
#include <map>

namespace games
{
Game make_tow(int n, bool p1_wins_ties)
{
    const Node p1_target = n + 1;
    const Node p2_target = 0;

    std::vector<std::vector<Node>> adj_list(n + 2);

    for (Node node = 1; node <= n; ++node)
    {
        adj_list[node] = {node + 1, node - 1};
    }

    return {.adj_list = std::move(adj_list),
            .p1_target = p1_target,
            .p2_target = p2_target,
            .p1_wins_ties = p1_wins_ties};
}

Game make_race(int a, int b, bool p1_wins_ties)
{
    const Node p1_target = a * b;
    const Node p2_target = (a * b) + 1;

    std::vector<std::vector<Node>> adj_list((a * b) + 2);

    auto get_node = [=](int x, int y) -> Node
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
            adj_list[get_node(x, y)] = {get_node(x + 1, y), get_node(x, y + 1)};
        }
    }

    return {.adj_list = std::move(adj_list),
            .p1_target = p1_target,
            .p2_target = p2_target,
            .p1_wins_ties = p1_wins_ties};
}

Game make_coins(const std::vector<int>& coins, bool p1_wins_ties)
{
    const Node p1_target = 1;
    const Node p2_target = 2;
    std::vector<std::vector<Node>> adj_list(3);

    std::map<std::pair<int, int>, Node> state_to_node;

    std::function<Node(int, int)> get_node = [&](int coin_index, int score_diff) -> Node
    {
        if (coin_index == static_cast<int>(coins.size()))
        {
            if (score_diff > 0)
            {
                return p1_target;
            }
            if (score_diff < 0)
            {
                return p2_target;
            }
            return p1_wins_ties ? p1_target : p2_target;
        }

        auto state = std::make_pair(coin_index, score_diff);
        auto [it, inserted] = state_to_node.try_emplace(state, static_cast<Node>(adj_list.size()));

        if (!inserted)
        {
            return it->second;
        }

        Node node = it->second;
        adj_list.emplace_back();

        int coin = coins[coin_index];
        Node p1_wins_coin = get_node(coin_index + 1, score_diff + coin);
        Node p2_wins_coin = get_node(coin_index + 1, score_diff - coin);
        adj_list[node] = {p1_wins_coin, p2_wins_coin};

        return node;
    };

    adj_list[0] = {get_node(1, coins[0]), get_node(1, -coins[0])};

    return {.adj_list = std::move(adj_list),
            .p1_target = p1_target,
            .p2_target = p2_target,
            .p1_wins_ties = p1_wins_ties};
}

Game make_game_sum(const std::vector<RootedGame>& rooted_games, bool p1_wins_ties)
{
    const Node p1_target = 1;
    const Node p2_target = 2;
    std::vector<std::vector<Node>> adj_list(3);

    for (auto&& rooted_game : rooted_games)
    {
        const Game& subgame = rooted_game.game;
        const int subgame_num_nodes = static_cast<int>(subgame.adj_list.size());

        std::vector<Node> node_mapping(subgame_num_nodes);
        node_mapping[subgame.p1_target] = p1_target;
        node_mapping[subgame.p2_target] = p2_target;

        for (Node node = 0; node < subgame_num_nodes; ++node)
        {
            if (node == subgame.p1_target || node == subgame.p2_target)
            {
                continue;
            }

            node_mapping[node] = static_cast<Node>(adj_list.size());
            adj_list.emplace_back();
        }

        adj_list[0].push_back(node_mapping[rooted_game.start_node]);

        for (Node node = 0; node < subgame_num_nodes; ++node)
        {
            if (node == subgame.p1_target || node == subgame.p2_target)
            {
                continue;
            }

            Node mapped_node = node_mapping[node];

            for (Node neighbor : subgame.adj_list[node])
            {
                adj_list[mapped_node].push_back(node_mapping[neighbor]);
            }
        }
    }

    return {.adj_list = std::move(adj_list),
            .p1_target = p1_target,
            .p2_target = p2_target,
            .p1_wins_ties = p1_wins_ties};
}

} // namespace games
