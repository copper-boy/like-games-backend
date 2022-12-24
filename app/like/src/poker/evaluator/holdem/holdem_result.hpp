//
// Created by deded on 16.04.22.
//

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wc++17-extensions"
#ifndef POKER_HOLDEM_RESULT_HPP
#define POKER_HOLDEM_RESULT_HPP

#include "../../card/rank.hpp"
#include "../../utils/bit.hpp"
#include "../../utils/utility.hpp"

#include <array>
#include <bitset>
#include <cstdint>
#include <stdexcept>
#include <string>

namespace like {
    namespace poker {
        namespace evaluator {
            namespace holdem {
                inline namespace constants {
                    const uint8_t c_no_pair = 0;
                    const uint8_t c_one_pair = 1;
                    const uint8_t c_two_pair = 2;
                    const uint8_t c_three_of_a_kind = 3;
                    const uint8_t c_straight = 4;
                    const uint8_t c_flush = 5;
                    const uint8_t c_full_house = 6;
                    const uint8_t c_four_of_a_kind = 7;
                    const uint8_t c_straight_flush = 8;

                    const uint8_t c_offset_minor = c_num_ranks;
                    const uint8_t c_offset_major = c_offset_minor + 4;
                    const uint8_t c_offset_type = c_offset_major + 4;
                } // namespace constants

                class holdem_result {
                    uint32_t m_result;

                public:

                    holdem_result() = delete;

                    holdem_result(uint8_t type, uint8_t major, uint8_t minor, uint16_t kickers) noexcept :
                            m_result((type << c_offset_type) | (major << c_offset_major) | (minor << c_offset_minor) |(kickers & c_mask_ranks)) {}

                    [[nodiscard]] uint8_t type() const noexcept {
                        return static_cast<uint8_t>(m_result >> c_offset_type);
                    };

                    [[nodiscard]] rank major_rank() const noexcept {
                        return rank(rank_t(c_mask_ranks_numbers & ((m_result >> c_offset_major) - 0)));
                    };

                    [[nodiscard]] rank minor_rank() const noexcept {
                        return rank(rank_t(c_mask_ranks_numbers & ((m_result >> c_offset_minor) - 0)));
                    };

                    [[nodiscard]] uint16_t kickers() const noexcept { return (c_mask_ranks & m_result); };

                    [[nodiscard]] uint32_t as_bitset() const noexcept { return m_result; };

                    [[nodiscard]] std::string str() const {
                        std::array str_representation{"high card,", "a pair of", "two pairs,", "three of a kind,",
                                                      "a straight,",
                                                      "a flush,", "a full house,", "four of a kind,",
                                                      "a straight flush,"};

                        switch (const uint8_t t = type(); t) {
                            case c_no_pair:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       std::string(rank{rank_t{cross_idx_high16(kickers())}}.str_nice_single());
                            case c_one_pair:
                            case c_three_of_a_kind:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       major_rank().str_nice_mult();
                            case c_four_of_a_kind:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       major_rank().str_nice_mult();
                            case c_two_pair:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       major_rank().str_nice_mult() + std::string(" and ") +
                                       minor_rank().str_nice_mult();
                            case c_full_house:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       major_rank().str_nice_mult() + std::string(" full of ") +
                                       minor_rank().str_nice_mult();
                            case c_straight:
                            case c_straight_flush:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       std::string(major_rank().str_nice_single()) + std::string(" high");
                            case c_flush:
                                return std::string(str_representation[t]) + std::string(" ") +
                                       std::string(rank{rank_t{cross_idx_high16(kickers())}}.str_nice_single()) +
                                       std::string(" high");
                            default:
                                throw std::runtime_error("invalid evaluation result");
                        }
                    }

                    [[nodiscard]] std::string str_long() const {
                        switch (const uint8_t t = type(); t) {
                            case c_no_pair:
                            case c_one_pair:
                            case c_three_of_a_kind:
                            case c_four_of_a_kind:
                            case c_two_pair:
                            case c_flush:
                                return str() + ", kicker(s): " + str_kickers();
                            default:
                                return str();
                        }
                    }

                    auto operator<=>(const holdem_result &) const = default;

                private:
                    std::string str_kickers() const {
                        std::string str;
                        const uint16_t k = kickers();

                        int8_t i = c_num_ranks;
                        for (uint64_t mask = uint64_t(1) << c_num_ranks; mask; mask >>= 1, i--) {
                            if (k & mask) {
                                str += std::string(rank(rank_t(i)).str_nice_single()) + " ";
                            }
                        }
                        str.pop_back();
                        return str;
                    }
                };
            } // namespace holdem
        } // namespace evaluator
    } // namespace poker
} // namespace like

#endif //POKER_HOLDEM_RESULT_HPP

#pragma clang diagnostic pop