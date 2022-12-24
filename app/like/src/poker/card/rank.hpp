//
// Created by deded on 16.04.22.
//

#ifndef POKER_RANK_HPP
#define POKER_RANK_HPP

#include "../utils/utility.hpp"

#include <array>
#include <compare>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>

namespace like {
    namespace poker {
        inline namespace constants {
            enum class rank_t : uint8_t {
                two = 0,
                three,
                four,
                five,
                six,
                seven,
                eight,
                nine,
                ten,
                jack,
                queen,
                king,
                ace
            };

            const uint8_t c_rank_two = 0;
            const uint8_t c_rank_three = 1;
            const uint8_t c_rank_four = 2;
            const uint8_t c_rank_five = 3;
            const uint8_t c_rank_six = 4;
            const uint8_t c_rank_seven = 5;
            const uint8_t c_rank_eight = 6;
            const uint8_t c_rank_nine = 7;
            const uint8_t c_rank_ten = 8;
            const uint8_t c_rank_jack = 9;
            const uint8_t c_rank_queen = 10;
            const uint8_t c_rank_king = 11;
            const uint8_t c_rank_ace = 12;
            const uint8_t c_num_ranks = 13;

            const uint8_t c_mask_ranks_numbers = 0b0000'1111;
            const uint16_t c_mask_ranks = 0b0001'1111'1111'1111;

        }    // namespace constants

        class rank {
        public:
            uint8_t m_rank;

            rank() = delete;

            explicit rank(char c) {
                if (c != '\0') {
                    m_rank = from_char(c);
                    if (m_rank >= c_num_ranks) {
                        throw std::runtime_error(std::string("rank(char): could not parse char '") + c + "'");
                    }
                }
            }

            explicit rank(rank_t rt) : m_rank(static_cast<uint8_t>(rt)) {
                if (m_rank >= c_num_ranks) {
                    throw std::runtime_error("rank(const rank_t): invalid number '" + std::to_string(m_rank) + "'");
                }
            }

            explicit rank(std::string_view str) : m_rank(from_char(str[0])) {
                if (str.size() != 1) {
                    throw std::runtime_error(
                            std::string("rank(const string_view): string with wrong size '").append(str) + "'");
                } else if (m_rank >= c_num_ranks) {
                    throw std::runtime_error(
                            std::string("rank(const string_view): could not parse char '") + str[0] + "'");
                }
            }

            [[nodiscard]] uint16_t as_bitset() const noexcept { return uint16_t(1) << m_rank; }

            [[nodiscard]] std::string str() const noexcept {
                return std::string(1, to_char(static_cast<rank_t>(m_rank)));
            }

            [[nodiscard]] std::string_view str_nice_single() const noexcept {
                std::array str_representation{"Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
                                              "Nine", "Ten", "Jack", "Queen", "King", "Ace"};
                return str_representation[m_rank];
            }

            [[nodiscard]] std::string str_nice_mult() const noexcept {
                if (m_rank == c_rank_six) {
                    return (std::string(str_nice_single()) + "es");
                } else {
                    return (std::string(str_nice_single()) + "s");
                }
            }

            auto operator<=>(const rank &) const = default;

        private:
            [[nodiscard]] char to_char(rank_t rt) const noexcept {
                switch (rt) {
                    case rank_t::two:
                        return '2';
                    case rank_t::three:
                        return '3';
                    case rank_t::four:
                        return '4';
                    case rank_t::five:
                        return '5';
                    case rank_t::six:
                        return '6';
                    case rank_t::seven:
                        return '7';
                    case rank_t::eight:
                        return '8';
                    case rank_t::nine:
                        return '9';
                    case rank_t::ten:
                        return 'T';
                    case rank_t::jack:
                        return 'J';
                    case rank_t::queen:
                        return 'Q';
                    case rank_t::king:
                        return 'K';
                    case rank_t::ace:
                        return 'A';
                    default:
                        unreachable();
                }
            }

            [[nodiscard]] uint8_t from_char(char c) const noexcept {
                switch (c) {
                    case '2':
                        return c_rank_two;
                    case '3':
                        return c_rank_three;
                    case '4':
                        return c_rank_four;
                    case '5':
                        return c_rank_five;
                    case '6':
                        return c_rank_six;
                    case '7':
                        return c_rank_seven;
                    case '8':
                        return c_rank_eight;
                    case '9':
                        return c_rank_nine;
                    case 't':
                    case 'T':
                        return c_rank_ten;
                    case 'j':
                    case 'J':
                        return c_rank_jack;
                    case 'q':
                    case 'Q':
                        return c_rank_queen;
                    case 'k':
                    case 'K':
                        return c_rank_king;
                    case 'a':
                    case 'A':
                        return c_rank_ace;
                    default:
                        return c_num_ranks;
                };
            }
        };
    } // namespace poker
} // namespace like

#endif //POKER_RANK_HPP
