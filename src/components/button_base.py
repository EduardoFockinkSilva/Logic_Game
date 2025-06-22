"""
Componente base para botões com funcionalidades comuns
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_component import TexturedComponent
import sys
import os

# Adicionar o diretório src ao path para imports absolutos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from graphics.renderer import ModernRenderer
from shaders.shader_manager import ShaderManager
from typing import Optional, Callable, Tuple


class ButtonBase(TexturedComponent):
    """
    Classe base para botões (InputButton, MenuButton).
    Elimina duplicação de código entre diferentes tipos de botões.
    """
    
    def __init__(self, text: str, position: Tuple[int, int], size: Tuple[int, int] = (80, 80),
                 off_color: Tuple[int, int, int] = (255, 0, 0), on_color: Tuple[int, int, int] = (0, 255, 0),
                 text_color: Tuple[int, int, int] = (255, 255, 255), window_size: Tuple[int, int] = (800, 600),
                 shader_manager=None, callback: Optional[Callable] = None, initial_state: bool = False,
                 button_type: str = "circle"):
        super().__init__(window_size, shader_manager)
        
        self.text = text
        self.position = position
        self.size = size
        self.off_color = off_color
        self.on_color = on_color
        self.text_color = text_color
        self.callback = callback
        self.state = initial_state
        self.button_type = button_type  # "circle" ou "rectangle"
        
        # Estado do botão
        self.is_hovered = False
        self.is_clicked = False
        
        # Recursos OpenGL
        self.button_renderer = None
        self.text_renderer = None
        self.vao_name = f"{button_type}_button_{id(self)}"
        self.text_vao_name = f"{button_type}_button_text_{id(self)}"
        
        # Dados do botão
        self.button_vertices = None
        self.button_indices = None
        self.text_vertices = None
        self.text_indices = None

    def _initialize(self):
        """Inicializa renderers e shaders."""
        # Inicializar renderers
        self.button_renderer = ModernRenderer()
        self.text_renderer = ModernRenderer()
        
        # Usar o shader manager fornecido ou criar um novo
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shaders
        try:
            # Load button shader
            shader_name = "circle" if self.button_type == "circle" else "button"
            if not self.shader_manager.has_program(shader_name):
                self.shader_manager.load_shader(
                    shader_name,
                    "src/shaders/button_vertex.glsl",
                    "src/shaders/button_fragment.glsl"
                )
            
            # Load text shader
            if not self.shader_manager.has_program("text"):
                self.shader_manager.load_shader(
                    "text",
                    "src/shaders/text_vertex.glsl",
                    "src/shaders/text_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"[ButtonBase] Erro ao carregar shaders: {e}")
            self.shader_ok = False
            return
        
        # Criar textura do texto apenas uma vez
        if not self._texture_created:
            self._create_text_texture()
            self._texture_created = True
        
        # Criar dados do botão e do texto
        self._create_button_quad()
        self._create_text_quad()
        
        # Criar VAOs
        if self.button_vertices is not None and self.button_indices is not None:
            self.button_renderer.create_quad_vao(self.vao_name, self.button_vertices, self.button_indices)
        if self.text_vertices is not None and self.text_indices is not None:
            self.text_renderer.create_quad_vao(self.text_vao_name, self.text_vertices, self.text_indices)

    def _create_text_texture(self):
        """Cria a textura do texto do botão."""
        pygame.font.init()
        font_size = min(14, self.size[1] // 4)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        text_surface = font.render(self.text, True, self.text_color)
        self.create_texture_from_surface(text_surface)

    def _create_button_quad(self):
        """Cria os dados do quad do botão."""
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            self.position[0], self.position[1], self.size[0], self.size[1]
        )
        self.button_vertices, self.button_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _create_text_quad(self):
        """Cria o quad para o texto centralizado no botão."""
        # Centralizar texto no botão
        text_x = self.position[0] + (self.size[0] - self.text_width) // 2
        text_y = self.position[1] + (self.size[1] - self.text_height) // 2
        
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            text_x, text_y, self.text_width, self.text_height
        )
        self.text_vertices, self.text_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _update(self, delta_time):
        pass

    def _render(self, renderer):
        if self.button_renderer is None or self.text_renderer is None or self.shader_manager is None or not self.shader_ok:
            return
            
        self._setup_gl_state()
        
        # Matriz de projeção ortográfica
        ortho = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        try:
            # Render button
            shader_name = "circle" if self.button_type == "circle" else "button"
            button_shader = self.shader_manager.get_program(shader_name)
            if button_shader:
                glUseProgram(button_shader)
                
                # Escolher cor baseada no estado
                if self.state:
                    color = self.on_color
                else:
                    color = self.off_color
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(button_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar botão com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
                self.button_renderer.render_quad(self.vao_name, button_shader)
            
            # Render text
            text_shader = self.shader_manager.get_program("text")
            if text_shader and self.texture_id:
                glUseProgram(text_shader)
                
                # Setar textura
                location = glGetUniformLocation(text_shader, "textTexture")
                if location != -1:
                    glUniform1i(location, 0)
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(text_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                self.text_renderer.render_quad(self.text_vao_name, text_shader, self.texture_id)
                
        except Exception as e:
            print(f"[ButtonBase] Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()

    def handle_mouse_event(self, event):
        """Processa eventos do mouse. Deve ser implementado pelas subclasses."""
        pass

    def _check_hover(self, mouse_x: int, mouse_y: int) -> bool:
        """Verifica se o mouse está sobre o botão."""
        x, y = self.position
        width, height = self.size
        return (x <= mouse_x <= x + width and y <= mouse_y <= y + height)

    def get_state(self) -> bool:
        """Retorna o estado atual do botão."""
        return self.state

    def set_state(self, state: bool):
        """Define o estado do botão."""
        self.state = state

    def _destroy(self):
        """Destrói recursos OpenGL."""
        super()._destroy()
        if self.button_renderer:
            self.button_renderer.cleanup()
        if self.text_renderer:
            self.text_renderer.cleanup() 