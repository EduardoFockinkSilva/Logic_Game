"""
HUD de debug para informações de desenvolvimento
"""

import pygame
from src.components.core.base_component import Component
from src.components.ui.text_component import TextComponent


class DebugHUD(Component):
    """HUD de debug - mostra posição do mouse, FPS e outras informações"""
    
    def __init__(self, window_size=(800, 600), enabled=True, shader_manager=None):
        """Inicializa HUD de debug"""
        super().__init__()
        self.window_size = window_size
        self.enabled = enabled
        self.shader_manager = shader_manager
        
        # Componentes de texto
        self.mouse_pos_text = None
        self.fps_text = None
        
        # Dados de debug
        self.mouse_pos = (0, 0)
        self.fps = 0
        self.frame_count = 0
        self.last_fps_update = 0
        
        # Configurações
        self.font_size = 16
        self.text_color = (255, 255, 0)  # Amarelo para debug
        self.update_interval = 0.1  # Atualizar FPS a cada 100ms
    
    def _initialize(self):
        """Inicializa componentes de texto do HUD"""
        # Componente para posição do mouse
        self.mouse_pos_text = TextComponent(
            text="Mouse: (0, 0)",
            font_size=self.font_size,
            color=self.text_color,
            position=(0.02, 0.95),  # Canto superior esquerdo
            window_size=self.window_size,
            shader_manager=self.shader_manager,
            centered=False
        )
        
        # Componente para FPS
        self.fps_text = TextComponent(
            text="FPS: 0",
            font_size=self.font_size,
            color=self.text_color,
            position=(0.02, 0.92),  # Logo abaixo da posição do mouse
            window_size=self.window_size,
            shader_manager=self.shader_manager,
            centered=False
        )
        
        # Inicializar componentes
        self.mouse_pos_text.initialize()
        self.fps_text.initialize()
    
    def _update(self, delta_time):
        """Atualiza informações de debug"""
        if not self.enabled:
            return
        
        # Atualizar posição do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.mouse_pos = (mouse_x, mouse_y)
        
        # Atualizar texto da posição do mouse
        if self.mouse_pos_text:
            self.mouse_pos_text.text = f"Mouse: ({mouse_x}, {mouse_y})"
        
        # Calcular FPS
        self.frame_count += 1
        self.last_fps_update += delta_time
        
        if self.last_fps_update >= self.update_interval:
            self.fps = int(self.frame_count / self.last_fps_update)
            self.frame_count = 0
            self.last_fps_update = 0
            
            # Atualizar texto do FPS
            if self.fps_text:
                self.fps_text.text = f"FPS: {self.fps}"
        
        # Atualizar componentes de texto
        if self.mouse_pos_text:
            self.mouse_pos_text.update(delta_time)
        if self.fps_text:
            self.fps_text.update(delta_time)
    
    def _render(self, renderer):
        """Renderiza HUD de debug"""
        if not self.enabled:
            return
        
        # Renderizar componentes de texto
        if self.mouse_pos_text:
            self.mouse_pos_text.render(renderer)
        if self.fps_text:
            self.fps_text.render(renderer)
    
    def _destroy(self):
        """Destrói componentes do HUD"""
        if self.mouse_pos_text:
            self.mouse_pos_text.destroy()
        if self.fps_text:
            self.fps_text.destroy()
    
    def toggle(self):
        """Alterna visibilidade do HUD"""
        self.enabled = not self.enabled
    
    def set_enabled(self, enabled: bool):
        """Define se HUD está habilitado"""
        self.enabled = enabled
    
    def get_mouse_position(self):
        """Retorna posição atual do mouse"""
        return self.mouse_pos
    
    def get_fps(self):
        """Retorna FPS atual"""
        return self.fps 