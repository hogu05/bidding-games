#pragma once
#include <vector>

#include "types.hpp"

namespace lp
{
double compute_matrix_value(const std::vector<std::vector<double>>& payoff_matrix);
std::vector<double> get_strategy(const std::vector<std::vector<double>>& payoff_matrix,
                                 Player player);
} // namespace lp
