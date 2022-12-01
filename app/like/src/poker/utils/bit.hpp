//
// Created by deded on 16.04.22.
//

#ifndef POKER_BIT_HPP
#define POKER_BIT_HPP

#include <bit>
#include <cstdint>

namespace like {
namespace poker {
uint8_t cross_idx_low16(const uint16_t mask) {
  return mask == 0 ? 0 : static_cast<uint8_t>(std::countr_zero(mask));
}

uint8_t cross_idx_low64(const uint64_t mask) {
  return mask == 0 ? 0 : static_cast<uint8_t>(std::countr_zero(mask));
}

uint8_t cross_idx_high16(const uint16_t mask) {
  return mask == 0 ? 0 : static_cast<uint8_t>(15 - std::countl_zero(mask));
}

uint8_t cross_idx_high64(const uint64_t mask) {
  return mask == 0 ? 0 : static_cast<uint8_t>(63 - std::countl_zero(mask));
}
} // namespace poker
} // namespace like

#endif // POKER_BIT_HPP
