"""
Sistema de Componentes Base para o Jogo.

Este módulo define a hierarquia base de componentes que todos os elementos
do jogo herdam. O sistema usa o padrão Component para permitir composição
flexível de funcionalidades.

A hierarquia inclui:
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


class Component(ABC):
    """
    Classe base abstrata para todos os componentes do jogo.
    
    Implementa o padrão Component para arquitetura modular, permitindo
    que entidades sejam compostas por múltiplos componentes que fornecem
    funcionalidades específicas. Cada componente segue um ciclo de vida
    bem definido: inicialização, atualização/renderização, e destruição.
    
    Attributes:
        entity: Entidade pai que possui este componente
        enabled: Se o componente está ativo e deve ser atualizado/renderizado
        _initialized: Flag interna para controlar se o componente foi inicializado
    """
    
    def __init__(self, entity: Optional[Any] = None):
        """
        Inicializa um novo componente.
        
        Args:
            entity: Entidade pai que possui este componente (opcional)
        """
        self.entity = entity
        self.enabled = True
        self._initialized = False
    
    def initialize(self) -> None:
        """
        Inicializa o componente. Chamado uma vez após a criação.
        
        Este método garante que a inicialização aconteça apenas uma vez,
        mesmo se chamado múltiplas vezes. Subclasses devem sobrescrever
        _initialize() para implementar a inicialização específica.
        """
        if not self._initialized:
            self._initialize()
            self._initialized = True
    
    @abstractmethod
    def _initialize(self) -> None:
        """
        Implementação específica da inicialização.
        
        Este método deve ser sobrescrito pelas subclasses para implementar
        a inicialização específica do componente, como carregar recursos,
        configurar OpenGL, etc.
        """
        pass
    
    def update(self, delta_time: float) -> None:
        """
        Atualiza o componente a cada frame.
        
        Este método é chamado a cada frame para atualizar a lógica do componente.
        Só executa se o componente estiver habilitado e inicializado.
        
        Args:
            delta_time: Tempo desde o último frame em segundos
        """
        if self.enabled and self._initialized:
            self._update(delta_time)
    
    def _update(self, delta_time: float) -> None:
        """
        Implementação específica da atualização.
        
        Este método deve ser sobrescrito pelas subclasses para implementar
        a lógica de atualização específica do componente.
        
        Args:
            delta_time: Tempo desde o último frame em segundos
        """
        pass
    
    def render(self, renderer: Any) -> None:
        """
        Renderiza o componente.
        
        Este método é chamado a cada frame para renderizar o componente.
        Só executa se o componente estiver habilitado e inicializado.
        
        Args:
            renderer: Renderizador OpenGL ou outro sistema de renderização
        """
        if self.enabled and self._initialized:
            self._render(renderer)
    
    def _render(self, renderer: Any) -> None:
        """
        Implementação específica da renderização.
        
        Este método deve ser sobrescrito pelas subclasses para implementar
        a renderização específica do componente.
        
        Args:
            renderer: Renderizador OpenGL ou outro sistema de renderização
        """
        pass
    
    def destroy(self) -> None:
        """
        Destrói o componente e libera recursos.
        
        Este método garante que os recursos sejam liberados adequadamente,
        mesmo se chamado múltiplas vezes. Subclasses devem sobrescrever
        _destroy() para implementar a limpeza específica.
        """
        if self._initialized:
            self._destroy()
            self._initialized = False
    
    def _destroy(self) -> None:
        """
        Implementação específica da destruição.
        
        Este método deve ser sobrescrito pelas subclasses para implementar
        a limpeza específica de recursos, como deletar texturas OpenGL,
        fechar arquivos, etc.
        """
        pass


class RenderableComponent(Component):
    """
    Componente base para elementos renderizáveis com OpenGL.
    
    Fornece funcionalidades comuns para renderização OpenGL, incluindo
    gerenciamento de estado OpenGL, conversão de coordenadas e criação
    de geometria básica. Subclasses podem focar na lógica específica
    de renderização sem se preocupar com detalhes OpenGL.
    
    Attributes:
        window_size: Tamanho da janela (largura, altura)
        shader_manager: Gerenciador de shaders (opcional)
        renderer: Renderizador associado (opcional)
        shader_ok: Flag indicando se os shaders estão funcionando
    """
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        """
        Inicializa um componente renderizável.
        
        Args:
            window_size: Tamanho da janela (largura, altura)
            shader_manager: Gerenciador de shaders (opcional)
        """
        super().__init__()
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.renderer = None
        self.shader_ok = False
    
    def _setup_gl_state(self):
        """
        Configura o estado OpenGL para renderização 2D.
        
        Salva o estado atual do OpenGL e configura para renderização 2D
        com blending habilitado e depth test desabilitado.
        """
        self.prev_viewport = glGetIntegerv(GL_VIEWPORT)
        self.prev_blend = glIsEnabled(GL_BLEND)
        self.prev_depth_test = glIsEnabled(GL_DEPTH_TEST)
        
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
    
    def _restore_gl_state(self):
        """
        Restaura o estado OpenGL anterior.
        
        Restaura o viewport, blending e depth test para os valores
        que estavam ativos antes da configuração.
        """
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
        
        Converte coordenadas de tela (pixels) para coordenadas OpenGL
        normalizadas (-1 a 1), considerando que o eixo Y é invertido
        no OpenGL em relação ao sistema de coordenadas da tela.
        
        Args:
            x, y: Posição em coordenadas de tela (pixels)
            width, height: Dimensões em coordenadas de tela (pixels)
            
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
        Cria vértices e índices para um quad (retângulo).
        
        Cria arrays numpy com vértices e índices para renderizar um quad
        na posição e tamanho especificados. Os vértices incluem coordenadas
        de textura para mapeamento UV.
        
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
    
    Fornece funcionalidades comuns para criação e gerenciamento de texturas
    OpenGL a partir de superfícies pygame. Subclasses podem facilmente
    criar texturas a partir de imagens ou superfícies renderizadas.
    
    Attributes:
        texture_id: ID da textura OpenGL
        text_width: Largura da textura em pixels
        text_height: Altura da textura em pixels
        _texture_created: Flag indicando se a textura foi criada
    """
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        """
        Inicializa um componente com textura.
        
        Args:
            window_size: Tamanho da janela (largura, altura)
            shader_manager: Gerenciador de shaders (opcional)
        """
        super().__init__(window_size, shader_manager)
        self.texture_id = None
        self.text_width = 0
        self.text_height = 0
        self._texture_created = False
    
    def create_texture_from_surface(self, surface) -> int:
        """
        Cria uma textura OpenGL a partir de uma superfície pygame.
        
        Converte uma superfície pygame em uma textura OpenGL, configurando
        filtros de textura apropriados para renderização 2D.
        
        Args:
            surface: Superfície pygame a ser convertida
            
        Returns:
            ID da textura OpenGL criada
            
        Note:
            Se uma textura já existir, ela será deletada antes de criar a nova.
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
        """
        Libera recursos da textura.
        
        Deleta a textura OpenGL se ela existir, liberando a memória
        de vídeo associada.
        """
        if self.texture_id:
            glDeleteTextures([self.texture_id])
            self.texture_id = None 