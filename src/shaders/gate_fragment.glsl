#version 330 core

in vec2 TexCoord;
in vec4 Color;
out vec4 FragColor;

void main()
{
    // Porta retangular com cantos arredondados
    vec2 center = vec2(0.5, 0.5);
    vec2 pos = TexCoord - center;
    float distance = length(pos);
    
    // Retângulo arredondado
    float radius = 0.4;
    float smoothness = 0.05;
    float gate = smoothstep(radius + smoothness, radius - smoothness, distance);
    
    FragColor = vec4(Color.rgb, Color.a * gate);
} 