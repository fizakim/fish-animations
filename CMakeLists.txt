cmake_minimum_required(VERSION 3.14)
project(fish_movement CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenGL REQUIRED)

# use an installed GLFW if there is one, otherwise download it
find_package(glfw3 QUIET)
if(NOT glfw3_FOUND)
    include(FetchContent)
    FetchContent_Declare(glfw GIT_REPOSITORY https://github.com/glfw/glfw.git GIT_TAG 3.4)
    set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
    set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
    set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(glfw)
endif()

add_executable(fish cpp/src/main.cpp cpp/src/obj.cpp)
target_include_directories(fish PRIVATE cpp/include)
target_link_libraries(fish PRIVATE OpenGL::GL glfw)
target_compile_definitions(fish PRIVATE OBJECTS_DIR="${CMAKE_SOURCE_DIR}/objects")
