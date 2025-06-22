"""
Componente base para todos os componentes do jogo
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Tuple, List
import numpy as np
import pygame
from OpenGL.GL import *


class Component(ABC):
    """
    Classe base para todos os componentes do jogo.
    Implementa o padrão Component para arquitetura modular.
    """
    
    def __init__(self, entity: Optional[Any] = None):
        """
        Inicializa o componente.
        
        Args:
            entity: Entidade pai que possui este componente
        """
        self.entity = entity
        self.enabled = True
        self._initialized = False
    
    def initialize(self) -> None:
        """Inicializa o componente. Chamado uma vez após a criação."""
        if not self._initialized:
            self._initialize()
            self._initialized = True
    
    @abstractmethod
    def _initialize(self) -> None:
        """Implementação específica da inicialização."""
        pass
    
    def update(self, delta_time: float) -> None:
        """
        Atualiza o componente a cada frame.
        
        Args:
            delta_time: Tempo desde o último frame em segundos
        """
        if self.enabled and self._initialized:
            self._update(delta_time)
    
    def _update(self, delta_time: float) -> None:
        """Implementação específica da atualização."""
        pass
    
    def render(self, renderer: Any) -> None:
        """
        Renderiza o componente.
        
        Args:
            renderer: Renderizador OpenGL
        """
        if self.enabled and self._initialized:
            self._render(renderer)
    
    def _render(self, renderer: Any) -> None:
        """Implementação específica da renderização."""
        pass
    
    def destroy(self) -> None:
        """Destrói o componente e libera recursos."""
        if self._initialized:
            self._destroy()
            self._initialized = False
    
    def _destroy(self) -> None:
        """Implementação específica da destruição."""
        pass


class RenderableComponent(Component):
    """
    Componente base para elementos renderizáveis com OpenGL.
    Fornece funcionalidades comuns para renderização.
    """
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        super().__init__()
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.renderer = None
        self.shader_ok = False
    
    def _setup_gl_state(self):
        """Configura o estado OpenGL para renderização 2D."""
        self.prev_viewport = glGetIntegerv(GL_VIEWPORT)
        self.prev_blend = glIsEnabled(GL_BLEND)
        self.prev_depth_test = glIsEnabled(GL_DEPTH_TEST)
        
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
    
    def _restore_gl_state(self):
        """Restaura o estado OpenGL anterior."""
        glViewport(*self.prev_viewport)
        if self.prev_blend:
            glEnable(GL_BLEND)
        else:
            glDisable(GL_BLEND)
        if self.prev_depth_test:
            glEnable(GL_DEPTH_TEST)
        else:
            glDisable(GL_DEPTH_TEST)
    
    def screen_to_gl_coords(self, x: int, y: int, width: int, height: int) -> Tuple[float, float, float, float]:
        """
        Converte coordenadas de tela para coordenadas OpenGL.
        
        Args:
            x, y: Posição em coordenadas de tela
            width, height: Dimensões em coordenadas de tela
            
        Returns:
            Tupla (gl_x, gl_y, gl_width, gl_height) em coordenadas OpenGL
        """
        gl_x = (x / self.window_size[0]) * 2 - 1
        gl_y = 1 - ((y + height) / self.window_size[1]) * 2
        gl_width = (width / self.window_size[0]) * 2
        gl_height = (height / self.window_size[1]) * 2
        return gl_x, gl_y, gl_width, gl_height
    
    def create_quad_vertices(self, gl_x: float, gl_y: float, gl_width: float, gl_height: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Cria vértices e índices para um quad.
        
        Args:
            gl_x, gl_y: Posição em coordenadas OpenGL
            gl_width, gl_height: Dimensões em coordenadas OpenGL
            
        Returns:
            Tupla (vertices, indices) como arrays numpy
        """
        vertices = np.array([
            gl_x, gl_y, 0.0,          0.0, 0.0,  # inferior esquerdo
            gl_x + gl_width, gl_y, 0.0,      1.0, 0.0,  # inferior direito
            gl_x + gl_width, gl_y + gl_height, 0.0, 1.0, 1.0,  # superior direito
            gl_x, gl_y + gl_height, 0.0,      0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        return vertices, indices


class TexturedComponent(RenderableComponent):
    """
    Componente base para elementos com textura.
    Fornece funcionalidades comuns para criação e gerenciamento de texturas.
    """
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        super().__init__(window_size, shader_manager)
        self.texture_id = None
        self.text_width = 0
        self.text_height = 0
        self._texture_created = False
    
    def create_texture_from_surface(self, surface) -> int:
        """
        Cria uma textura OpenGL a partir de uma superfície pygame.
        
        Args:
            surface: Superfície pygame
            
        Returns:
            ID da textura OpenGL criada
        """
        # Deletar textura anterior se existir
        if self.texture_id:
            glDeleteTextures([self.texture_id])
        
        # Obter dados da superfície
        self.text_width, self.text_height = surface.get_size()
        texture_data = pygame.image.tostring(surface, "RGBA", True)
        
        # Criar textura OpenGL
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.text_width, self.text_height, 
                    0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return self.texture_id
    
    def _destroy(self) -> None:
        """Libera recursos da textura."""
        if self.texture_id:
            glDeleteTextures([self.texture_id])
            self.texture_id = None 