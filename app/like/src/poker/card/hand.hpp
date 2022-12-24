//
// Created by deded on 16.04.22.
//

#ifndef POKER_HAND_HPP
#define POKER_HAND_HPP

#include "card.hpp"
#include "cardset.hpp"

#include <array>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <utility>

namespace like {
    namespace poker {
        template<typename T>
        using is_card = std::is_same<T, typename poker::card>;
        template<typename T>
        const bool is_card_v = is_card<T>::value;
        template<typename T>
        using is_rank = std::is_same<T, typename poker::rank>;
        template<typename T>
        inline const bool is_rank_v = is_rank<T>::value;
        template<typename T>
        using is_card_or_rank = std::disjunction<is_card<T>, is_rank<T>>;
        template<typename T>
        inline const bool is_card_or_rank_v = is_card_or_rank<T>::value;

        namespace v1 {
            template<typename T, bool allow_duplicates, bool is_auto_ordered, std::size_t N, std::enable_if_t<is_card_or_rank_v<T>, int> = 0>
            class hand_helper {
                static_assert(N
                >= 2 || N <= 4, "for now, only handsizes of 2 <= N <= 4 are supported");

                using c_r_type = T;
                static const auto char_count = is_card_v<c_r_type> ? 2 : 1;

                template<std::size_t... I>
                [[nodiscard]]uint64_t as_bitset_impl(std::index_sequence<I...>) const noexcept {
                    return (m_arr[I].as_bitset() | ...);
                }

            public:
                std::array <T, N> m_arr;

                hand_helper() = default;

                template<std::enable_if_t<N == 2, int> = 0>
                hand_helper(const c_r_type c1, const c_r_type c2) noexcept(allow_duplicates): m_arr({c1, c2}) {
                        if (!allow_duplicates) {
                            if (c1 == c2) {
                                throw std::runtime_error(
                                        "hand(const crt, const crt): tried to create hand with equal input (no duplicates allowed): " +
                                        c1.str() +
                                        c2.str());
                            }
                        }
                }

                template<std::enable_if_t<is_card_v<T> && N == 2, int> = 0>
                hand_helper(const uint8_t i1, const uint8_t i2) : hand_helper(c_r_type(i1), c_r_type(i2)) {}

                template<std::enable_if_t<N == 2, int> = 0>
                explicit hand_helper(const std::string_view str)
                        : hand_helper(c_r_type{str.substr(0 * char_count, char_count)},
                                      c_r_type{str.substr(1 * char_count, char_count)}) {
                    if (str.size() != 2 * char_count) {
                        throw std::runtime_error(
                                std::string(
                                        "hand(const string_view): tried to create a hand with a string of wrong size: '").append(
                                        str) + "'");
                    }
                }

                template<typename Indices = std::make_index_sequence <N>>
                [[nodiscard]] auto as_bitset() const noexcept {
                    return as_bitset_impl(Indices{});
                }

                template<typename U = c_r_type, std::enable_if_t<is_card_v<U>, int> = 0>
                [[nodiscard]] cardset as_cardset() const noexcept {
                    return cardset(m_arr);
                }

                template<std::enable_if_t<N == 2, int> = 0>
                [[nodiscard]] std::string str() const noexcept {
                    return std::string(m_arr.front().str() + m_arr.back().str());
                }

                operator std::string() {
                    return str();
                }

                auto operator<=>(const hand_helper &) const noexcept = default;
            };
        }    // namespace v1

        using hand_2c = v1::hand_helper<card, false, true, 2>;

    } // namespace poker
} // namespace like

#endif //POKER_HAND_HPP
