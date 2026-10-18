#include "obj.h"

int main() {
    std::string path = OBJECTS_DIR "/shark.obj";
    int length = 2;
    int side = 0;
    auto amp = [](float t) { return 2*t*t ; };
    float freq = 3;
    float wl = 1;
    std::string skin = "skins/shark.png";
    bool show_spine = false;

    Obj fish(path, length, side, amp, freq, wl, skin);
    fish.view_animation(show_spine);
}
