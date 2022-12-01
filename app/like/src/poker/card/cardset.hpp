//
// Created by deded on 16.04.22.
//

#ifndef POKER_CARDSET_HPP
#define POKER_CARDSET_HPP

#include "../utils/bit.hpp"
#include "card.hpp"

#include <algorithm>
#include <array>
#include <cstdint>
#include <initializer_list>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

namespace like {
namespace poker {
inline namespace constants {
const uint64_t c_cardset_full = 0xFFFF'FFFF'FFFF'FFFF >> (64 - c_deck_size);
} // namespace constants

class cardset {
  uint64_t m_cards = 0;

  auto set(const uint64_t &bitset) noexcept {
    m_cards = bitset;
    return *this;
  }

public:
  cardset() = default;

  explicit cardset(const uint64_t &bitset) : m_cards(bitset) {
    if (bitset > c_cardset_full) {
      throw std::runtime_error("cardset(const uint64_t): cardset max value (" +
                               std::to_string(c_cardset_full) +
                               ") exceeded by argument " +
                               std::to_string(bitset));
    }
  }

  explicit cardset(const std::span<const card> sp) noexcept {
    for (auto &&c : sp) {
      m_cards |= c.as_bitset();
    }
  }

  explicit cardset(const std::initializer_list<const card> li) noexcept {
    for (auto &&c : li) {
      m_cards |= c.as_bitset();
    }
  }

  explicit cardset(const std::string_view sv) {
    if (0 != sv.size() % 2) {
      throw std::runtime_error(
          std::string("string with wrong size: '").append(sv) + "'");
    } else {
      for (size_t i = 0; i < sv.size(); i += 2) {
        m_cards |= card{sv.substr(i, 2)}.as_bitset();
      }
    }
  }

  [[nodiscard]] size_t size() const noexcept { return std::popcount(m_cards); }

  [[nodiscard]] uint64_t as_bitset() const noexcept { return m_cards; }

  [[nodiscard]] std::string str() const noexcept {
    std::string out{};
    for (uint64_t mask = m_cards; mask;) {
      const auto idx = cross_idx_low64(mask);
      out += card(idx).str();
      mask &= mask - 1;
    }
    return out;
  }

  [[nodiscard]] bool contains(const card c) const noexcept {
    return (m_cards & c.as_bitset()) != 0;
  }

  [[nodiscard]] bool contains(const cardset &cs) const noexcept {
    return (m_cards | cs.m_cards) == m_cards;
  }

  [[nodiscard]] cardset combine(const card c) const noexcept {
    return cardset{}.set(m_cards | c.as_bitset());
  }

  [[nodiscard]] cardset combine(const cardset &cs) const noexcept {
    return cardset{}.set(m_cards | cs.m_cards);
  }

  void clear() noexcept { m_cards = 0; }

  void fill() noexcept { m_cards = c_cardset_full; }

  void insert(const card c) noexcept { m_cards |= c.as_bitset(); }

  void join(const cardset cs) noexcept { m_cards |= cs.m_cards; }

  void remove(const card c) noexcept { m_cards ^= c.as_bitset(); }

  void remove(const cardset cs) noexcept { m_cards ^= cs.m_cards; }

  auto operator<=>(const cardset &) const noexcept = default;
};
} // namespace poker
} // namespace like

#endif // POKER_CARDSET_HPP
