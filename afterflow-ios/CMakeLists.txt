cmake_minimum_required(VERSION 3.29)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Select the device architecture before enabling the Apple toolchain.
if (CMAKE_SYSTEM_NAME STREQUAL "iOS" OR IOS OR GEODE_TARGET_PLATFORM STREQUAL "iOS")
    set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Device architecture" FORCE)
elseif (CMAKE_HOST_APPLE)
    set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "Mac architectures")
endif()
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
project(Afterflow VERSION 2.1.6 LANGUAGES C CXX)

if (NOT CMAKE_SYSTEM_NAME STREQUAL "iOS" AND NOT GEODE_TARGET_PLATFORM STREQUAL "iOS")
    message(FATAL_ERROR "This port targets iOS. Configure with -DCMAKE_SYSTEM_NAME=iOS -DGEODE_TARGET_PLATFORM=iOS")
endif()
if (NOT DEFINED ENV{GEODE_SDK})
    message(FATAL_ERROR "Set GEODE_SDK to the Geode 5.11.2 SDK directory")
endif()
add_library(${PROJECT_NAME} SHARED src/main.cpp)
add_subdirectory("$ENV{GEODE_SDK}" "${CMAKE_CURRENT_BINARY_DIR}/geode")
setup_geode_mod(${PROJECT_NAME})

# The pinned bindings generate global FMOD C wrappers before their per-class
# includes. Supply the SDK's matching C declarations to that generated target.
# This does not alter addresses, ABI, or the SDK headers.
if (TARGET GeodeBindings)
    target_compile_options(GeodeBindings PRIVATE
        -include "$ENV{GEODE_SDK}/loader/include/Geode/fmod/fmod.h")
endif()
