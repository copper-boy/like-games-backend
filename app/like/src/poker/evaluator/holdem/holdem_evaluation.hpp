//
// Created by deded on 16.04.22.
//

#ifndef POKER_HOLDEM_EVALUATION_HPP
#define POKER_HOLDEM_EVALUATION_HPP

#include "../../card/cardset.hpp"
#include "holdem_lookup_tables.hpp"
#include "holdem_result.hpp"
#include "../../utils/bit.hpp"

#include <cstdint>
#include <stdexcept>

namespace like {
    namespace poker {
        namespace evaluator {
            namespace holdem {
                auto evaluate_unsafe(const cardset cs) noexcept {
                    const uint64_t mask = cs.as_bitset();
                    const uint16_t mask_c = (mask >> (0 * c_num_ranks)) & c_mask_ranks;
                    const uint16_t mask_d = (mask >> (1 * c_num_ranks)) & c_mask_ranks;
                    const uint16_t mask_h = (mask >> (2 * c_num_ranks)) & c_mask_ranks;
                    const uint16_t mask_s = (mask >> (3 * c_num_ranks)) & c_mask_ranks;

                    {
                        auto flush_or_straight_flush = [](const uint16_t mask_flush) {
                            const auto x = poker_table_straight[mask_flush];
                            if (x > 0) {
                                return holdem_result(c_straight_flush, x, 0, 0);
                            } else {
                                return holdem_result(c_flush, 0, 0, poker_table_top5[mask_flush]);
                            }
                        };

                        if (std::popcount(mask_c) >= 5) {
                            return flush_or_straight_flush(mask_c);
                        } else if (std::popcount(mask_d) >= 5) {
                            return flush_or_straight_flush(mask_d);
                        } else if (std::popcount(mask_h) >= 5) {
                            return flush_or_straight_flush(mask_h);
                        } else if (std::popcount(mask_s) >= 5) {
                            return flush_or_straight_flush(mask_s);
                        }
                    }
                    const uint16_t mask_all_cards = mask_c | mask_d | mask_h | mask_s;

                    if (const uint16_t mask_quads = (mask_c & mask_d & mask_h & mask_s); mask_quads) {
                        return holdem_result(c_four_of_a_kind, cross_idx_high16(mask_quads), 0,
                                             (uint16_t(1) << cross_idx_high16(mask_all_cards & ~mask_quads)));
                    }

                    const uint16_t mask_trips =
                            ((mask_c & mask_d) | (mask_h & mask_s)) & ((mask_c & mask_h) | (mask_d & mask_s));

                    if (mask_trips) {
                        if (std::popcount(mask_trips) > 1) {
                            return holdem_result(c_full_house, cross_idx_high16(mask_trips),
                                                 cross_idx_low16(mask_trips),
                                                 0);
                        }

                        if (const uint16_t mask_pair_fh = (mask_all_cards ^
                                                           (mask_c ^ mask_d ^ mask_h ^ mask_s)); mask_pair_fh) {
                            return holdem_result(c_full_house, cross_idx_high16(mask_trips),
                                                 cross_idx_high16(mask_pair_fh),
                                                 0);
                        }
                    }

                    const auto rank_straight = poker_table_straight[mask_all_cards];
                    if (rank_straight > 0) {
                        return holdem_result(c_straight, rank_straight, 0, 0);
                    }

                    if (mask_trips) {
                        const uint16_t mask_kickers = mask_all_cards & ~(mask_trips);
                        const auto high_kicker = cross_idx_high16(mask_kickers);
                        const auto low_kicker = cross_idx_high16(mask_kickers & ~(uint16_t(1) << high_kicker));
                        return holdem_result(c_three_of_a_kind, cross_idx_high16(mask_trips), 0,
                                             uint16_t(1) << high_kicker | uint16_t(1) << low_kicker);
                    }

                    const uint16_t mask_pair = (mask_all_cards ^ (mask_c ^ mask_d ^ mask_h ^ mask_s));
                    if (const auto num_pairs = std::popcount(mask_pair); num_pairs > 1) {
                        const auto high_rank = cross_idx_high16(mask_pair);
                        const auto low_rank = cross_idx_high16(mask_pair & ~(uint16_t(1) << high_rank));
                        const auto kicker_rank = cross_idx_high16(
                                mask_all_cards & ~(uint16_t(1) << high_rank | uint16_t(1) << low_rank));
                        return holdem_result(c_two_pair, high_rank, low_rank, uint16_t(1) << kicker_rank);
                    } else if (num_pairs > 0) {
                        const uint16_t mask_kickers = mask_all_cards & ~(mask_pair);
                        return holdem_result(c_one_pair, cross_idx_high16(mask_pair), 0,
                                             poker_table_top3[mask_kickers]);
                    }

                    return holdem_result(c_no_pair, 0, 0, poker_table_top5[mask_all_cards]);
                }
            } // namespace evaluator
        } // namespace holdem
    } // namespace poker
} // namespace like

#endif //POKER_HOLDEM_EVALUATION_HPP
