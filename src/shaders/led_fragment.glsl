#version 330 core

in vec2 TexCoord;
in vec4 Color;
out vec4 FragColor;

void main()
{
    // Create a perfect circle
    vec2 center = vec2(0.5, 0.5);
    vec2 pos = TexCoord - center;
    
    // Calculate distance from center
    float distance = length(pos);
    
    // Create circle effect with smooth edges
    float radius = 0.45;
    float smoothness = 0.05;
    
    // Smooth circle function
    float circle = smoothstep(radius + smoothness, radius - smoothness, distance);
    
    // Use the color from vertex shader
    FragColor = vec4(Color.rgb, Color.a * circle);
} 