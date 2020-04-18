#version 440

in vec2 in_vert;
in vec3 in_color;

out vec3 v_color;

uniform float height;
uniform float width;

mat4 view() {
    return mat4(
        height/width, 0.0, 0.0, 0.0,
        0.0, width/height, 0.0, 0.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 0.0, 1.0
    );
}

void main() {
    v_color = in_color;
    gl_Position = view() * vec4(in_vert, 1.0, 1.0);
}
