cmake_minimum_required(VERSION 3.5)
project(like CXX)

set(CMAKE_CXX_STANDARD 23)

add_executable(${PROJECT_NAME} src/main.cpp)

include(cmake/CPM.cmake)

CPMAddPackage(
        NAME glaze
        GITHUB_REPOSITORY stephenberry/glaze
        GIT_TAG main
)

CPMAddPackage(
        NAME drogon
        VERSION 1.8.1
        GITHUB_REPOSITORY drogonframework/drogon
        GIT_TAG v1.8.1
)

target_link_libraries(${PROJECT_NAME} PRIVATE glaze drogon)
