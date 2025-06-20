#version 330 core

in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D textTexture;

void main()
{
    vec4 texColor = texture(textTexture, TexCoord);
    
    // Se o pixel for transparente, descartar
    if(texColor.a < 0.1)
        discard;
    
    FragColor = texColor;
} 