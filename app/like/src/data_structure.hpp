
//
// Created by deded on 10/20/22.
//

#ifndef POKER_MICROSERVICES_DATA_STRUCTURE_HPP
#define POKER_MICROSERVICES_DATA_STRUCTURE_HPP

#include "poker/card/card.hpp"
#include "poker/card/hand.hpp"

#include "glaze/glaze.hpp"

#include <array>
#include <cstdint>
#include <string>
#include <vector>

namespace like {
namespace data_structures {
struct evaluator_request_schema {
  std::vector<std::string> hands;
  std::vector<std::string> board;

  struct glaze {
    using T = evaluator_request_schema;

    static constexpr auto value =
        glz::object("hands", &T::hands, "board", &T::board);
  };
};

struct hand_schema {
  uint64_t id;
  std::string hand;

  struct glaze {
    using T = hand_schema;

    static constexpr auto value = glz::object("id", &T::id, "hand", &T::hand);
  };
};

struct evaluator_response_schema_detail {
  std::vector<hand_schema> winners;

  struct glaze {
    using T = evaluator_response_schema_detail;

    static constexpr auto value = glz::object("winners", &T::winners);
  };
};

struct evaluator_response_schema {
  bool ok = true;
  evaluator_response_schema_detail detail;

  struct glaze {
    using T = evaluator_response_schema;

    static constexpr auto value =
        glz::object("ok", &T::ok, "detail", &T::detail);
  };
};

struct equities_request_schema {
  std::vector<std::string> hands;
  std::vector<std::string> board = {};

  struct glaze {
    using T = equities_request_schema;

    static constexpr auto value =
        glz::object("hands", &T::hands, "board", &T::board);
  };
};

struct equities_result_schema {
  uint64_t id;
  std::string wins;

  struct glaze {
    using T = equities_result_schema;

    static constexpr auto value = glz::object("id", &T::id, "wins", &T::wins);
  };
};

struct equities_response_schema_detail {
  std::vector<equities_result_schema> winners;

  struct glaze {
    using T = equities_response_schema_detail;

    static constexpr auto value = glz::object("winners", &T::winners);
  };
};

struct equities_response_schema {
  bool ok = true;
  equities_response_schema_detail detail;

  struct glaze {
    using T = equities_response_schema;

    static constexpr auto value =
        glz::object("ok", &T::ok, "detail", &T::detail);
  };
};
} // namespace data_structures
} // namespace like

#endif // POKER_MICROSERVICES_DATA_STRUCTURE_HPP
