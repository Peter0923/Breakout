#version 330 core

in vec2 vertex;
in vec3 texcoords;

out vec3 TexCoords;

uniform mat4 projection;

void main(){
    gl_Position = projection * vec4(vertex, 0.0, 1.0);
    TexCoords = texcoords;
}