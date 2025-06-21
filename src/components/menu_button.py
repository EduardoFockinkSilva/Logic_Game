"""
Componente para renderizar botões de menu clicáveis
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_component import Component
from ..graphics.renderer import ModernRenderer
from ..shaders.shader_manager import ShaderManager


def _flip_surface(surface):
    """Inverte a superfície verticalmente (corrige origem do OpenGL)."""
    return pygame.transform.flip(surface, False, True)

class MenuButton(Component):
    def __init__(self, text, position, size=(200, 50), color=(100, 150, 255), 
                 hover_color=(150, 200, 255), window_size=(800, 600), 
                 shader_manager=None, callback=None, bg_color=(40, 40, 80), border_color=(180, 180, 220)):
        super().__init__()
        self.text = text
        self.position = position  # (x, y) em coordenadas de tela
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.callback = callback
        self.bg_color = bg_color
        self.border_color = border_color
        
        # Estado do botão
        self.is_hovered = False
        self.is_clicked = False
        
        # Recursos OpenGL
        self.text_texture_id = None
        self.text_width = 0
        self.text_height = 0
        self.button_renderer = None
        self.text_renderer = None
        self.vao_name = f"button_{id(self)}"
        self.text_vao_name = f"button_text_{id(self)}"
        self.shader_ok = False
        self._texture_created = False
        
        # Dados do quad do botão
        self.button_vertices = None
        self.button_indices = None
        self.text_vertices = None
        self.text_indices = None

    def initialize(self):
        super().initialize()

    def _initialize(self):
        # Inicializar renderers
        self.button_renderer = ModernRenderer()
        self.text_renderer = ModernRenderer()
        
        # Usar o shader manager fornecido ou criar um novo
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shader de texto apenas se não foi carregado antes
        try:
            if not self.shader_manager.has_program("text"):
                self.shader_manager.load_shader(
                    "text",
                    "src/shaders/text_vertex.glsl",
                    "src/shaders/text_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"[MenuButton] Erro ao carregar shader de texto: {e}")
            self.shader_ok = False
            return
        
        # Criar textura do texto apenas uma vez
        if not self._texture_created:
            self._create_text_texture()
            self._texture_created = True
        
        # Criar dados do quad do botão e do texto
        self._create_button_quad()
        self._create_text_quad()
        
        # Criar VAOs
        if self.button_vertices is not None and self.button_indices is not None:
            self.button_renderer.create_quad_vao(self.vao_name, self.button_vertices, self.button_indices)
        if self.text_vertices is not None and self.text_indices is not None:
            self.text_renderer.create_quad_vao(self.text_vao_name, self.text_vertices, self.text_indices)

    def _create_text_texture(self):
        """Cria a textura do texto do botão, corrigindo a orientação."""
        pygame.font.init()
        # Reduzir o tamanho da fonte para caber no botão
        font_size = min(20, self.size[1] // 2)  # Máximo 20px ou metade da altura do botão
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        text_surface = font.render(self.text, True, self.color)
        text_surface = _flip_surface(text_surface)  # Corrigir orientação
        self.text_width, self.text_height = text_surface.get_size()
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        # Criar textura OpenGL
        self.text_texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.text_width, self.text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

    def _create_button_quad(self):
        """Cria os dados do quad do botão (retângulo preenchido) com leve ajuste para cima (somando ao Y)."""
        x, y = self.position
        width, height = self.size
        y = y + 25  # Somar para subir
        # Converter coordenadas de tela para OpenGL (-1 a 1)
        gl_x = (x / self.window_size[0]) * 2 - 1
        gl_y = 1 - (y / self.window_size[1]) * 2
        gl_width = (width / self.window_size[0]) * 2
        gl_height = (height / self.window_size[1]) * 2
        self.button_vertices = np.array([
            gl_x, gl_y, 0.0,          0.0, 0.0,  # inferior esquerdo
            gl_x + gl_width, gl_y, 0.0,      1.0, 0.0,  # inferior direito
            gl_x + gl_width, gl_y + gl_height, 0.0, 1.0, 1.0,  # superior direito
            gl_x, gl_y + gl_height, 0.0,      0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        self.button_indices = np.array([
            0, 1, 2, 2, 3, 0
        ], dtype=np.uint32)

    def _create_text_quad(self):
        """Cria o quad para o texto centralizado no botão."""
        x, y = self.position
        width, height = self.size
        
        # Centralizar texto no botão (usando coordenadas de tela)
        # x e y são as coordenadas do canto superior esquerdo do botão
        text_x = x + (width - self.text_width) // 2
        text_y = y + (height - self.text_height) // 2  # Removido o offset -50
        
        # Converter para coordenadas OpenGL (-1 a 1)
        # Considerando que Y maior = mais para cima no sistema usado
        gl_x = (text_x / self.window_size[0]) * 2 - 1
        gl_y = 1 - (text_y / self.window_size[1]) * 2
        gl_width = (self.text_width / self.window_size[0]) * 2
        gl_height = (self.text_height / self.window_size[1]) * 2
        
        self.text_vertices = np.array([
            gl_x, gl_y, 0.0,          0.0, 0.0,
            gl_x + gl_width, gl_y, 0.0,      1.0, 0.0,
            gl_x + gl_width, gl_y + gl_height, 0.0, 1.0, 1.0,
            gl_x, gl_y + gl_height, 0.0,      0.0, 1.0
        ], dtype=np.float32)
        
        self.text_indices = np.array([
            0, 1, 2, 2, 3, 0
        ], dtype=np.uint32)

    def _update(self, delta_time):
        pass

    def _render(self, renderer):
        if self.button_renderer is None or self.text_renderer is None or self.shader_manager is None or not self.shader_ok:
            return
        prev_viewport = glGetIntegerv(GL_VIEWPORT)
        prev_blend = glIsEnabled(GL_BLEND)
        prev_depth_test = glIsEnabled(GL_DEPTH_TEST)
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        # Matriz de projeção ortográfica
        left, right = -1, 1
        top, bottom = -1, 1
        near, far = -1, 1
        ortho = np.array([
            [2/(right-left), 0, 0, -(right+left)/(right-left)],
            [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
            [0, 0, -2/(far-near), -(far+near)/(far-near)],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        try:
            shader_program = self.shader_manager.get_program("text")
            if shader_program:
                glUseProgram(shader_program)
                # Desenhar retângulo preenchido (botão)
                color = self.hover_color if self.is_hovered else self.bg_color
                loc_proj = glGetUniformLocation(shader_program, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar quad do botão (sem textura)
                glUniform1i(glGetUniformLocation(shader_program, "textTexture"), 0)
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 0.85)
                self.button_renderer.render_quad(self.vao_name, shader_program)
                
                # Desenhar texto por cima com a cor correta
                text_color = self.hover_color if self.is_hovered else self.color
                glVertexAttrib4f(2, text_color[0]/255.0, text_color[1]/255.0, text_color[2]/255.0, 1.0)
                glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
                self.text_renderer.render_quad(self.text_vao_name, shader_program, self.text_texture_id)
                glBindTexture(GL_TEXTURE_2D, 0)
        except Exception as e:
            print(f"[MenuButton] Erro ao renderizar botão: {e}")
        finally:
            glViewport(prev_viewport[0], prev_viewport[1], prev_viewport[2], prev_viewport[3])
            if prev_blend:
                glEnable(GL_BLEND)
            else:
                glDisable(GL_BLEND)
            if prev_depth_test:
                glEnable(GL_DEPTH_TEST)
            else:
                glDisable(GL_DEPTH_TEST)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self._check_hover(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if self._check_hover(mouse_x, mouse_y):
                    self.is_clicked = True
                    if self.callback:
                        self.callback()

    def _check_hover(self, mouse_x, mouse_y):
        x, y = self.position
        width, height = self.size
        
        # Apply the same coordinate transformation as the button rendering
        # Convert mouse coordinates to the same space as the button
        mouse_gl_x = (mouse_x / self.window_size[0]) * 2 - 1
        mouse_gl_y = 1 - (mouse_y / self.window_size[1]) * 2
        
        # Convert button coordinates to OpenGL space (same as in _create_button_quad)
        button_x = x + 25  # Apply the same offset as the button
        button_y = y + 25  # Apply the same offset as the button
        button_gl_x = (button_x / self.window_size[0]) * 2 - 1
        button_gl_y = 1 - (button_y / self.window_size[1]) * 2
        button_gl_width = (width / self.window_size[0]) * 2
        button_gl_height = (height / self.window_size[1]) * 2
        
        # Check if mouse is inside the button in OpenGL coordinates
        if (button_gl_x <= mouse_gl_x <= button_gl_x + button_gl_width and 
            button_gl_y <= mouse_gl_y <= button_gl_y + button_gl_height):
            if not self.is_hovered:
                self.is_hovered = True
                self._update_hover_texture()
            return True
        else:
            if self.is_hovered:
                self.is_hovered = False
                self._update_normal_texture()
            return False

    def _update_hover_texture(self):
        if self._texture_created:
            pygame.font.init()
            font_size = min(20, self.size[1] // 2)
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text_surface = font.render(self.text, True, self.hover_color)
            text_surface = _flip_surface(text_surface)
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.text_width, self.text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            glBindTexture(GL_TEXTURE_2D, 0)

    def _update_normal_texture(self):
        if self._texture_created:
            pygame.font.init()
            font_size = min(20, self.size[1] // 2)
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text_surface = font.render(self.text, True, self.color)
            text_surface = _flip_surface(text_surface)
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.text_width, self.text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            glBindTexture(GL_TEXTURE_2D, 0)

    def _destroy(self):
        if self.text_texture_id:
            glDeleteTextures([self.text_texture_id])
        if self.button_renderer:
            self.button_renderer.cleanup()
        if self.text_renderer:
            self.text_renderer.cleanup() 