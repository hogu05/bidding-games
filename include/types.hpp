#pragma once

#include <cstdint>
#include <limits>

using Node = int;
using Coins = int;

constexpr Coins INF_COINS = std::numeric_limits<Coins>::max();

enum class Player : std::uint8_t
{
    P1,
    P2
};
