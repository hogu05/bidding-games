#pragma once
#include <vector>

#include "types.hpp"

class Game
{
  private:
    std::vector<std::vector<Node>> adj_list;
    Node p1_target;
    Node p2_target;
    bool p1_wins_ties;

  public:
    Game(std::vector<std::vector<Node>> adj_list, Node p1_target, Node p2_target,
         bool p1_wins_ties);
    Game flipped() const;

    int get_num_nodes() const;
    Node get_p1_target() const;
    Node get_p2_target() const;
    const std::vector<Node>& get_neighbors(Node node) const;
    bool get_p1_wins_ties() const;
};
