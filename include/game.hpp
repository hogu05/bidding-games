#pragma once
#include <vector>

#include "types.hpp"

class Game
{
  private:
    int num_nodes;
    Node p1_target;
    Node p2_target;
    std::vector<std::vector<Node>> adj_list;
    bool p1_wins_ties;

  public:
    Game(int num_nodes, Node p1_target, Node p2_target, bool p1_wins_ties);
    void add_edge(Node from, Node to);

    int get_num_nodes() const;
    Node get_p1_target() const;
    Node get_p2_target() const;
    const std::vector<Node>& get_neighbors(Node node) const;
    bool get_p1_wins_ties() const;
};
