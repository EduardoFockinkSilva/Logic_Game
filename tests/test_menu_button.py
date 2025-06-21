import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from src.components.menu_button import MenuButton

WIDTH, HEIGHT = 800, 600

def test_callback():
    """Callback de teste para o botão."""
    print("Botão clicado!")

def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Teste Final - MenuButton")

    glViewport(0, 0, WIDTH, HEIGHT)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Criar botão de teste
    button = MenuButton(
        text="Test Button",
        position=(300, 250),
        size=(200, 50),
        color=(100, 150, 255),
        hover_color=(150, 200, 255),
        window_size=(WIDTH, HEIGHT),
        callback=test_callback
    )
    button.initialize()

    print("=== TESTE FINAL ===")
    print(f"Botão criado na posição: {button.position}")
    print(f"Área clicável: ({button.position[0]}, {button.position[1]}) até ({button.position[0] + button.size[0]}, {button.position[1] + button.size[1]})")
    print("Mova o mouse sobre o botão e clique para testar!")
    print("Pressione ESC para sair")
    print("==================")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
            # Passar eventos do mouse para o botão
            button.handle_mouse_event(event)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        button.render(None)
        pygame.display.flip()
        pygame.time.wait(10)

    button.destroy()
    pygame.quit()

if __name__ == "__main__":
    main() 