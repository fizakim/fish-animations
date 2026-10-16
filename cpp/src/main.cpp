#include "obj.h"

int main() {
    std::string path = OBJECTS_DIR "/shark.obj";
    int length = 2;
    int side = 0;
    auto amp = [](float t) { return 2 * t * t; };
    float freq = 0.5;
    float wl = 1;
    bool show_spine = true;

    Obj fish(path, length, side, amp, freq, wl);
    fish.view_animation(show_spine);
}
