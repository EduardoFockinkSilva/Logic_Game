"""
Componente para porta lógica OR com feedback visual
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


class ORGate(Component):
    def __init__(self, position, size=(120, 80), 
                 off_color=(128, 128, 128), on_color=(255, 192, 203),
                 text_color=(255, 255, 255), window_size=(800, 600), 
                 shader_manager=None, input_buttons=None):
        super().__init__()
        self.position = position  # (x, y) em coordenadas de tela
        self.size = size
        self.off_color = off_color  # Gray when off
        self.on_color = on_color    # Light pink when on
        self.text_color = text_color
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.input_buttons = input_buttons or []  # Lista de botões de entrada
        
        print(f"[ORGate] Created with off_color: {self.off_color}, on_color: {self.on_color}")
        
        # Recursos OpenGL
        self.text_texture_id = None
        self.text_width = 0
        self.text_height = 0
        self.gate_renderer = None
        self.text_renderer = None
        self.vao_name = f"or_gate_{id(self)}"
        self.text_vao_name = f"or_gate_text_{id(self)}"
        self.shader_ok = False
        self._texture_created = False
        
        # Dados do quad da porta
        self.gate_vertices = None
        self.gate_indices = None
        self.text_vertices = None
        self.text_indices = None

    def initialize(self):
        super().initialize()

    def _initialize(self):
        # Inicializar renderers
        self.gate_renderer = ModernRenderer()
        self.text_renderer = ModernRenderer()
        
        # Usar o shader manager fornecido ou criar um novo
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shaders
        try:
            # Load gate shader for gate background
            if not self.shader_manager.has_program("gate"):
                self.shader_manager.load_shader(
                    "gate",
                    "src/shaders/gate_vertex.glsl",
                    "src/shaders/gate_fragment.glsl"
                )
            
            # Load text shader for text
            if not self.shader_manager.has_program("text"):
                self.shader_manager.load_shader(
                    "text",
                    "src/shaders/text_vertex.glsl",
                    "src/shaders/text_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"[ORGate] Erro ao carregar shaders: {e}")
            self.shader_ok = False
            return
        
        # Criar textura do texto apenas uma vez
        if not self._texture_created:
            self._create_text_texture()
            self._texture_created = True
        
        # Criar dados do quad da porta e do texto
        self._create_gate_quad()
        self._create_text_quad()
        
        # Criar VAOs
        if self.gate_vertices is not None and self.gate_indices is not None:
            self.gate_renderer.create_quad_vao(self.vao_name, self.gate_vertices, self.gate_indices)
        if self.text_vertices is not None and self.text_indices is not None:
            self.text_renderer.create_quad_vao(self.text_vao_name, self.text_vertices, self.text_indices)

    def _create_text_texture(self):
        """Cria a textura do texto da porta."""
        pygame.font.init()
        font_size = min(18, self.size[1] // 4)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        text_surface = font.render("OR", True, self.text_color)
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

    def _create_gate_quad(self):
        """Cria os dados do quad da porta."""
        x, y = self.position
        width, height = self.size
        
        # Corrigir: usar y + height para alinhar o topo da porta com a coordenada de tela
        gl_x = (x / self.window_size[0]) * 2 - 1
        gl_y = 1 - ((y + height) / self.window_size[1]) * 2
        gl_width = (width / self.window_size[0]) * 2
        gl_height = (height / self.window_size[1]) * 2
        
        self.gate_vertices = np.array([
            gl_x, gl_y, 0.0,          0.0, 0.0,  # inferior esquerdo
            gl_x + gl_width, gl_y, 0.0,      1.0, 0.0,  # inferior direito
            gl_x + gl_width, gl_y + gl_height, 0.0, 1.0, 1.0,  # superior direito
            gl_x, gl_y + gl_height, 0.0,      0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        
        self.gate_indices = np.array([
            0, 1, 2, 2, 3, 0
        ], dtype=np.uint32)

    def _create_text_quad(self):
        """Cria o quad para o texto centralizado na porta."""
        x, y = self.position
        width, height = self.size
        
        # Centralizar texto na porta
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
        if self.gate_renderer is None or self.text_renderer is None or self.shader_manager is None or not self.shader_ok:
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
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        try:
            # Render gate background using gate shader
            gate_shader = self.shader_manager.get_program("gate")
            if gate_shader:
                glUseProgram(gate_shader)
                
                # Calcular resultado da porta OR
                result = self._calculate_or_result()
                
                # Escolher cor baseada no resultado
                if result:
                    color = self.on_color
                else:
                    color = self.off_color
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(gate_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar quad da porta com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 0.9)
                self.gate_renderer.render_quad(self.vao_name, gate_shader)
            
            # Render text using text shader
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
            print(f"[ORGate] Erro na renderização: {e}")
        
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

    def _calculate_or_result(self):
        """Calcula o resultado da porta OR baseado nos botões de entrada."""
        if not self.input_buttons:
            return False
        
        # OR logic: True if ANY input is True
        for button in self.input_buttons:
            if hasattr(button, 'get_state') and button.get_state():
                return True
        return False

    def add_input_button(self, button):
        """Adiciona um botão de entrada à porta."""
        if button not in self.input_buttons:
            self.input_buttons.append(button)

    def remove_input_button(self, button):
        """Remove um botão de entrada da porta."""
        if button in self.input_buttons:
            self.input_buttons.remove(button)

    def get_result(self):
        """Retorna o resultado atual da porta OR."""
        return self._calculate_or_result()

    def _destroy(self):
        """Limpa recursos OpenGL."""
        if self.text_texture_id is not None:
            glDeleteTextures([self.text_texture_id])
            self.text_texture_id = None 