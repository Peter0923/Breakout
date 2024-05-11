#version 330 core

in vec4 in_vert;
out vec2 TexCoords;

uniform bool confuse;
uniform bool chaos;
uniform bool shake;

uniform float time;

void main(){
    gl_Position = vec4(in_vert.xy, 0.0, 1.0);
    TexCoords = in_vert.zw;

    if(confuse){
        TexCoords = vec2(1.0-in_vert.z, 1.0-in_vert.w);
    }else if(chaos){
        float strength = 0.1;
        TexCoords = vec2(TexCoords.x+sin(time)*strength, TexCoords.y+cos(time)*strength);
    }

    if(shake){
        float strength = 0.005;
        gl_Position.x += cos(time * 10) * strength;
        gl_Position.y += cos(time * 15) * strength;
    }   
}