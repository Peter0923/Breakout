#version 330 core

in vec3 TexCoords;
in vec3 spriteColor;

out vec4 FragColor;

uniform sampler2DArray image;

void main(){
    FragColor = vec4(spriteColor, 1.0) * texture(image, TexCoords);
}