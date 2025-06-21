"""
Motor principal do jogo
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List, Dict, Any, Optional
import time

from ..components.base_component import Component
from ..components.debug_hud import DebugHUD
from ..shaders.shader_manager import ShaderManager


class GameEngine:
    """
    Motor principal do jogo que gerencia o loop principal,
    renderização e componentes.
    """
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "Puzzle Lógico"):
        """
        Inicializa o motor do jogo.
        
        Args:
            width: Largura da janela
            height: Altura da janela
            title: Título da janela
        """
        self.width = width
        self.height = height
        self.title = title
        self.running = False
        
        # Componentes do jogo
        self.components: List[Component] = []
        
        # HUD de debug
        self.debug_hud = None
        
        # Gerenciador de shaders
        self.shader_manager = ShaderManager()
        
        # Tempo
        self.last_time = 0.0
        self.delta_time = 0.0
        
        # Display Pygame
        self.display = None
    
    def initialize(self) -> None:
        """Inicializa o motor do jogo."""
        # Inicializar Pygame
        pygame.init()
        
        # Configurar display com OpenGL moderno
        self.display = pygame.display.set_mode(
            (self.width, self.height), 
            DOUBLEBUF | OPENGL
        )
        pygame.display.set_caption(self.title)
        
        # Configurar OpenGL moderno
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Criar e adicionar HUD de debug
        self.debug_hud = DebugHUD(
            window_size=(self.width, self.height),
            shader_manager=self.shader_manager
        )
        self.add_component(self.debug_hud)
        
        # Inicializar componentes
        for component in self.components:
            component.initialize()
    
    def add_component(self, component: Component) -> None:
        """
        Adiciona um componente ao jogo.
        
        Args:
            component: Componente a ser adicionado
        """
        self.components.append(component)
        if self.running:
            component.initialize()
    
    def remove_component(self, component: Component) -> None:
        """
        Remove um componente do jogo.
        
        Args:
            component: Componente a ser removido
        """
        if component in self.components:
            component.destroy()
            self.components.remove(component)
    
    def clear_components(self) -> None:
        """
        Remove todos os componentes do jogo.
        """
        for component in self.components:
            component.destroy()
        self.components.clear()
    
    def update(self) -> None:
        """Atualiza todos os componentes."""
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
        
        for component in self.components:
            component.update(self.delta_time)
    
    def render(self) -> None:
        """Renderiza todos os componentes."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Configurar viewport para renderização
        glViewport(0, 0, self.width, self.height)
        
        for component in self.components:
            component.render(self)
        
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """
        Processa eventos do Pygame.
        
        Returns:
            True se o jogo deve continuar, False para sair
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F1:
                    # Alternar HUD de debug com F1
                    if self.debug_hud:
                        self.debug_hud.toggle()
                        print(f"HUD de debug {'ativado' if self.debug_hud.enabled else 'desativado'}")
            
            # Passar eventos do mouse para componentes que precisam
            for component in self.components:
                mouse_handler = getattr(component, 'handle_mouse_event', None)
                if mouse_handler is not None:
                    mouse_handler(event)
        
        return True
    
    def run(self) -> None:
        """Executa o loop principal do jogo."""
        self.initialize()
        self.running = True
        self.last_time = time.time()
        
        print(f"Jogo iniciado: {self.title}")
        print("Pressione ESC para sair")
        print("Pressione F1 para alternar o HUD de debug")
        
        while self.running:
            # Processar eventos
            self.running = self.handle_events()
            
            # Atualizar
            self.update()
            
            # Renderizar
            self.render()
            
            # Controlar FPS
            pygame.time.wait(10)
        
        self.cleanup()
    
    def cleanup(self) -> None:
        """Limpa recursos do jogo."""
        print("Finalizando jogo...")
        
        # Destruir componentes
        for component in self.components:
            component.destroy()
        
        # Limpar shaders
        self.shader_manager.cleanup()
        
        # Finalizar Pygame
        pygame.quit()
        
        print("Jogo finalizado!")
    
    def get_shader_manager(self) -> ShaderManager:
        """Retorna o gerenciador de shaders."""
        return self.shader_manager
    
    def get_debug_hud(self) -> Optional[DebugHUD]:
        """Retorna o HUD de debug."""
        return self.debug_hud 