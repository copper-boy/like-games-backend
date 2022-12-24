//
// Created by deded on 16.04.22.
//

#ifndef POKER_SUIT_HPP
#define POKER_SUIT_HPP

#include "../utils/utility.hpp"

#include <compare>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>

namespace like {
    namespace poker {
        inline namespace constants {
            enum class suit_t : uint8_t {
                clubs = 0,
                diamonds,
                hearts,
                spades
            };

            const uint8_t c_suit_clubs = 0;
            const uint8_t c_suit_diamonds = 1;
            const uint8_t c_suit_hearts = 2;
            const uint8_t c_suit_spades = 3;
            const uint8_t c_num_suits = 4;
        }    // namespace constants

        class suit {
        public:
            uint8_t m_suit;

            suit() = delete;

            explicit suit(char c) {
                if (c != '\0') {
                    m_suit = from_char(c);
                    if (m_suit >= c_num_suits) {
                        throw std::runtime_error(std::string("suit(const char): could not parse char '") + c + "'");
                    }
                }
            }

            explicit suit(suit_t st) : m_suit(static_cast<uint8_t>(st)) {
                if (m_suit >= c_num_suits) {
                    throw std::runtime_error("suit(const suit_t): invalid number '" + std::to_string(m_suit) + "'");
                }
            }

            explicit suit(std::string_view str) : m_suit(from_char(str[0])) {
                if (str.size() != 1) {
                    throw std::runtime_error(
                            std::string("suit(const string_view): string with wrong size '").append(str) + "'");
                } else if (m_suit >= c_num_suits) {
                    throw std::runtime_error(
                            std::string("suit(const string_view): could not parse char '") + str[0] + "'");
                }
            }

            [[nodiscard]] std::string str() const noexcept { return std::string(1, to_char(static_cast<suit_t>(m_suit))); }

            auto operator<=>(const suit &) const noexcept = default;

        private:
            [[nodiscard]] char to_char(suit_t st) const noexcept {
                switch (st) {
                    case suit_t::clubs:
                        return 'c';
                    case suit_t::diamonds:
                        return 'd';
                    case suit_t::hearts:
                        return 'h';
                    case suit_t::spades:
                        return 's';
                    default:
                        unreachable();
                }
            }

            [[nodiscard]] uint8_t from_char(char c) const noexcept {
                switch (c) {
                    case 'c':
                    case 'C':
                        return c_suit_clubs;
                    case 'd':
                    case 'D':
                        return c_suit_diamonds;
                    case 'h':
                    case 'H':
                        return c_suit_hearts;
                    case 's':
                    case 'S':
                        return c_suit_spades;
                    default:
                        return c_num_suits;
                };
            }
        };
    } // namespace poker
} // namespace like

#endif //POKER_SUIT_HPP
