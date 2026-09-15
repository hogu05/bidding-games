from allpay import compute_poorman_thresholds, compute_richman_threshold


def assert_poorman_thresholds(game, node, expected, max_budget):
    thresholds = compute_poorman_thresholds(game, max_budget)
    for p2_budget in range(max_budget + 1):
        actual = thresholds[node][p2_budget]
        expected_value = expected(p2_budget)
        assert (
            actual == expected_value
        ), f"node={node} p2_budget={p2_budget}: got {actual}, expected {expected_value}"


def assert_richman_thresholds(game, node, expected, max_budget):
    for p2_budget in range(max_budget + 1):
        actual = compute_richman_threshold(game, node, p2_budget)
        expected_value = expected(p2_budget)
        assert (
            actual == expected_value
        ), f"node={node} p2_budget={p2_budget}: got {actual}, expected {expected_value}"
