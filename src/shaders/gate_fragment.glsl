#version 330 core

in vec2 TexCoord;
in vec4 Color;
out vec4 FragColor;

void main()
{
    // Create a rectangular gate with rounded corners
    vec2 center = vec2(0.5, 0.5);
    vec2 pos = TexCoord - center;
    
    // Calculate distance from center
    float distance = length(pos);
    
    // Create rounded rectangle effect
    float radius = 0.4;
    float smoothness = 0.05;
    
    // Smooth rounded rectangle function
    float gate = smoothstep(radius + smoothness, radius - smoothness, distance);
    
    // Use the color from vertex shader
    FragColor = vec4(Color.rgb, Color.a * gate);
} 