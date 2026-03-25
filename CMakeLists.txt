cmake_minimum_required(VERSION 3.30)
project(allpay_solver)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

add_executable(allpay_solver
    src/main.cpp
    src/game.cpp
    src/solver.cpp
    src/games.cpp
)

target_include_directories(allpay_solver PRIVATE include)
