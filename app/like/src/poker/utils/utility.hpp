//
// Created by deded on 16.04.22.
//

#ifndef POKER_UTILITY_HPP
#define POKER_UTILITY_HPP

namespace like {
    namespace poker {
#ifdef __GNUC__
        [[noreturn]] inline __attribute__((always_inline)) void unreachable() {
            __builtin_unreachable();
        }
#elif defined(_MSC_VER)
        [[noreturn]] __forceinline void unreachable() {
            __assume(false);
        }
#else                                                                                                     // ???
        inline void unreachable() {
            // unreachable not supported
        }
#endif
    } // namespace poker
} // namespace like

#endif //POKER_UTILITY_HPP
