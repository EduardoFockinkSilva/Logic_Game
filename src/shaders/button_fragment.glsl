#version 330 core

in vec2 TexCoord;
in vec4 Color;
out vec4 FragColor;

void main()
{
    // Distância do centro
    vec2 center = vec2(0.5, 0.5);
    float distance = length(TexCoord - center);
    
    // Círculo com bordas suaves
    float radius = 0.45;
    float smoothness = 0.05;
    float circle = smoothstep(radius + smoothness, radius - smoothness, distance);
    
    FragColor = vec4(Color.rgb, Color.a * circle);
} 