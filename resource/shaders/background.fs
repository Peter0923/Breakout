#version 330 core

in vec2 TexCoords;

uniform vec3 color;

out vec4 FragColor;

uniform sampler2D image;

void main(){
    FragColor = vec4(color, 1.0) * texture(image, TexCoords);
}