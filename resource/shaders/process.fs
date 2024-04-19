#version 330 core

in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D scene;

uniform vec2 offsets[9];
uniform float blur_kernel[9];
uniform int edge_kernel[9];

uniform bool confuse;
uniform bool chaos;
uniform bool shake;

void main(){
    vec3 sample[9];
    FragColor = vec4(0.0f);

    if(chaos || shake)
        for(int i=0; i<9; ++i)
            sample[i] = texture(scene, TexCoords+offsets[i]).rgb;
    
    if(confuse)
        FragColor = vec4(1.0 - texture(scene, TexCoords).rgb, 1.0);
    else if(chaos){
        for(int i=0; i<9; ++i)
            FragColor += vec4(sample[i]*edge_kernel[i], 0.0f);
        FragColor.a = 1.0f;
    }else if(shake){
        for(int i=0; i<9; ++i)
            FragColor += vec4(sample[i]*blur_kernel[i], 0.0f);
        FragColor.a = 1.0f;
    }else
        FragColor = texture(scene, TexCoords);
}