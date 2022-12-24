//
// Created by deded on 18.04.22.
//

#ifndef POKERLIKE_GAME_HPP
#define POKERLIKE_GAME_HPP

#include "../../card/card.hpp"
#include "../../card/cardset.hpp"
#include "../../card/hand.hpp"
#include "../../evaluator/holdem/holdem_evaluation.hpp"

#include <set>            //
#include <span>           //
#include <utility>        // std::pair, std::get

namespace like {
    namespace poker {
        namespace game {
            namespace holdem {
                using namespace poker::evaluator::holdem;

                class gamecards {
                public:
                    std::vector <card> m_board;
                    std::vector <hand_2c> m_hands;

                    // create with matching arrays
                    explicit gamecards(std::vector <std::string> const& board,
                                       std::vector <std::string> const& hands) :
                            m_board(board.begin(), board.end()), m_hands(hands.begin(), hands.end()) {
                        if (m_board.size() + m_hands.size() !=
                            std::set(m_board.cbegin(), m_board.cend()).size() +
                            std::set(m_hands.cbegin(), m_hands.cend()).size()) {
                            throw std::logic_error("Cards not unique");
                        }
                    }

                    // provide operator for equality
                    auto operator<=>(const gamecards &) const noexcept = delete;

                    bool operator==(const gamecards &) const noexcept = default;
                };
            } // namespace holdem
        } // namespace game
    } // namespace poker
} // namespace like

#endif //POKERLIKE_GAME_HPP
