#version 330 core

in vec4 vertex;   // <vec2 position, vec2 texcoords>
in vec2 offset;  // 将offset作为一个顶点属性
in vec4 color;   // 将color作为一个顶点属性

out vec2 TexCoords;
out vec4 ParticleColor;
uniform float scale;

uniform mat4 projection;

void main(){
    TexCoords = vertex.zw;
    ParticleColor = color;
    gl_Position = projection * vec4(vertex.xy * scale + offset, 0.0f, 1.0f);
}