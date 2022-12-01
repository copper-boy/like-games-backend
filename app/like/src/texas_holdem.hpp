//
// Created by deded on 8/3/22.
//

#ifndef LIKE_TEXAS_HOLDEM_HPP
#define LIKE_TEXAS_HOLDEM_HPP

#include "data_structure.hpp"
#include "utils.hpp"

#include <drogon/drogon.h>

#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace like {
namespace poker {
namespace net {
namespace http {
namespace holdem {
auto holdem_evaluator_router(
    const drogon::HttpRequestPtr &request,
    std::function<void(const drogon::HttpResponsePtr &)> &&callback) -> void {
  auto request_json = glz::read_json<data_structures::evaluator_request_schema>(
      request->body());
  data_structures::evaluator_response_schema response_json;

  for (auto const &result : utils::holdem::side_pot_winners(
           game::holdem::gamecards(request_json.board, request_json.hands),
           utils::generator(request_json.hands.size()))) {
    response_json.detail.winners.push_back(
        std::move(data_structures::hand_schema{
            .id = result.second, .hand = result.first.str_long()}));
  }

  auto response = drogon::HttpResponse::newHttpResponse();
  response->setContentTypeCode(drogon::ContentType::CT_APPLICATION_JSON);
  response->setBody(glz::write_json(response_json));

  callback(response);
}

auto holdem_equity_router(
    const drogon::HttpRequestPtr &request,
    std::function<void(const drogon::HttpResponsePtr &)> &&callback) -> void {
  auto request_json =
      glz::read_json<data_structures::equities_request_schema>(request->body());
  data_structures::equities_response_schema response_json;

  for (auto const &win : utils::holdem::wins_in_percentages(
           poker::evaluator::holdem::calculate_equities(request_json.hands,
                                                        request_json.board))) {
    response_json.detail.winners.push_back(
        std::move(data_structures::equities_result_schema{.id = win.first,
                                                          .wins = win.second}));
  }
  auto response = drogon::HttpResponse::newHttpResponse();
  response->setContentTypeCode(drogon::ContentType::CT_APPLICATION_JSON);
  response->setBody(glz::write_json(response_json));

  callback(response);
}
} // namespace holdem
} // namespace http
} // namespace net
} // namespace poker
} // namespace like

#endif // LIKE_TEXAS_HOLDEM_HPP
