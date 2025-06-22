#version 330 core

in vec2 TexCoord;
in vec4 Color;
out vec4 FragColor;

void main()
{
    // Círculo perfeito
    vec2 center = vec2(0.5, 0.5);
    vec2 pos = TexCoord - center;
    float distance = length(pos);
    
    // Círculo com bordas suaves
    float radius = 0.45;
    float smoothness = 0.05;
    float circle = smoothstep(radius + smoothness, radius - smoothness, distance);
    
    FragColor = vec4(Color.rgb, Color.a * circle);
} 