#version 330 core

in vec2 TexCoord;
out vec4 FragColor;

uniform float uTime;
uniform vec2 uResolution;

void main()
{
    // Normalizar coordenadas
    vec2 uv = TexCoord;
    
    // Criar gradiente animado
    float time = uTime * 0.5;
    
    // Gradiente radial com movimento
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(uv, center);
    
    // Cores do gradiente
    vec3 color1 = vec3(0.1, 0.2, 0.4);  // Azul escuro
    vec3 color2 = vec3(0.3, 0.1, 0.6);  // Roxo
    vec3 color3 = vec3(0.6, 0.2, 0.8);  // Roxo claro
    
    // Animação do gradiente
    float wave1 = sin(dist * 10.0 - time * 2.0) * 0.5 + 0.5;
    float wave2 = sin(dist * 15.0 - time * 1.5) * 0.5 + 0.5;
    
    // Misturar cores baseado na distância e tempo
    vec3 finalColor = mix(color1, color2, wave1);
    finalColor = mix(finalColor, color3, wave2);
    
    // Adicionar brilho no centro
    float glow = 1.0 - dist * 2.0;
    glow = max(0.0, glow);
    finalColor += vec3(0.1, 0.2, 0.3) * glow;
    
    // Adicionar ruído sutil
    float noise = fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);
    finalColor += vec3(noise * 0.05);
    
    FragColor = vec4(finalColor, 1.0);
} 