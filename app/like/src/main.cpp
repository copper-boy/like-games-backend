//
// Created by deded on 5/1/22.
//

#include "texas_holdem.hpp"

#include <drogon/drogon.h>

auto main() -> int {
  drogon::app().registerHandler(
      "/api.like/holdem/evaluator",
      &like::poker::net::http::holdem::holdem_evaluator_router, {drogon::Post});
  drogon::app()
      .setLogLevel(trantor::Logger::kInfo)
      .addListener("0.0.0.0", 8080)
      .setThreadNum(0) // all threads used
      .run();
}
