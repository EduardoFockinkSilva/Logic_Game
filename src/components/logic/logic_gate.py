"""
Sistema de Portas Lógicas Base

Define a classe LogicGate, base para todas as portas lógicas do jogo.
Implementa funcionalidades comuns como entrada/saída lógica, renderização
e integração com o sistema de componentes.
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from src.components.core.base_component import TexturedComponent
from src.components.core.interfaces import LogicInputSource, RenderableState
from typing import List, Callable, Optional, Tuple
from src.core.renderer import ModernRenderer
from src.core.shader_manager import ShaderManager


class LogicGate(TexturedComponent, LogicInputSource, RenderableState):
    """Classe base para todas as portas lógicas do jogo"""
    
    def __init__(self, position: Tuple[int, int] = (0, 0), size: Tuple[int, int] = (60, 40),
                 off_color: Tuple[int, int, int] = (128, 128, 128),
                 on_color: Tuple[int, int, int] = (255, 255, 255)):
        """Inicializa nova porta lógica"""
        super().__init__()
        self.inputs: List[LogicInputSource] = []
        self.output = False
        self.off_color = off_color
        self.on_color = on_color
        self.position = position
        self.size = size
        
        # Recursos OpenGL
        self.gate_renderer = None
        self.text_renderer = None
        self.vao_name = f"{self.__class__.__name__.lower()}_{id(self)}"
        self.text_vao_name = f"{self.__class__.__name__.lower()}_text_{id(self)}"
        
        # Dados do quad da porta
        self.gate_vertices = None
        self.gate_indices = None
        self.text_vertices = None
        self.text_indices = None
        
        print(f"{self.__class__.__name__} criada com off_color: {off_color}, on_color: {on_color}")

    def _initialize(self):
        """Inicializa renderers e shaders"""
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
            print(f"Erro ao carregar shaders: {e}")
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
        """Cria textura do texto da porta"""
        pygame.font.init()
        font_size = min(18, self.size[1] // 4)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        text_surface = font.render(self.__class__.__name__.replace('Gate', ''), True, (255, 255, 255))
        self.create_texture_from_surface(text_surface)

    def _create_gate_quad(self):
        """Cria dados do quad da porta"""
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            self.position[0], self.position[1], self.size[0], self.size[1]
        )
        self.gate_vertices, self.gate_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _create_text_quad(self):
        """Cria quad para texto centralizado na porta"""
        # Centralizar texto na porta
        text_x = self.position[0] + (self.size[0] - self.text_width) // 2
        text_y = self.position[1] + (self.size[1] - self.text_height) // 2
        
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            text_x, text_y, self.text_width, self.text_height
        )
        self.text_vertices, self.text_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _update(self, delta_time):
        """Atualização específica da porta lógica"""
        # Recalcular resultado para manter estado atualizado
        self.get_result()

    def _render(self, renderer):
        """Renderização específica da porta lógica"""
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
            # Renderizar fundo da porta usando shader gate
            gate_shader = self.shader_manager.get_program("gate")
            if gate_shader:
                glUseProgram(gate_shader)
                
                # Obter cor de renderização
                color = self.get_render_color()
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(gate_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar porta com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
                self.gate_renderer.render_quad(self.vao_name, gate_shader)
            
            # Renderizar texto usando shader text
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
            print(f"Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()

    def _calculate_result(self) -> bool:
        """Calcula resultado da porta lógica - deve ser sobrescrito pelas subclasses"""
        return False

    def add_input(self, input_source: LogicInputSource) -> None:
        """Adiciona fonte de entrada à porta lógica"""
        if isinstance(input_source, LogicInputSource):
            self.inputs.append(input_source)
        else:
            raise TypeError(f"Input source must implement LogicInputSource, got {type(input_source)}")

    def remove_input(self, input_source: LogicInputSource) -> None:
        """Remove fonte de entrada da porta lógica"""
        if input_source in self.inputs:
            self.inputs.remove(input_source)

    def get_result(self) -> bool:
        """Retorna resultado lógico atual da porta"""
        self.output = self._calculate_result()
        return self.output

    def get_render_color(self) -> Tuple[int, int, int]:
        """Retorna cor atual para renderização baseada no estado"""
        return self.on_color if self.get_result() else self.off_color
    
    def get_position(self) -> Tuple[int, int]:
        """Retorna posição da porta na tela"""
        return self.position
    
    def get_size(self) -> Tuple[int, int]:
        """Retorna tamanho da porta"""
        return self.size

    def _destroy(self):
        """Destrói recursos OpenGL"""
        super()._destroy()
        if hasattr(self, 'gate_renderer') and self.gate_renderer:
            self.gate_renderer.cleanup()
        if hasattr(self, 'text_renderer') and self.text_renderer:
            self.text_renderer.cleanup() 