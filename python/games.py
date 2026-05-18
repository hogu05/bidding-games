from allpay import Game, Player


def make_tow(n, tiebreaker=Player.P1):
    p1_target = n + 1
    p2_target = 0
    adj_list = [[] for _ in range(n + 2)]
    for node in range(1, n + 1):
        adj_list[node] = [node + 1, node - 1]
    return Game(adj_list, p1_target, p2_target, tiebreaker)


def make_race(a, b, tiebreaker=Player.P1):
    p1_target = a * b
    p2_target = a * b + 1
    adj_list = [[] for _ in range(a * b + 2)]

    def get_node(x, y):
        if x == a:
            return p1_target
        if y == b:
            return p2_target
        return x * b + y

    for x in range(a):
        for y in range(b):
            adj_list[get_node(x, y)] = [get_node(x + 1, y), get_node(x, y + 1)]

    return Game(adj_list, p1_target, p2_target, tiebreaker)


def make_coins(coins, tiebreaker=Player.P1):
    p1_target = 1
    p2_target = 2
    adj_list = [[], [], []]
    state_to_node = {}

    def get_node(coin_index, score_diff):
        if coin_index == len(coins):
            if score_diff > 0:
                return p1_target
            if score_diff < 0:
                return p2_target
            return p1_target if tiebreaker == Player.P1 else p2_target

        state = (coin_index, score_diff)
        if state in state_to_node:
            return state_to_node[state]

        node = len(adj_list)
        state_to_node[state] = node
        adj_list.append([])

        coin = coins[coin_index]
        p1_win_coin = get_node(coin_index + 1, score_diff + coin)
        p2_win_coin = get_node(coin_index + 1, score_diff - coin)
        adj_list[node] = [p1_win_coin, p2_win_coin]

        return node

    adj_list[0] = [get_node(1, coins[0]), get_node(1, -coins[0])]
    return Game(adj_list, p1_target, p2_target, tiebreaker)


def make_game_sum(rooted_games, tiebreaker=Player.P1):
    p1_target = 1
    p2_target = 2
    adj_list = [[], [], []]

    for rooted_game in rooted_games:
        subgame = rooted_game.game
        subgame_adj = subgame.adj_list
        subgame_num_nodes = len(subgame_adj)

        node_mapping = [None] * subgame_num_nodes
        node_mapping[subgame.p1_target] = p1_target
        node_mapping[subgame.p2_target] = p2_target

        for node in range(subgame_num_nodes):
            if node == subgame.p1_target or node == subgame.p2_target:
                continue
            node_mapping[node] = len(adj_list)
            adj_list.append([])

        adj_list[0].append(node_mapping[rooted_game.start_node])

        for node in range(subgame_num_nodes):
            if node == subgame.p1_target or node == subgame.p2_target:
                continue
            mapped_node = node_mapping[node]
            for neighbor in subgame_adj[node]:
                adj_list[mapped_node].append(node_mapping[neighbor])

    return Game(adj_list, p1_target, p2_target, tiebreaker)
