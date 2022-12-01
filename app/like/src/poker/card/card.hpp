//
// Created by deded on 16.04.22.
//

#ifndef POKER_CARD_HPP
#define POKER_CARD_HPP

#include "rank.hpp"
#include "suit.hpp"

#include <compare>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>

namespace like {
namespace poker {
inline namespace constants {
const uint8_t c_deck_size = c_num_ranks * c_num_suits;
const uint8_t c_cardindex_min = 0;
const uint8_t c_cardindex_max = c_deck_size - 1;
} // namespace constants

class card {
public:
  const uint8_t m_card;

  card() = delete;

  card(uint8_t idx) : m_card(idx) {
    if (m_card > c_cardindex_max) {
      throw std::runtime_error("card(const uint8_t): tried to create card with "
                               "'out of bounds' index '" +
                               std::to_string(m_card) + "'");
    }
  }

  card(std::string_view sv)
      : m_card(poker::rank{sv[0]}.m_rank +
               poker::suit{sv[1]}.m_suit * c_num_ranks) {}

  card(const rank r, const suit s) noexcept
      : m_card(r.m_rank + s.m_suit * c_num_ranks) {}

  card(const rank_t rt, const suit_t st)
      : card(poker::rank{rt}, poker::suit{st}) {}

  [[nodiscard]] uint64_t as_bitset() const noexcept {
    return uint64_t(1) << m_card;
  }

  [[nodiscard]] poker::rank rank() const noexcept {
    return poker::rank{rank_t{uint8_t(m_card % c_num_ranks)}};
  }

  [[nodiscard]] poker::suit suit() const noexcept {
    return poker::suit{suit_t{uint8_t(m_card / c_num_ranks)}};
  }

  [[nodiscard]] std::string str() const noexcept {
    return std::string(cardstrings.substr(static_cast<size_t>(m_card) * 2, 2));
  }

  operator std::string() { return str(); }

  std::strong_ordering operator<=>(const card &other) const noexcept {
    if (const auto cmp = m_card % c_num_ranks <=> other.m_card % c_num_ranks;
        cmp != 0) {
      return cmp;
    }
    return m_card / c_num_suits <=> other.m_card / c_num_suits;
  }

  bool operator==(const card &other) const noexcept {
    return m_card == other.m_card;
  }

private:
  static inline const std::string cardstrings =
      "2c3c4c5c6c7c8c9cTcJcQcKcAc2d3d4d5d6d7d8d9dTdJdQdKdAd2h3h4h5h6h7h8h9hThJh"
      "QhKhAh2s3s4s5s6s7s8s9sTsJsQsKsAs";
};
} // namespace poker
} // namespace like

#endif // POKER_CARD_HPP
