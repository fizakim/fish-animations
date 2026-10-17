#define _USE_MATH_DEFINES
#include "obj.h"

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include <GLFW/glfw3.h>

#include <algorithm>
#include <cmath>
#include <fstream>
#include <sstream>
using namespace std;

Obj::Obj(string path, int length, int side, function<float(float)> amp, float freq, float wl, string skin)
    : length(length), side(side), amp(amp), freq(freq), wl(wl), skin(skin) {
    ifstream file(path);
    string line;
    while (getline(file, line)) {
        istringstream s(line);
        string tag;
        s >> tag;
        if (tag == "vt") {
            array<float, 2> t;
            s >> t[0] >> t[1];
            tex.push_back(t);
        } else if (tag == "v") {
            Vec v;
            s >> v[0] >> v[1] >> v[2];
            verts.push_back(v);
        } else if (tag == "f") {
            vector<int> f, ft;
            string x;
            while (s >> x) {
                f.push_back(stoi(x) - 1);
                ft.push_back(stoi(x.substr(x.find('/') + 1)) - 1);
            }
            faces.push_back(f);
            face_tex.push_back(ft);
        }
    }
    lo = hi = verts[0][length];
    for (auto& v : verts) {
        lo = min(lo, v[length]);
        hi = max(hi, v[length]);
    }
}

Line Obj::swim(float time) {
    Line new_verts = verts;
    for (auto& p : new_verts) {
        float t = (hi - p[length]) / (hi - lo);
        p[side] += amp(t) * sin(2 * M_PI * (t / wl - freq * time));
    }
    return new_verts;
}

vector<Line> Obj::spine(float time, int n) {
    Vec centre;
    for (int i = 0; i < 3; i++) {
        float mn = verts[0][i], mx = verts[0][i];
        for (auto& v : verts) {
            mn = min(mn, v[i]);
            mx = max(mx, v[i]);
        }
        centre[i] = (mn + mx) / 2;
    }
    Line rest, wave, upper, lower;
    for (int i = 0; i <= n; i++) {
        float t = (float)i / n;
        float a = amp(t);
        Vec p = centre;
        p[length] = hi - t * (hi - lo);
        rest.push_back(p);
        p[side] = centre[side] + a;
        upper.push_back(p);
        p[side] = centre[side] - a;
        lower.push_back(p);
        p[side] = centre[side] + a * sin(2 * M_PI * (t / wl - freq * time));
        wave.push_back(p);
    }
    return {rest, wave, upper, lower};
}

void Obj::view_animation(bool show_spine) {
    float r = 0;
    for (auto& v : verts)
        for (float x : v) r = max(r, abs(x));

    glfwInit();
    GLFWwindow* window = glfwCreateWindow(800, 800, "fish", nullptr, nullptr);
    glfwMakeContextCurrent(window);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_LINE_STIPPLE);

    if (skin != "") {
        int w, h, n;
        stbi_set_flip_vertically_on_load(1);
        unsigned char* img = stbi_load(skin.c_str(), &w, &h, &n, 4);
        GLuint id;
        glGenTextures(1, &id);
        glBindTexture(GL_TEXTURE_2D, id);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img);
        stbi_image_free(img);
        glEnable(GL_TEXTURE_2D);
    }

    float colours[4][3] = {{0.5, 0.5, 0.5}, {1, 0, 0}, {0, 0, 1}, {0, 0, 1}};
    float widths[4] = {1, 3, 1, 1};
    int stipples[4] = {0x00FF, 0xFFFF, 0x0101, 0x0101};

    float rotX = 20, rotY = -60;

    while (!glfwWindowShouldClose(window)) {
        if (glfwGetKey(window, GLFW_KEY_LEFT)) rotY -= 2;
        if (glfwGetKey(window, GLFW_KEY_RIGHT)) rotY += 2;
        if (glfwGetKey(window, GLFW_KEY_UP)) rotX -= 2;
        if (glfwGetKey(window, GLFW_KEY_DOWN)) rotX += 2;

        glClearColor(1, 1, 1, 1);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(-2 * r, 2 * r, -2 * r, 2 * r, -4 * r, 4 * r);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        glRotatef(rotX, 1, 0, 0);
        glRotatef(rotY, 0, 1, 0);

        float time = glfwGetTime();
        Line new_verts = swim(time);

        glEnable(GL_POLYGON_OFFSET_FILL);
        glPolygonOffset(1, 1);
        if (skin == "") glColor4f(1, 0.65, 0, show_spine ? 0.3 : 1);
        else glColor3f(1, 1, 1);
        for (int i = 0; i < faces.size(); i++) {
            glBegin(GL_POLYGON);
            for (int j = 0; j < faces[i].size(); j++) {
                if (skin != "") glTexCoord2fv(tex[face_tex[i][j]].data());
                glVertex3fv(new_verts[faces[i][j]].data());
            }
            glEnd();
        }
        glDisable(GL_POLYGON_OFFSET_FILL);

        if (skin == "") {
            glColor3f(0, 0, 0);
            glLineStipple(1, 0xFFFF);
            for (auto& f : faces) {
                glBegin(GL_LINE_LOOP);
                for (int i : f) glVertex3fv(new_verts[i].data());
                glEnd();
            }
        }

        if (show_spine) {
            glDisable(GL_DEPTH_TEST);
            vector<Line> lines = spine(time);
            for (int k = 0; k < 4; k++) {
                glColor3fv(colours[k]);
                glLineWidth(widths[k]);
                glLineStipple(1, stipples[k]);
                glBegin(GL_LINE_STRIP);
                for (auto& p : lines[k]) glVertex3fv(p.data());
                glEnd();
            }
            glLineWidth(1);
            glEnable(GL_DEPTH_TEST);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }
}
