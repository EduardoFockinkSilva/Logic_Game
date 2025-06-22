#!/usr/bin/env python3
"""
Teste das novas configurações de fonte
"""

import pygame
import sys
import os
from OpenGL.GL import *

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.style import ComponentStyle, Colors
from src.components.ui.menu_button import MenuButton
from src.core.shader_manager import ShaderManager

def test_fonts():
    """Testa as novas configurações de fonte"""
    pygame.init()
    
    # Configurar janela
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size, pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Teste de Fontes")
    
    # Inicializar shader manager
    shader_manager = ShaderManager()
    
    # Criar botões de teste com diferentes textos
    buttons = [
        MenuButton("Iniciar Jogo", (250, 200), window_size=window_size, shader_manager=shader_manager),
        MenuButton("Configurações", (250, 280), window_size=window_size, shader_manager=shader_manager),
        MenuButton("Sair", (250, 360), window_size=window_size, shader_manager=shader_manager),
        MenuButton("Teste Longo", (250, 440), window_size=window_size, shader_manager=shader_manager),
    ]
    
    # Inicializar botões
    for button in buttons:
        button._initialize()
    
    clock = pygame.time.Clock()
    running = True
    
    print("Testando novas configurações de fonte:")
    print(f"Tamanho da fonte dos botões: {ComponentStyle.BUTTON_FONT_SIZE}")
    print(f"Tamanho da fonte dos botões de menu: {ComponentStyle.MENU_BUTTON_FONT_SIZE}")
    print(f"Fontes preferidas: {ComponentStyle.PREFERRED_FONTS}")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            # Processar eventos dos botões
            for button in buttons:
                button.handle_mouse_event(event)
        
        # Limpar tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.2, 1.0)
        
        # Renderizar botões
        for button in buttons:
            button._render(None)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Limpar recursos
    for button in buttons:
        button._destroy()
    
    pygame.quit()
    print("Teste concluído!")

if __name__ == "__main__":
    test_fonts() 