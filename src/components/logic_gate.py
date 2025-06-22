"""
Componente base para portas lógicas com funcionalidades comuns
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
from typing import List, Callable, Optional


class LogicGate(TexturedComponent):
    """
    Classe base para portas lógicas (AND, OR, NOT).
    Elimina duplicação de código entre as diferentes portas.
    """
    
    def __init__(self, gate_type: str, position: tuple, size: tuple = (120, 80),
                 off_color: tuple = (128, 128, 128), on_color: tuple = (255, 255, 224),
                 text_color: tuple = (255, 255, 255), window_size: tuple = (800, 600),
                 shader_manager=None, input_buttons: Optional[List] = None,
                 logic_function: Optional[Callable] = None):
        super().__init__(window_size, shader_manager)
        
        self.gate_type = gate_type
        self.position = position
        self.size = size
        self.off_color = off_color
        self.on_color = on_color
        self.text_color = text_color
        self.input_buttons = input_buttons or []
        self.logic_function = logic_function
        
        # Recursos OpenGL
        self.gate_renderer = None
        self.text_renderer = None
        self.vao_name = f"{gate_type.lower()}_gate_{id(self)}"
        self.text_vao_name = f"{gate_type.lower()}_gate_text_{id(self)}"
        
        # Dados do quad da porta
        self.gate_vertices = None
        self.gate_indices = None
        self.text_vertices = None
        self.text_indices = None
        
        print(f"[{gate_type}Gate] Created with off_color: {self.off_color}, on_color: {self.on_color}")

    def _initialize(self):
        """Inicializa renderers e shaders."""
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
            print(f"[{self.gate_type}Gate] Erro ao carregar shaders: {e}")
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
        text_surface = font.render(self.gate_type, True, self.text_color)
        self.create_texture_from_surface(text_surface)

    def _create_gate_quad(self):
        """Cria os dados do quad da porta."""
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            self.position[0], self.position[1], self.size[0], self.size[1]
        )
        self.gate_vertices, self.gate_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _create_text_quad(self):
        """Cria o quad para o texto centralizado na porta."""
        # Centralizar texto na porta
        text_x = self.position[0] + (self.size[0] - self.text_width) // 2
        text_y = self.position[1] + (self.size[1] - self.text_height) // 2
        
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            text_x, text_y, self.text_width, self.text_height
        )
        self.text_vertices, self.text_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _update(self, delta_time):
        pass

    def _render(self, renderer):
        if self.gate_renderer is None or self.text_renderer is None or self.shader_manager is None or not self.shader_ok:
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
            # Render gate background using gate shader
            gate_shader = self.shader_manager.get_program("gate")
            if gate_shader:
                glUseProgram(gate_shader)
                
                # Calcular resultado da porta
                result = self._calculate_result()
                
                # Escolher cor baseada no resultado
                if result:
                    color = self.on_color
                else:
                    color = self.off_color
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(gate_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar porta com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
                self.gate_renderer.render_quad(self.vao_name, gate_shader)
            
            # Render text using text shader
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
            print(f"[{self.gate_type}Gate] Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()

    def _calculate_result(self) -> bool:
        """Calcula o resultado da porta lógica. Deve ser implementado pelas subclasses."""
        if self.logic_function:
            return self.logic_function(self.input_buttons)
        return False

    def add_input_button(self, button):
        """Adiciona um botão de entrada à porta."""
        if button not in self.input_buttons:
            self.input_buttons.append(button)

    def remove_input_button(self, button):
        """Remove um botão de entrada da porta."""
        if button in self.input_buttons:
            self.input_buttons.remove(button)

    def get_result(self) -> bool:
        """Retorna o resultado atual da porta."""
        return self._calculate_result()

    def _destroy(self):
        """Destrói recursos OpenGL."""
        super()._destroy()
        if self.gate_renderer:
            self.gate_renderer.cleanup()
        if self.text_renderer:
            self.text_renderer.cleanup()


# Funções lógicas específicas
def and_logic(input_buttons: List) -> bool:
    """Implementa a lógica AND: retorna True se todos os botões estiverem ativos."""
    if not input_buttons:
        return False
    return all(button.get_state() if hasattr(button, 'get_state') else False for button in input_buttons)


def or_logic(input_buttons: List) -> bool:
    """Implementa a lógica OR: retorna True se pelo menos um botão estiver ativo."""
    if not input_buttons:
        return False
    return any(button.get_state() if hasattr(button, 'get_state') else False for button in input_buttons)


def not_logic(input_buttons: List) -> bool:
    """Implementa a lógica NOT: retorna True se o botão estiver inativo."""
    if not input_buttons:
        return True
    # NOT gate usa apenas o primeiro botão de entrada
    button = input_buttons[0]
    return not (button.get_state() if hasattr(button, 'get_state') else False) 