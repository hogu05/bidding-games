from allpay import Game


def build_elements(game: Game, current_node: int | None = None) -> list[dict]:
    nodes = [_node_element(game, node, current_node) for node in range(len(game.adj_list))]
    edges = [
        _edge_element(source, target)
        for source, neighbors in enumerate(game.adj_list)
        for target in neighbors
    ]
    return nodes + edges


def _node_element(game: Game, node: int, current_node: int | None) -> dict:
    classes = []
    if node == game.p1_target:
        classes.append("p1-target")
    elif node == game.p2_target:
        classes.append("p2-target")
    if node == current_node:
        classes.append("current")
    return {"data": {"id": str(node)}, "classes": " ".join(classes)}


def _edge_element(source: int, target: int) -> dict:
    return {"data": {"source": str(source), "target": str(target)}}
