cmake_minimum_required(VERSION 3.30)
project(allpay_solver)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(allpay_lib
    src/solver.cpp
    src/games.cpp
)
target_include_directories(allpay_lib PUBLIC include)
set_target_properties(allpay_lib PROPERTIES POSITION_INDEPENDENT_CODE ON)

add_executable(allpay_solver src/main.cpp)
target_link_libraries(allpay_solver PRIVATE allpay_lib)

find_package(Python 3.8 REQUIRED COMPONENTS Interpreter Development.Module)

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(allpay src/bindings.cpp)

target_link_libraries(allpay PRIVATE allpay_lib)
install(TARGETS allpay LIBRARY DESTINATION .)
