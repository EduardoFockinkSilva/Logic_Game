"""
Componente LED que exibe o estado de uma entrada como um círculo colorido
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from src.components.base_component import RenderableComponent
import sys
import os
from src.components.interfaces import LogicInputSource, RenderableState
from typing import Tuple

# Adicionar o diretório src ao path para imports absolutos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from graphics.renderer import ModernRenderer
from shaders.shader_manager import ShaderManager


class LEDComponent(RenderableComponent, RenderableState):
    """
    Componente LED que exibe o estado de uma entrada como um círculo colorido.
    Usado para mostrar o resultado de portas lógicas.
    """
    
    def __init__(self, position, radius=20, 
                 off_color=(64, 64, 64), on_color=(0, 255, 0),
                 window_size=(800, 600), shader_manager=None, 
                 input_source: LogicInputSource = None):
        super().__init__(window_size, shader_manager)
        
        self.position = position
        self.radius = radius
        self.off_color = off_color  # Dark gray when off
        self.on_color = on_color    # Green when on
        self.input_source: LogicInputSource = input_source  # Componente que fornece o estado (ex: ANDGate)
        
        print(f"[LEDComponent] Created with off_color: {self.off_color}, on_color: {self.on_color}")
        
        # Recursos OpenGL
        self.led_renderer = None
        self.vao_name = f"led_{id(self)}"
        
        # Dados do círculo
        self.circle_vertices = None
        self.circle_indices = None

    def _initialize(self):
        """Inicializa renderer e shaders."""
        # Inicializar renderer
        self.led_renderer = ModernRenderer()
        
        # Carregar shaders
        try:
            # Load LED shader for perfect circle rendering
            if not self.shader_manager.has_program("led"):
                self.shader_manager.load_shader(
                    "led",
                    "src/shaders/gate_vertex.glsl",
                    "src/shaders/led_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"[LEDComponent] Erro ao carregar shaders: {e}")
            self.shader_ok = False
            return
        
        # Criar dados do círculo
        self._create_circle_quad()
        
        # Criar VAO
        if self.circle_vertices is not None and self.circle_indices is not None:
            self.led_renderer.create_quad_vao(self.vao_name, self.circle_vertices, self.circle_indices)

    def _create_circle_quad(self):
        """Cria os dados do quad circular para o LED."""
        x, y = self.position
        diameter = self.radius * 2
        
        # Converter coordenadas de tela para OpenGL
        gl_x, gl_y, gl_size, _ = self.screen_to_gl_coords(x, y, diameter, diameter)
        
        # Criar um quad quadrado que será renderizado como círculo pelo shader
        self.circle_vertices, self.circle_indices = self.create_quad_vertices(gl_x, gl_y, gl_size, gl_size)

    def _update(self, delta_time):
        pass

    def _render(self, renderer):
        if self.led_renderer is None or self.shader_manager is None or not self.shader_ok:
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
            # Render LED using LED shader
            led_shader = self.shader_manager.get_program("led")
            if led_shader:
                glUseProgram(led_shader)
                
                # Obter estado do LED
                is_on = self._get_led_state()
                
                # Escolher cor baseada no estado
                color = self.get_render_color()
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(led_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar LED com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
                self.led_renderer.render_quad(self.vao_name, led_shader)
                
        except Exception as e:
            print(f"[LEDComponent] Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()

    def _get_led_state(self):
        """Obtém o estado atual do LED baseado na fonte de entrada."""
        if self.input_source is None:
            return False
        
        # Se a fonte de entrada tem um método get_result, use-o primeiro (portas lógicas)
        if hasattr(self.input_source, 'get_result'):
            return self.input_source.get_result()
        
        # Se a fonte de entrada tem um método get_state, use-o (outros componentes)
        elif hasattr(self.input_source, 'get_state'):
            return self.input_source.get_state()
        
        # Caso contrário, assuma que está desligado
        return False

    def set_input_source(self, source: LogicInputSource):
        """Define a fonte de entrada para o LED."""
        self.input_source = source

    def get_state(self):
        """Retorna o estado atual do LED."""
        return self._get_led_state()

    def get_render_color(self) -> Tuple[int, int, int]:
        """
        Retorna a cor atual para renderização baseada no estado do LED.
        Separa a lógica de estado da renderização.
        """
        is_on = self._get_led_state()
        return self.on_color if is_on else self.off_color
    
    def get_position(self) -> Tuple[int, int]:
        """Retorna a posição do LED."""
        return self.position
    
    def get_size(self) -> Tuple[int, int]:
        """Retorna o tamanho do LED (diâmetro)."""
        return (self.radius * 2, self.radius * 2)

    def _destroy(self):
        """Destrói recursos OpenGL."""
        if self.led_renderer:
            self.led_renderer.cleanup() 