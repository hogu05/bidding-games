#include "games.hpp"

#include <functional>
#include <map>

namespace games
{
Game make_tow(int n, bool p1_wins_ties)
{
    int num_nodes = n + 2;

    Node p1_target = num_nodes - 1;
    Node p2_target = 0;

    std::vector<std::vector<Node>> adj_list(num_nodes);

    for (Node i = 1; i <= n; ++i)
    {
        adj_list[i].push_back(i + 1);
        adj_list[i].push_back(i - 1);
    }

    return {std::move(adj_list), p1_target, p2_target, p1_wins_ties};
}

Game make_race(int a, int b, bool p1_wins_ties)
{
    int num_nodes = (a * b) + 2;

    Node p1_target = a * b;
    Node p2_target = (a * b) + 1;

    std::vector<std::vector<Node>> adj_list(num_nodes);

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
            Node node = get_node(x, y);

            adj_list[node].push_back(get_node(x + 1, y));
            adj_list[node].push_back(get_node(x, y + 1));
        }
    }

    return {std::move(adj_list), p1_target, p2_target, p1_wins_ties};
}

Game make_coins(const std::vector<int>& coins, bool p1_wins_ties)
{
    int num_coins = static_cast<int>(coins.size());
    const Node p1_target = 1;
    const Node p2_target = 2;
    std::vector<std::vector<Node>> adj_list(3);

    std::map<std::pair<int, int>, Node> state_to_node;

    std::function<Node(int, int)> build_node = [&](int coin_index, int score_diff) -> Node
    {
        if (coin_index == num_coins)
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
        Node p1_wins_coin = build_node(coin_index + 1, score_diff + coin);
        Node p2_wins_coin = build_node(coin_index + 1, score_diff - coin);
        adj_list[node] = {p1_wins_coin, p2_wins_coin};

        return node;
    };

    adj_list[0] = {build_node(1, coins[0]), build_node(1, -coins[0])};

    return {std::move(adj_list), p1_target, p2_target, p1_wins_ties};
}
} // namespace games
