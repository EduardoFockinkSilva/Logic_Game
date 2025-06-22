"""
Motor principal do jogo
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List, Dict, Any, Optional
import time

from src.components.core.base_component import Component
from src.components.ui.debug_hud import DebugHUD
from src.components.core.connection_manager import ConnectionManager
from ..shaders.shader_manager import ShaderManager


class GameEngine:
    """Motor principal do jogo - gerencia loop, renderização e componentes"""
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "Puzzle Lógico"):
        self.width = width
        self.height = height
        self.title = title
        self.running = False
        
        # Componentes do jogo
        self.components: List[Component] = []
        self.debug_hud = None
        self.shader_manager = ShaderManager()
        self.connection_manager = ConnectionManager(
            window_size=(width, height),
            shader_manager=self.shader_manager
        )
        self.level_manager = None
        
        # Tempo
        self.last_time = 0.0
        self.delta_time = 0.0
        self.display = None
    
    def initialize(self) -> None:
        """Inicializa Pygame, OpenGL e componentes"""
        pygame.init()
        
        # Configurar display OpenGL
        self.display = pygame.display.set_mode(
            (self.width, self.height), 
            DOUBLEBUF | OPENGL
        )
        pygame.display.set_caption(self.title)
        
        # Configurar OpenGL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Criar HUD de debug
        self.debug_hud = DebugHUD(
            window_size=(self.width, self.height),
            shader_manager=self.shader_manager
        )
        self.add_component(self.debug_hud)
        
        # Inicializar componentes
        for component in self.components:
            component.initialize()
    
    def add_component(self, component: Component) -> None:
        """Adiciona componente ao jogo"""
        self.components.append(component)
        
        # Adicionar ao gerenciador de conexões se for componente lógico
        if hasattr(component, 'get_result') or hasattr(component, 'get_state'):
            self.connection_manager.add_component(component)
        
        if self.running:
            component.initialize()
    
    def remove_component(self, component: Component) -> None:
        """Remove componente do jogo"""
        if component in self.components:
            self.connection_manager.remove_component(component)
            component.destroy()
            self.components.remove(component)
    
    def set_level_manager(self, level_manager) -> None:
        """Define gerenciador de níveis"""
        self.level_manager = level_manager
    
    def clear_components(self) -> None:
        """Remove todos os componentes"""
        self.connection_manager.clear_all_connections()
        
        for component in self.components:
            component.destroy()
        self.components.clear()
    
    def update(self) -> None:
        """Atualiza componentes e conexões"""
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
        
        for component in self.components:
            component.update(self.delta_time)
        
        self.connection_manager.update(self.delta_time)
        
        # Verificar conclusão do nível
        if self.level_manager:
            self.level_manager.add_completion_button()
    
    def render(self) -> None:
        """Renderiza componentes e conexões"""
        glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
        glViewport(0, 0, self.width, self.height)
        
        # Renderizar componentes
        for component in self.components:
            component.render(self)
        
        # Renderizar conexões por último
        self.connection_manager.render(self)
        
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """Processa eventos do Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F1:
                    # Alternar HUD de debug
                    if self.debug_hud:
                        self.debug_hud.toggle()
                        print(f"HUD de debug {'ativado' if self.debug_hud.enabled else 'desativado'}")
                elif event.key == pygame.K_F2:
                    # Mostrar informações das conexões
                    connection_count = self.connection_manager.get_connection_count()
                    print(f"Total de conexões: {connection_count}")
            
            # Passar eventos do mouse para componentes
            for component in self.components:
                mouse_handler = getattr(component, 'handle_mouse_event', None)
                if mouse_handler is not None:
                    mouse_handler(event)
        
        return True
    
    def run(self) -> None:
        """Executa loop principal do jogo"""
        self.initialize()
        self.running = True
        self.last_time = time.time()
        
        print(f"Jogo iniciado: {self.title}")
        print("ESC: Sair | F1: Debug HUD | F2: Info conexões")
        
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.render()
            pygame.time.wait(10)
        
        self.cleanup()
    
    def cleanup(self) -> None:
        """Limpa recursos do jogo"""
        print("Limpando recursos...")
        
        self.connection_manager.clear_all_connections()
        
        for component in self.components:
            component.destroy()
        
        pygame.quit()
        print("Jogo finalizado.")
    
    def get_shader_manager(self) -> ShaderManager:
        """Retorna gerenciador de shaders"""
        return self.shader_manager
    
    def get_debug_hud(self) -> Optional[DebugHUD]:
        """Retorna HUD de debug"""
        return self.debug_hud
    
    def get_connection_manager(self) -> ConnectionManager:
        """Retorna gerenciador de conexões"""
        return self.connection_manager 