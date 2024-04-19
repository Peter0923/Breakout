#version 330 core

in vec4 vertex;  // <vec2 position, vec2 texcoords>

uniform vec2 pos;
uniform vec2 size;
uniform mat4 projection;

out vec2 TexCoords;

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
    TexCoords = vertex.zw;
}