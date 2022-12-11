//
// Created by deded on 10/22/22.
//

#ifndef POKER_MICROSERVICES_UTILS_HPP
#define POKER_MICROSERVICES_UTILS_HPP

#include "poker/evaluator/holdem/holdem_equity_calculation.hpp"
#include "poker/evaluator/holdem/holdem_evaluation.hpp"
#include "poker/evaluator/holdem/holdem_result.hpp"
#include "poker/game/holdem/game.hpp"

#include <optional>

namespace like {
namespace utils {
namespace holdem {
auto side_pot_winners(const poker::game::holdem::gamecards &cards,
                      const std::vector<size_t> &eligible_player_indices)
    -> std::vector<std::pair<poker::evaluator::holdem::holdem_result, size_t>> {
  std::vector<std::pair<poker::evaluator::holdem::holdem_result, size_t>>
      winners;
  std::for_each(eligible_player_indices.cbegin(),
                eligible_player_indices.cend(), [&](const size_t pos) {
                  winners.emplace_back(
                      poker::evaluator::holdem::evaluate_unsafe(
                          poker::cardset(cards.m_board)
                              .combine(cards.m_hands[pos].as_cardset())),
                      pos);
                });
  std::sort(
      winners.begin(), winners.end(),
      [&](const auto &lhs, const auto &rhs) { return lhs.first > rhs.first; });
  const auto first_non_winner =
      std::find_if(winners.cbegin() + 1, winners.cend(),
                   [&](const auto &e) { return e.first < winners[0].first; });
  const auto dist = std::distance(winners.cbegin(), first_non_winner);

  winners.resize(
      dist,
      std::make_pair(poker::evaluator::holdem::holdem_result(0, 0, 0, 0), 0));

  return winners;
}
} // namespace utils
} // namespace like

#endif // POKER_MICROSERVICES_UTILS_HPP
