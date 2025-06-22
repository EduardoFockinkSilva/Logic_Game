"""
Sistema de Componentes Base para o Jogo

Define a hierarquia base de componentes que todos os elementos
do jogo herdam. Usa o padrão Component para composição flexível.

Hierarquia:
- Component: Classe base abstrata com funcionalidades básicas
- RenderableComponent: Para componentes que precisam de renderização OpenGL
- TexturedComponent: Para componentes que usam texturas

Cada componente segue o ciclo de vida: initialize -> update/render -> destroy
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Tuple, List
import numpy as np
import pygame
from OpenGL.GL import *
from src.core.renderer import ModernRenderer
from src.core.shader_manager import ShaderManager


class Component(ABC):
    """Classe base abstrata para todos os componentes do jogo"""
    
    def __init__(self, entity: Optional[Any] = None):
        """Inicializa novo componente"""
        self.entity = entity
        self.enabled = True
        self._initialized = False
    
    def initialize(self) -> None:
        """Inicializa componente - chamado uma vez após criação"""
        if not self._initialized:
            self._initialize()
            self._initialized = True
    
    @abstractmethod
    def _initialize(self) -> None:
        """Implementação específica da inicialização - deve ser sobrescrito"""
        pass
    
    def update(self, delta_time: float) -> None:
        """Atualiza componente a cada frame"""
        if self.enabled and self._initialized:
            self._update(delta_time)
    
    def _update(self, delta_time: float) -> None:
        """Implementação específica da atualização - deve ser sobrescrito"""
        pass
    
    def render(self, renderer: Any) -> None:
        """Renderiza componente"""
        if self.enabled and self._initialized:
            self._render(renderer)
    
    def _render(self, renderer: Any) -> None:
        """Implementação específica da renderização - deve ser sobrescrito"""
        pass
    
    def destroy(self) -> None:
        """Destrói componente e libera recursos"""
        if self._initialized:
            self._destroy()
            self._initialized = False
    
    def _destroy(self) -> None:
        """Implementação específica da destruição - deve ser sobrescrito"""
        pass


class RenderableComponent(Component):
    """Componente base para elementos renderizáveis com OpenGL"""
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        """Inicializa componente renderizável"""
        super().__init__()
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.renderer = None
        self.shader_ok = False
    
    def _setup_gl_state(self):
        """Configura estado OpenGL para renderização 2D"""
        self.prev_viewport = glGetIntegerv(GL_VIEWPORT)
        self.prev_blend = glIsEnabled(GL_BLEND)
        self.prev_depth_test = glIsEnabled(GL_DEPTH_TEST)
        
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
    
    def _restore_gl_state(self):
        """Restaura estado OpenGL anterior"""
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
        """Converte coordenadas de tela para coordenadas OpenGL"""
        gl_x = (x / self.window_size[0]) * 2 - 1
        gl_y = 1 - ((y + height) / self.window_size[1]) * 2
        gl_width = (width / self.window_size[0]) * 2
        gl_height = (height / self.window_size[1]) * 2
        return gl_x, gl_y, gl_width, gl_height
    
    def create_quad_vertices(self, gl_x: float, gl_y: float, gl_width: float, gl_height: float) -> Tuple[np.ndarray, np.ndarray]:
        """Cria vértices e índices para um quad (retângulo)"""
        vertices = np.array([
            gl_x, gl_y, 0.0,          0.0, 0.0,  # inferior esquerdo
            gl_x + gl_width, gl_y, 0.0,      1.0, 0.0,  # inferior direito
            gl_x + gl_width, gl_y + gl_height, 0.0, 1.0, 1.0,  # superior direito
            gl_x, gl_y + gl_height, 0.0,      0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        return vertices, indices


class TexturedComponent(RenderableComponent):
    """Componente base para elementos com textura"""
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        """Inicializa componente com textura"""
        super().__init__(window_size, shader_manager)
        self.texture_id = None
        self.text_width = 0
        self.text_height = 0
        self._texture_created = False
    
    def create_texture_from_surface(self, surface) -> int:
        """Cria textura OpenGL a partir de superfície pygame"""
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
        """Libera recursos da textura"""
        if self.texture_id:
            glDeleteTextures([self.texture_id])
            self.texture_id = None 