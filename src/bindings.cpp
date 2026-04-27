#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>

#include "game.hpp"
#include "games.hpp"
#include "solver.hpp"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(allpay, m)
{
    nb::class_<Game>(m, "Game").def("flipped", &Game::flipped);

    nb::class_<RootedGame>(m, "RootedGame")
        .def(nb::init<Game, Node>(), "game"_a, "start_node"_a)
        .def_ro("game", &RootedGame::game)
        .def_ro("start_node", &RootedGame::start_node);

    m.def("make_race", &games::make_race, "a"_a, "b"_a, "p1_wins_ties"_a = true);
    m.def("make_tow", &games::make_tow, "n"_a, "p1_wins_ties"_a = true);
    m.def("make_coins", &games::make_coins, "coins"_a, "p1_wins_ties"_a = true);
    m.def("make_game_sum", &games::make_game_sum, "rooted_games"_a, "p1_wins_ties"_a = true);

    m.def("poorman_reachability", &solver::poorman_reachability, "game"_a, "p2_budget"_a);
}
