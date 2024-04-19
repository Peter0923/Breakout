#version 330 core

in vec4 vertex;  // <vec2 position, vec2 texcoords>
in vec2 pos;
in vec2 size;
in vec3 color;
in vec3 layer;

uniform mat4 projection;

out vec3 TexCoords;
out vec3 spriteColor;

void main(){
    mat4 scale = mat4(size.x, 0, 0, 0,
                      0, size.y, 0, 0,
                      0, 0, 1, 0,
                      0, 0, 0, 1);
    mat4 translate = mat4(1, 0, 0, 0,
                          0, 1, 0, 0,
                          0, 0, 1, 0,
                          pos.x, pos.y, 0, 1);
    gl_Position = projection * translate * scale * vec4(vertex.xy, 0.0, 1.0);
    TexCoords = vec3(vertex.zw, 1.0) * layer;
    spriteColor = color;
}