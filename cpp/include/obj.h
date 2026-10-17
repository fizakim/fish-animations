#pragma once

#include <array>
#include <functional>
#include <string>
#include <vector>

using Vec = std::array<float, 3>;
using Line = std::vector<Vec>;

class Obj {
public:
    Obj(std::string path, int length = 0, int side = 2, std::function<float(float)> amp = [](float t) { return 0.3f * t * t; }, float freq = 1, float wl = 1, std::string skin = "");

    Line swim(float time);
    std::vector<Line> spine(float time, int n = 50);
    void view_animation(bool show_spine = false);

private:
    int length, side;
    std::function<float(float)> amp;
    float freq, wl, lo, hi;
    std::string skin;
    Line verts;
    std::vector<std::vector<int>> faces;
    std::vector<std::vector<int>> face_tex;
    std::vector<std::array<float, 2>> tex;
};
