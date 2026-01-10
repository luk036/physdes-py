cmake_minimum_required(VERSION 3.20)
project(physdes-cpp VERSION 0.1.0 LANGUAGES CXX)

# Set C++ standard to C++23
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Options
option(BUILD_TESTS "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" OFF)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Library target (header-only)
add_library(physdes INTERFACE)
target_include_directories(physdes INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Tests
if(BUILD_TESTS)
    enable_testing()

    # Find doctest
    find_package(doctest QUIET)
    if(NOT doctest_FOUND)
        message(STATUS "doctest not found, downloading...")
        include(FetchContent)
        FetchContent_Declare(
            doctest
            GIT_REPOSITORY https://github.com/doctest/doctest.git
            GIT_TAG v2.4.11
        )
        FetchContent_MakeAvailable(doctest)
    endif()

    # Add test executable
    add_executable(physdes_tests tests/main.cpp)
    target_link_libraries(physdes_tests PRIVATE physdes doctest::doctest)

    add_test(NAME physdes_tests COMMAND physdes_tests)
endif()

# Examples
if(BUILD_EXAMPLES)
    add_executable(example_interval src/example_interval.cpp)
    target_link_libraries(example_interval PRIVATE physdes)
endif()

# Install target
install(DIRECTORY include/ DESTINATION include)
install(TARGETS physdes EXPORT physdes-targets)
install(EXPORT physdes-targets DESTINATION lib/cmake/physdes)
