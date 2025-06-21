#version 330 core

in vec2 TexCoord;
in vec4 Color;
out vec4 FragColor;

void main()
{
    // Calculate distance from center
    vec2 center = vec2(0.5, 0.5);
    float distance = length(TexCoord - center);
    
    // Create a circle with smooth edges
    float radius = 0.45;
    float smoothness = 0.05;
    
    // Smooth circle function
    float circle = smoothstep(radius + smoothness, radius - smoothness, distance);
    
    // Use the color from vertex shader
    FragColor = vec4(Color.rgb, Color.a * circle);
} 