#version 330 core

in vec4 vertex;   // <vec2 position, vec2 texcoords>
in vec2 offset;
in vec4 color;

out vec2 TexCoords;
out vec4 ParticleColor;
uniform float scale;

uniform mat4 projection;

void main(){
    TexCoords = vertex.zw;
    ParticleColor = color;
    gl_Position = projection * vec4(vertex.xy * scale + offset, 0.0f, 1.0f);
}