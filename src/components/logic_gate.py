"""
Sistema de Portas Lógicas Base.

Este módulo define a classe LogicGate, que serve como base para todas as
portas lógicas do jogo (AND, OR, NOT). Implementa funcionalidades comuns
como entrada/saída lógica, renderização e integração com o sistema de
componentes.

A classe LogicGate implementa as interfaces LogicInputSource e RenderableState,
permitindo que portas lógicas sejam usadas como fonte de entrada para LEDs
e outros componentes, além de fornecer dados para renderização baseados
em seu estado atual.
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_component import TexturedComponent
import sys
import os
from .interfaces import LogicInputSource, RenderableState
from typing import List, Callable, Optional, Tuple
from src.graphics.renderer import ModernRenderer
from src.shaders.shader_manager import ShaderManager

# Adicionar o diretório src ao path para imports absolutos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class LogicGate(TexturedComponent, LogicInputSource, RenderableState):
    """
    Classe base para todas as portas lógicas do jogo.
    
    Fornece funcionalidades comuns para portas lógicas, incluindo:
    - Gerenciamento de entradas e saída lógica
    - Renderização baseada no estado
    - Integração com o sistema de componentes
    - Implementação das interfaces LogicInputSource e RenderableState
    
    Subclasses devem implementar _calculate_result() para definir a lógica
    específica de cada tipo de porta.
    
    Attributes:
        inputs: Lista de componentes de entrada (LogicInputSource)
        output: Resultado calculado da porta lógica
        off_color: Cor quando a porta está desligada (R, G, B)
        on_color: Cor quando a porta está ligada (R, G, B)
        position: Posição da porta na tela (x, y)
        size: Tamanho da porta (largura, altura)
    """
    
    def __init__(self, position: Tuple[int, int] = (0, 0), size: Tuple[int, int] = (60, 40),
                 off_color: Tuple[int, int, int] = (128, 128, 128),
                 on_color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Inicializa uma nova porta lógica.
        
        Args:
            position: Posição inicial (x, y) da porta na tela
            size: Tamanho (largura, altura) da porta
            off_color: Cor quando a porta está desligada (R, G, B)
            on_color: Cor quando a porta está ligada (R, G, B)
        """
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
        
        print(f"[{self.__class__.__name__}] Created with off_color: {off_color}, on_color: {on_color}")

    def _initialize(self):
        """
        Inicializa renderers e shaders.
        
        Configura os recursos OpenGL necessários para renderização da porta lógica.
        """
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
            print(f"[{self.__class__.__name__}] Erro ao carregar shaders: {e}")
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
        """
        Cria a textura do texto da porta.
        
        Renderiza o nome da porta em uma superfície pygame e converte
        para textura OpenGL.
        """
        pygame.font.init()
        font_size = min(18, self.size[1] // 4)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        text_surface = font.render(self.__class__.__name__.replace('Gate', ''), True, (255, 255, 255))
        self.create_texture_from_surface(text_surface)

    def _create_gate_quad(self):
        """
        Cria os dados do quad da porta.
        
        Converte coordenadas de tela para OpenGL e cria vértices
        para renderização da porta.
        """
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            self.position[0], self.position[1], self.size[0], self.size[1]
        )
        self.gate_vertices, self.gate_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _create_text_quad(self):
        """
        Cria o quad para o texto centralizado na porta.
        
        Posiciona o texto no centro da porta e cria vértices
        para renderização do texto.
        """
        # Centralizar texto na porta
        text_x = self.position[0] + (self.size[0] - self.text_width) // 2
        text_y = self.position[1] + (self.size[1] - self.text_height) // 2
        
        gl_x, gl_y, gl_width, gl_height = self.screen_to_gl_coords(
            text_x, text_y, self.text_width, self.text_height
        )
        self.text_vertices, self.text_indices = self.create_quad_vertices(gl_x, gl_y, gl_width, gl_height)

    def _update(self, delta_time):
        """
        Atualização específica da porta lógica.
        
        Recalcula o resultado lógico a cada frame para garantir que
        mudanças nas entradas sejam refletidas imediatamente.
        
        Args:
            delta_time: Tempo desde o último frame em segundos
        """
        # Recalcular resultado para manter estado atualizado
        self.get_result()

    def _render(self, renderer):
        """
        Renderização específica da porta lógica.
        
        Renderiza a porta usando a cor apropriada baseada no estado atual.
        
        Args:
            renderer: Renderizador OpenGL
        """
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
                
                # Obter cor de renderização (separado da lógica de estado)
                color = self.get_render_color()
                
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
            print(f"[{self.__class__.__name__}] Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()

    def _calculate_result(self) -> bool:
        """
        Calcula o resultado da porta lógica.
        
        Este método deve ser sobrescrito pelas subclasses para implementar
        a lógica específica de cada tipo de porta (AND, OR, NOT, etc.).
        
        Returns:
            Resultado lógico da porta
        """
        return False

    def add_input(self, input_source: LogicInputSource) -> None:
        """
        Adiciona uma fonte de entrada à porta lógica.
        
        Args:
            input_source: Componente que implementa LogicInputSource
        """
        if isinstance(input_source, LogicInputSource):
            self.inputs.append(input_source)
        else:
            raise TypeError(f"Input source must implement LogicInputSource, got {type(input_source)}")

    def remove_input(self, input_source: LogicInputSource) -> None:
        """
        Remove uma fonte de entrada da porta lógica.
        
        Args:
            input_source: Fonte de entrada a ser removida
        """
        if input_source in self.inputs:
            self.inputs.remove(input_source)

    def get_result(self) -> bool:
        """
        Retorna o resultado lógico atual da porta.
        
        Calcula o resultado baseado nas entradas atuais e na lógica
        específica implementada pela subclasse.
        
        Returns:
            True se a porta está ativa, False caso contrário
        """
        self.output = self._calculate_result()
        return self.output

    def get_render_color(self) -> Tuple[int, int, int]:
        """
        Retorna a cor atual para renderização baseada no estado.
        
        Returns:
            Cor atual (R, G, B) baseada no resultado lógico da porta
        """
        return self.on_color if self.get_result() else self.off_color
    
    def get_position(self) -> Tuple[int, int]:
        """
        Retorna a posição da porta na tela.
        
        Returns:
            Posição (x, y) da porta
        """
        return self.position
    
    def get_size(self) -> Tuple[int, int]:
        """
        Retorna o tamanho da porta.
        
        Returns:
            Tamanho (largura, altura) da porta
        """
        return self.size

    def _destroy(self):
        """
        Destrói recursos OpenGL.
        
        Libera todos os recursos OpenGL associados à porta lógica,
        incluindo renderers e texturas.
        """
        super()._destroy()
        if hasattr(self, 'gate_renderer') and self.gate_renderer:
            self.gate_renderer.cleanup()
        if hasattr(self, 'text_renderer') and self.text_renderer:
            self.text_renderer.cleanup() 