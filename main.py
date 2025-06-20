#!/usr/bin/env python3
"""
Jogo de Puzzle Lógico com Pygame e OpenGL
Main entry point
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    """Função principal do jogo"""
    print("Iniciando o jogo de Puzzle Lógico...")
    
    # Inicializar Pygame
    pygame.init()
    
    # Configurar display
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Puzzle Lógico - CG Game")
    
    # Configurar OpenGL
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    
    print("Display configurado com sucesso!")
    print("Pressione ESC para sair")
    
    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Limpar buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Renderizar um triângulo simples (teste)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)  # Vermelho
        glVertex3f(-1, -1, 0)
        glColor3f(0.0, 1.0, 0.0)  # Verde
        glVertex3f(1, -1, 0)
        glColor3f(0.0, 0.0, 1.0)  # Azul
        glVertex3f(0, 1, 0)
        glEnd()
        
        # Atualizar display
        pygame.display.flip()
        pygame.time.wait(10)
    
    # Finalizar
    pygame.quit()
    print("Jogo finalizado!")

if __name__ == "__main__":
    main() 