"""
Componente para botões de entrada que podem ser alternados on/off
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
    return pygame.transform.flip(surface, False, False)


class InputButton(Component):
    def __init__(self, text, position, size=(80, 80), 
                 off_color=(255, 0, 0), on_color=(0, 255, 0),
                 text_color=(255, 255, 255), window_size=(800, 600), 
                 shader_manager=None, initial_state=False):
        super().__init__()
        self.text = text
        self.position = position  # (x, y) em coordenadas de tela
        self.size = size
        self.off_color = off_color  # Red when off
        self.on_color = on_color    # Green when on
        self.text_color = text_color
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.state = initial_state  # False = off, True = on
        
        # Estado do botão
        self.is_hovered = False
        self.is_clicked = False
        
        # Recursos OpenGL
        self.text_texture_id = None
        self.text_width = 0
        self.text_height = 0
        self.button_renderer = None
        self.text_renderer = None
        self.vao_name = f"input_button_{id(self)}"
        self.text_vao_name = f"input_button_text_{id(self)}"
        self.shader_ok = False
        self._texture_created = False
        
        # Dados do círculo do botão
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
        
        # Carregar shaders
        try:
            # Load circle shader for button
            if not self.shader_manager.has_program("circle"):
                self.shader_manager.load_shader(
                    "circle",
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
            print(f"[InputButton] Erro ao carregar shaders: {e}")
            self.shader_ok = False
            return
        
        # Criar textura do texto apenas uma vez
        if not self._texture_created:
            self._create_text_texture()
            self._texture_created = True
        
        # Criar dados do círculo do botão e do texto
        self._create_circle_quad()
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
        # Don't flip the surface - this was causing the text inversion
        self.text_width, self.text_height = text_surface.get_size()
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        # Criar textura OpenGL
        self.text_texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.text_width, self.text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

    def _create_circle_quad(self):
        """Cria os dados do quad circular do botão."""
        x, y = self.position
        width, height = self.size
        
        # Corrigir: usar y + height para alinhar o topo do botão com a coordenada de tela
        gl_x = (x / self.window_size[0]) * 2 - 1
        gl_y = 1 - ((y + height) / self.window_size[1]) * 2
        gl_width = (width / self.window_size[0]) * 2
        gl_height = (height / self.window_size[1]) * 2
        
        # Criar um quad que será renderizado como círculo no fragment shader
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
        
        # Centralizar texto no botão
        text_x = x + (width - self.text_width) // 2
        text_y = y + (height - self.text_height) // 2
        
        # Corrigir: alinhar topo do texto
        gl_x = (text_x / self.window_size[0]) * 2 - 1
        gl_y = 1 - ((text_y + self.text_height) / self.window_size[1]) * 2
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
        
        # Matriz de projeção ortográfica - usar identidade já que coordenadas já estão em OpenGL
        ortho = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        try:
            # Render circle button
            circle_shader = self.shader_manager.get_program("circle")
            if circle_shader:
                glUseProgram(circle_shader)
                
                # Escolher cor baseada no estado
                color = self.on_color if self.state else self.off_color
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(circle_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar círculo do botão
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 0.9)
                self.button_renderer.render_quad(self.vao_name, circle_shader)
            
            # Render text
            text_shader = self.shader_manager.get_program("text")
            if text_shader and self.text_texture_id is not None:
                glUseProgram(text_shader)
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(text_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar texto
                glBindTexture(GL_TEXTURE_2D, self.text_texture_id)
                glUniform1i(glGetUniformLocation(text_shader, "textTexture"), 0)
                glVertexAttrib4f(2, 1.0, 1.0, 1.0, 1.0)
                self.text_renderer.render_quad(self.text_vao_name, text_shader)
                glBindTexture(GL_TEXTURE_2D, 0)
                
        except Exception as e:
            print(f"[InputButton] Erro na renderização: {e}")
        
        finally:
            # Restaurar estado OpenGL
            glViewport(*prev_viewport)
            if prev_blend:
                glEnable(GL_BLEND)
            else:
                glDisable(GL_BLEND)
            if prev_depth_test:
                glEnable(GL_DEPTH_TEST)
            else:
                glDisable(GL_DEPTH_TEST)

    def handle_mouse_event(self, event):
        """Manipula eventos de mouse para o botão."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if self._check_hover(mouse_x, mouse_y):
                self.is_clicked = True
                self.state = not self.state  # Alternar estado
                print(f"Input button '{self.text}' toggled to: {'ON' if self.state else 'OFF'}")
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_clicked = False
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.is_hovered = self._check_hover(mouse_x, mouse_y)
        
        return False

    def _check_hover(self, mouse_x, mouse_y):
        """Verifica se o mouse está sobre o botão (círculo)."""
        x, y = self.position
        width, height = self.size
        
        # Calcular centro do círculo
        center_x = x + width // 2
        center_y = y + height // 2
        radius = min(width, height) // 2
        
        # Calcular distância do mouse ao centro
        distance = ((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2) ** 0.5
        
        return distance <= radius

    def get_state(self):
        """Retorna o estado atual do botão."""
        return self.state

    def set_state(self, state):
        """Define o estado do botão."""
        self.state = bool(state)

    def _destroy(self):
        """Destrói recursos OpenGL."""
        if self.text_texture_id is not None:
            glDeleteTextures([self.text_texture_id])
            self.text_texture_id = None 