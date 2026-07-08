#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>

#include "game.hpp"
#include "poorman.hpp"
#include "richman.hpp"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(allpay, m)
{
    nb::enum_<Player>(m, "Player").value("P1", Player::P1).value("P2", Player::P2);

    nb::class_<Game>(m, "Game")
        .def(nb::init<std::vector<std::vector<Node>>, Node, Node, Player>(), "adj_list"_a,
             "p1_target"_a, "p2_target"_a, "tiebreaker"_a)
        .def_ro("adj_list", &Game::adj_list)
        .def_ro("p1_target", &Game::p1_target)
        .def_ro("p2_target", &Game::p2_target)
        .def_ro("tiebreaker", &Game::tiebreaker)
        .def("flipped", &Game::flipped);

    nb::class_<RootedGame>(m, "RootedGame")
        .def(nb::init<Game, Node>(), "game"_a, "start_node"_a)
        .def_ro("game", &RootedGame::game)
        .def_ro("start_node", &RootedGame::start_node);

    m.def("compute_poorman_thresholds", &poorman::compute_thresholds, "game"_a, "max_p2_budget"_a);
    m.def("compute_poorman_values", &poorman::compute_values, "game"_a, "max_p1_budget"_a,
          "max_p2_budget"_a);
    m.def("get_poorman_strategy", &poorman::get_strategy, "game"_a, "node"_a, "p1_budget"_a,
          "p2_budget"_a, "values"_a, "player"_a);

    m.def("compute_richman_thresholds", &richman::compute_thresholds, "game"_a, "total_budget"_a);
    m.def("compute_richman_threshold", &richman::compute_threshold, "game"_a, "node"_a,
          "p2_budget"_a);
    m.def("compute_richman_values", &richman::compute_values, "game"_a, "total_budget"_a);
    m.def("get_richman_strategy", &richman::get_strategy, "game"_a, "node"_a, "p1_budget"_a,
          "values"_a, "player"_a);
}
