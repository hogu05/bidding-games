#include "lp.hpp"

#include <Highs.h>
#include <numeric>

namespace lp
{

static std::unique_ptr<Highs> build_lp(const std::vector<std::vector<double>>& payoff_matrix,
                                       Player player)
{
    auto max_p1_bid = static_cast<Coins>(payoff_matrix.size());
    auto max_p2_bid = static_cast<Coins>(payoff_matrix[0].size());

    auto highs = std::make_unique<Highs>();
    highs->setOptionValue("output_flag", false);

    if (player == Player::P1)
    {
        highs->changeObjectiveSense(ObjSense::kMaximize);

        for (Coins _ = 0; _ < max_p1_bid; ++_)
        {
            highs->addVar(0.0, 1.0);
        }
        highs->addVar(0.0, 1.0);
        highs->changeColCost(max_p1_bid, 1.0);

        std::vector<int> sum_indices(max_p1_bid);
        std::iota(sum_indices.begin(), sum_indices.end(), 0);
        std::vector<double> sum_values(max_p1_bid, 1.0);
        highs->addRow(1.0, 1.0, max_p1_bid, sum_indices.data(), sum_values.data());

        for (Coins p2_bid = 0; p2_bid < max_p2_bid; ++p2_bid)
        {
            std::vector<int> value_indices;
            std::vector<double> value_values;
            for (Coins p1_bid = 0; p1_bid < max_p1_bid; ++p1_bid)
            {
                value_indices.push_back(p1_bid);
                value_values.push_back(payoff_matrix[p1_bid][p2_bid]);
            }
            value_indices.push_back(max_p1_bid);
            value_values.push_back(-1.0);
            highs->addRow(0.0, kHighsInf, max_p1_bid + 1, value_indices.data(),
                          value_values.data());
        }
    }
    else
    {
        highs->changeObjectiveSense(ObjSense::kMinimize);

        for (Coins _ = 0; _ < max_p2_bid; ++_)
        {
            highs->addVar(0.0, 1.0);
        }
        highs->addVar(0.0, 1.0);
        highs->changeColCost(max_p2_bid, 1.0);

        std::vector<int> sum_indices(max_p2_bid);
        std::iota(sum_indices.begin(), sum_indices.end(), 0);
        std::vector<double> sum_values(max_p2_bid, 1.0);
        highs->addRow(1.0, 1.0, max_p2_bid, sum_indices.data(), sum_values.data());

        for (Coins p1_bid = 0; p1_bid < max_p1_bid; ++p1_bid)
        {
            std::vector<int> value_indices;
            std::vector<double> value_values;
            for (Coins p2_bid = 0; p2_bid < max_p2_bid; ++p2_bid)
            {
                value_indices.push_back(p2_bid);
                value_values.push_back(payoff_matrix[p1_bid][p2_bid]);
            }
            value_indices.push_back(max_p2_bid);
            value_values.push_back(-1.0);
            highs->addRow(-kHighsInf, 0.0, max_p2_bid + 1, value_indices.data(),
                          value_values.data());
        }
    }

    return highs;
}

double compute_matrix_value(const std::vector<std::vector<double>>& payoff_matrix)
{
    auto highs = build_lp(payoff_matrix, Player::P1);
    highs->run();
    int value_index = static_cast<Coins>(payoff_matrix.size());
    return highs->getSolution().col_value[value_index];
}

std::vector<double> get_strategy(const std::vector<std::vector<double>>& payoff_matrix,
                                 Player player)
{
    auto highs = build_lp(payoff_matrix, player);
    highs->run();
    const auto& col_values = highs->getSolution().col_value;
    Coins num_bids = (player == Player::P1) ? static_cast<Coins>(payoff_matrix.size())
                                            : static_cast<Coins>(payoff_matrix[0].size());
    return {col_values.begin(), col_values.begin() + num_bids};
}

} // namespace lp
