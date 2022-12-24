//
// Created by deded on 16.04.22.
//

#ifndef POKER_HOLDEM_EQUITY_CALCULATION_HPP
#define POKER_HOLDEM_EQUITY_CALCULATION_HPP

#include "../../card/card.hpp"
#include "../../card/cardset.hpp"
#include "../../card/hand.hpp"
#include "holdem_evaluation.hpp"

#include <algorithm>    // std::max_element, std::count
#include <cstdint>
#include <numeric>      // std::reduce
#include <stdexcept>    // std::runtime_error

namespace like {
    namespace poker {
        namespace evaluator {
            namespace holdem {
                struct equity_calculation_result_t {
                    std::vector <uint32_t> m_wins;
                    std::vector <uint32_t> m_ties;
                    std::vector<float> m_equities;
                };

                equity_calculation_result_t
                calculate_equities(const std::vector <std::string> &h, const std::vector <std::string> &v = {}) {
                    std::vector<hand_2c> hands(h.begin(), h.end());
                    std::vector<card> vec_board(v.begin(), v.end());
                    if (const auto sz = hands.size(); sz < 2 || sz > 9) {
                        throw std::runtime_error("invalid number of hands (should be in the range of [2,9])");
                    }

                    const auto all_hole_cards = [&]() {
                        cardset cs{};
                        for (auto &&hand: hands) {
                            cs = cs.combine(hand.as_cardset());
                        }
                        return cs;
                    }();

                    if (all_hole_cards.size() != hands.size() * 2) {
                        throw std::runtime_error("hands contain duplicate cards.");
                    }

                    if (vec_board.size() > 5) {
                        throw std::runtime_error("invalid number of board cards (should be less or equal to five)");
                    }
                    const auto board = [&]() {
                        cardset cs{};
                        for (auto &&card: vec_board) {
                            cs.insert(card);
                        }
                        return cs;
                    }();
                    if (board.size() != vec_board.size()) {
                        throw std::runtime_error("board contains duplicate cards");
                    }
                    const auto all_fixed_cards = board.combine(all_hole_cards);
                    if (all_fixed_cards.size() != board.size() + all_hole_cards.size()) {
                        throw std::runtime_error("hands and board contain duplicate cards");
                    }

                    std::vector <uint32_t> wins;
                    std::vector <uint32_t> ties;
                    std::vector <uint32_t> score;
                    std::vector<float> equities;
                    for (unsigned i = 0; i < hands.size(); ++i) {
                        wins.push_back(0);
                        ties.push_back(0);
                        score.push_back(0);
                        equities.push_back(0.0f);
                    }

                    auto calculate_and_store_results = [&](const cardset &additional_cards) {
                        const auto runout = additional_cards.combine(board);
                        std::vector <holdem_result> results;
                        for (auto &&hand: hands) {
                            results.emplace_back(evaluate_unsafe(runout.combine(hand.as_cardset())));
                        }

                        const auto it_max = std::max_element(results.cbegin(), results.cend());
                        const auto num_max = std::count(results.cbegin(), results.cend(), *it_max);
                        if (num_max > 1) {
                            for (unsigned n = 0; n < results.size(); ++n) {
                                if (results[n] == *it_max) {
                                    ties[n] += 1;
                                    score[n] += 1;
                                }
                            }
                        } else {
                            for (unsigned n = 0; n < results.size(); ++n) {
                                if (results[n] == *it_max) {
                                    wins[n] += 1;
                                    score[n] += static_cast<uint32_t>(hands.size());
                                    break;
                                }
                            }
                        }
                    };

                    if (board.size() == 5) {
                        calculate_and_store_results(cardset{});
                    } else {
                        for (uint8_t i = 0; i < c_deck_size; ++i) {
                            card c1{i};
                            if (all_fixed_cards.contains(c1)) {
                                continue;
                            }

                            if (board.size() == 4) {
                                const auto additional_cards = cardset{c1};
                                calculate_and_store_results(additional_cards);
                            } else {
                                for (uint8_t j = i + 1; j < c_deck_size; ++j) {
                                    card c2{j};
                                    if (all_fixed_cards.contains(c2)) {
                                        continue;
                                    }

                                    if (board.size() == 3) {
                                        const auto additional_cards = cardset{c1, c2};
                                        calculate_and_store_results(additional_cards);
                                    } else {
                                        for (uint8_t k = j + 1; k < c_deck_size; ++k) {
                                            card c3{k};
                                            if (all_fixed_cards.contains(c3)) {
                                                continue;
                                            }

                                            if (board.size() == 2) {
                                                const auto additional_cards = cardset{c1, c2, c3};
                                                calculate_and_store_results(additional_cards);
                                            } else {
                                                for (uint8_t l = k + 1; l < c_deck_size; ++l) {
                                                    card c4{l};
                                                    if (all_fixed_cards.contains(c4)) {
                                                        continue;
                                                    }

                                                    if (board.size() == 1) {
                                                        const auto additional_cards = cardset{c1, c2, c3, c4};
                                                        calculate_and_store_results(additional_cards);
                                                    } else {
                                                        for (uint8_t m = l + 1; m < c_deck_size; ++m) {
                                                            card c5{m};
                                                            if (all_fixed_cards.contains(c5)) {
                                                                continue;
                                                            }
                                                            const auto additional_cards = cardset{c1, c2, c3, c4, c5};
                                                            calculate_and_store_results(additional_cards);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    const auto total_score = std::reduce(score.cbegin(), score.cend(), uint32_t(0));
                    for (unsigned i = 0; i < hands.size(); ++i) {
                        equities[i] = static_cast<float>(score[i]) / total_score;
                        equities[i] *= 100;
                    }

                    return equity_calculation_result_t{wins, ties, equities};
                }
            } // namespace holdem
        } // namespace evaluator
    } // namespace poker
} // namespace like

#endif //POKER_HOLDEM_EQUITY_CALCULATION_HPP
