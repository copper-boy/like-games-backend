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

auto wins_in_percentages(
    const poker::evaluator::holdem::equity_calculation_result_t &__results)
    -> std::vector<std::pair<uint64_t, std::string>> {
  std::vector<std::pair<uint64_t, std::string>> wins;
  for (size_t index = 0; auto const &result : __results.m_equities) {
    wins.push_back(std::make_pair(
        index++,
        (std::stringstream{} << std::fixed << std::setprecision(2) << result)
            .str()));
  }
  return wins;
}
} // namespace holdem

struct unique_t {
public:
  unique_t(size_t from) : _current{from} {}

  size_t operator()() { return _current++; }

private:
  size_t _current = 0;
};

auto generator(size_t size) -> std::vector<size_t> {
  std::vector<size_t> generated(size);

  std::generate(generated.begin(), generated.end(), unique_t{0});

  return generated;
}
} // namespace utils
} // namespace like

#endif // POKER_MICROSERVICES_UTILS_HPP
