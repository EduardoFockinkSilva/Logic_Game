import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from src.components.text_component import TextComponent

WIDTH, HEIGHT = 800, 600

def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Teste de Texto OpenGL")

    glViewport(0, 0, WIDTH, HEIGHT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    text = TextComponent(
        text="Logic Game",
        font_size=48,
        color=(255,255,255),
        position=(0.5, 0.05),
        window_size=(WIDTH, HEIGHT)
    )
    text.initialize()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        text.render(None)
        pygame.display.flip()
        pygame.time.wait(10)

    text.destroy()
    pygame.quit()

if __name__ == "__main__":
    main() 