#include <chrono>
#include <iostream>

#include "games.hpp"
#include "solver.hpp"

int main()
{
    Game race = games::make_race(3, 3);
    Game tow = games::make_tow(3);

    auto start_time = std::chrono::high_resolution_clock::now();

    Coins race_threshold = solver::poorman_reachability(race, 0, 100);
    Coins tow_threshold = solver::poorman_reachability(tow, 3, 100);

    auto end_time = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

    std::cout << "RACE: " << race_threshold << std::endl;
    std::cout << "TOW: " << tow_threshold << std::endl;
    std::cout << duration << std::endl;

    return 0;
}
