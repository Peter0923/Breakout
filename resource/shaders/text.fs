#version 330 core

in vec3 TexCoords;
out vec4 color;

uniform sampler2DArray text4;
uniform vec3 textColor;

void main(){
    color = vec4(textColor, texture(text4, TexCoords).r);
}