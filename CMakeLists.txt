cmake_minimum_required(VERSION 3.30)
project(allpay_solver)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(FetchContent)
FetchContent_Declare(
    highs
    GIT_REPOSITORY https://github.com/ERGO-Code/HiGHS.git
    GIT_TAG v1.14.0
)

set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(highs)

add_library(allpay_lib
    src/lp.cpp
    src/poorman.cpp
    src/richman.cpp
)
target_include_directories(allpay_lib PUBLIC include)
target_link_libraries(allpay_lib PRIVATE highs::highs)

find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module)

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(allpay src/bindings.cpp)

target_link_libraries(allpay PRIVATE allpay_lib)
install(TARGETS allpay LIBRARY DESTINATION .)
install(FILES python/games.py DESTINATION .)
