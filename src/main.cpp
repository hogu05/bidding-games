#include <chrono>
#include <iostream>

#include "games.hpp"
#include "poorman.hpp"

int main()
{
    Game game1 = games::make_tow(18, true);
    Game game2 = games::make_coins({1, 2, 3, 4, 5}, true);
    Game game3 = games::make_race(10, 10, true);
    Game game4 = games::make_game_sum(
        {RootedGame(game1, 2), RootedGame(game2, 0), RootedGame(game3, 0)}, true);

    auto start = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<Coins>> winning_thresholds1 = poorman::compute_thresholds(game1, 1000);
    std::vector<std::vector<Coins>> winning_thresholds2 = poorman::compute_thresholds(game2, 1000);
    std::vector<std::vector<Coins>> winning_thresholds3 = poorman::compute_thresholds(game3, 1000);
    std::vector<std::vector<Coins>> winning_thresholds4 = poorman::compute_thresholds(game4, 1000);

    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> elapsed = end - start;
    std::cout << elapsed.count() << std::endl;
    std::cout << winning_thresholds1[2][1000] << std::endl;
    std::cout << winning_thresholds2[0][1000] << std::endl;
    std::cout << winning_thresholds3[0][1000] << std::endl;
    std::cout << winning_thresholds4[0][1000] << std::endl;

    Game game5 = games::make_tow(2, true);
    std::vector<std::vector<std::vector<double>>> dp = poorman::compute_values(game5, 10, 10);

    std::cout << dp[1][10][10] << std::endl;

    return 0;
}
