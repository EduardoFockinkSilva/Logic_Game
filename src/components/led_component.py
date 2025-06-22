"""
Componente LED que exibe o estado de uma entrada como um círculo colorido
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_component import Component
from ..graphics.renderer import ModernRenderer
from ..shaders.shader_manager import ShaderManager


class LEDComponent(Component):
    def __init__(self, position, radius=20, 
                 off_color=(64, 64, 64), on_color=(0, 255, 0),
                 window_size=(800, 600), shader_manager=None, 
                 input_source=None):
        super().__init__()
        self.position = position  # (x, y) em coordenadas de tela
        self.radius = radius
        self.off_color = off_color  # Dark gray when off
        self.on_color = on_color    # Green when on
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.input_source = input_source  # Componente que fornece o estado (ex: ANDGate)
        
        print(f"[LEDComponent] Created with off_color: {self.off_color}, on_color: {self.on_color}")
        
        # Recursos OpenGL
        self.led_renderer = None
        self.vao_name = f"led_{id(self)}"
        self.shader_ok = False
        
        # Dados do círculo
        self.circle_vertices = None
        self.circle_indices = None

    def _initialize(self):
        # Inicializar renderer
        self.led_renderer = ModernRenderer()
        
        # Usar o shader manager fornecido ou criar um novo
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
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
        gl_x = (x / self.window_size[0]) * 2 - 1
        gl_y = 1 - ((y + diameter) / self.window_size[1]) * 2
        gl_size = (diameter / self.window_size[0]) * 2
        
        # Criar um quad quadrado que será renderizado como círculo pelo shader
        self.circle_vertices = np.array([
            gl_x, gl_y, 0.0,          0.0, 0.0,  # inferior esquerdo
            gl_x + gl_size, gl_y, 0.0,      1.0, 0.0,  # inferior direito
            gl_x + gl_size, gl_y + gl_size, 0.0, 1.0, 1.0,  # superior direito
            gl_x, gl_y + gl_size, 0.0,      0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        
        self.circle_indices = np.array([
            0, 1, 2, 2, 3, 0
        ], dtype=np.uint32)

    def _update(self, delta_time):
        pass

    def _render(self, renderer):
        if self.led_renderer is None or self.shader_manager is None or not self.shader_ok:
            return
            
        prev_viewport = glGetIntegerv(GL_VIEWPORT)
        prev_blend = glIsEnabled(GL_BLEND)
        prev_depth_test = glIsEnabled(GL_DEPTH_TEST)
        
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        
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
                if is_on:
                    color = self.on_color
                else:
                    color = self.off_color
                
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

    def _get_led_state(self):
        """Obtém o estado atual do LED baseado na fonte de entrada."""
        if self.input_source is None:
            return False
        
        # Se a fonte de entrada tem um método get_result, use-o
        if hasattr(self.input_source, 'get_result'):
            return self.input_source.get_result()
        
        # Se a fonte de entrada tem um método get_state, use-o
        elif hasattr(self.input_source, 'get_state'):
            return self.input_source.get_state()
        
        # Caso contrário, assuma que está desligado
        return False

    def set_input_source(self, source):
        """Define a fonte de entrada para o LED."""
        self.input_source = source

    def get_state(self):
        """Retorna o estado atual do LED."""
        return self._get_led_state()

    def _destroy(self):
        """Destrói recursos OpenGL."""
        pass 