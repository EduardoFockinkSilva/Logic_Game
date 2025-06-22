"""
Componente para renderizar conexões visuais entre componentes lógicos

Implementa sistema de conexões que desenha linhas entre componentes
e muda de cor baseado no estado do sinal que está sendo transmitido
através da conexão.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from src.components.core.base_component import RenderableComponent
from src.components.core.interfaces import LogicInputSource, RenderableState
from typing import Tuple, Optional

from src.core.renderer import ModernRenderer
from src.core.shader_manager import ShaderManager


class ConnectionComponent(RenderableComponent, RenderableState):
    """Componente que renderiza conexões visuais entre componentes lógicos"""
    
    def __init__(self, start_point: Tuple[int, int], end_point: Tuple[int, int],
                 signal_source: Optional[LogicInputSource] = None,
                 off_color: Tuple[int, int, int] = (64, 64, 64),
                 on_color: Tuple[int, int, int] = (0, 255, 0),
                 line_width: int = 3,
                 connection_type: str = 'straight',
                 window_size: Tuple[int, int] = (800, 600),
                 shader_manager=None):
        """Inicializa nova conexão"""
        super().__init__(window_size, shader_manager)
        
        self.start_point = start_point
        self.end_point = end_point
        self.signal_source = signal_source
        self.off_color = off_color
        self.on_color = on_color
        self.line_width = line_width
        self.connection_type = connection_type
        
        # Recursos OpenGL
        self.connection_renderer = None
        self.vao_name = f"connection_{id(self)}"
        
        # Dados da linha
        self.line_vertices = None
        self.line_indices = None
        
        # Estado de renderização
        self.visible = True
        self.enabled = True
        
        print(f"Conexão criada de {start_point} para {end_point}")
    
    def _initialize(self):
        """Inicializa renderer e shaders para conexões"""
        # Inicializar renderer
        self.connection_renderer = ModernRenderer()
        
        # Carregar shaders
        try:
            # Load connection shader
            if not self.shader_manager.has_program("connection"):
                self.shader_manager.load_shader(
                    "connection",
                    "src/shaders/gate_vertex.glsl",
                    "src/shaders/gate_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"Erro ao carregar shaders: {e}")
            self.shader_ok = False
            return
        
        # Criar dados da linha
        self._create_line_geometry()
        
        # Criar VAO
        if self.line_vertices is not None and self.line_indices is not None:
            self.connection_renderer.create_quad_vao(self.vao_name, self.line_vertices, self.line_indices)
    
    def _create_line_geometry(self):
        """Cria geometria da linha baseada no tipo de conexão"""
        if self.connection_type == 'straight':
            self._create_straight_line()
        elif self.connection_type == 'stepped':
            self._create_stepped_line()
        elif self.connection_type == 'curved':
            self._create_curved_line()
        else:
            self._create_straight_line()  # Fallback
    
    def _create_straight_line(self):
        """Cria geometria para linha reta"""
        # Converter pontos para coordenadas OpenGL
        start_gl = self._screen_to_gl_point(self.start_point)
        end_gl = self._screen_to_gl_point(self.end_point)
        
        # Calcular vetor da linha
        line_vector = (end_gl[0] - start_gl[0], end_gl[1] - start_gl[1])
        line_length = np.sqrt(line_vector[0]**2 + line_vector[1]**2)
        
        # Normalizar e calcular perpendicular para espessura
        if line_length > 0:
            normalized = (line_vector[0] / line_length, line_vector[1] / line_length)
            perpendicular = (-normalized[1], normalized[0])
        else:
            perpendicular = (0, 1)
        
        # Calcular espessura em coordenadas OpenGL
        thickness_gl = (self.line_width / self.window_size[0]) * 2
        
        # Criar retângulo ao longo da linha
        p1 = (start_gl[0] + perpendicular[0] * thickness_gl, start_gl[1] + perpendicular[1] * thickness_gl)
        p2 = (start_gl[0] - perpendicular[0] * thickness_gl, start_gl[1] - perpendicular[1] * thickness_gl)
        p3 = (end_gl[0] - perpendicular[0] * thickness_gl, end_gl[1] - perpendicular[1] * thickness_gl)
        p4 = (end_gl[0] + perpendicular[0] * thickness_gl, end_gl[1] + perpendicular[1] * thickness_gl)
        
        # Criar vértices (posição + coordenadas de textura)
        self.line_vertices = np.array([
            p1[0], p1[1], 0.0, 0.0, 0.0,  # inferior esquerdo
            p2[0], p2[1], 0.0, 1.0, 0.0,  # inferior direito
            p3[0], p3[1], 0.0, 1.0, 1.0,  # superior direito
            p4[0], p4[1], 0.0, 0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        
        self.line_indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
    
    def _create_stepped_line(self):
        """Cria geometria para linha em degraus (para conexões ortogonais)"""
        # Implementação simplificada - linha reta por enquanto
        self._create_straight_line()
    
    def _create_curved_line(self):
        """Cria geometria para linha curva (para conexões suaves)"""
        # Implementação simplificada - linha reta por enquanto
        self._create_straight_line()
    
    def _screen_to_gl_point(self, point: Tuple[int, int]) -> Tuple[float, float]:
        """Converte ponto de tela para coordenadas OpenGL"""
        gl_x = (point[0] / self.window_size[0]) * 2 - 1
        gl_y = 1 - (point[1] / self.window_size[1]) * 2
        return (gl_x, gl_y)
    
    def _update(self, delta_time: float):
        """Atualização específica da conexão"""
        # A conexão não precisa de atualização específica
        # O estado é determinado pela fonte do sinal
        pass
    
    def _render(self, renderer):
        """Renderização específica da conexão"""
        if self.connection_renderer is None or self.shader_manager is None or not self.shader_ok:
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
            # Renderizar conexão usando shader connection
            connection_shader = self.shader_manager.get_program("connection")
            if connection_shader:
                glUseProgram(connection_shader)
                
                # Obter cor baseada no estado do sinal
                color = self.get_render_color()
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(connection_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar conexão com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 1.0)
                self.connection_renderer.render_quad(self.vao_name, connection_shader)
                
        except Exception as e:
            print(f"Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()
    
    def get_render_color(self) -> Tuple[int, int, int]:
        """Retorna cor atual para renderização baseada no estado do sinal"""
        if self.signal_source is None:
            return self.off_color
        
        # Verificar se há sinal
        has_signal = False
        if hasattr(self.signal_source, 'get_result'):
            has_signal = self.signal_source.get_result()
        elif hasattr(self.signal_source, 'get_state'):
            has_signal = self.signal_source.get_state()
        
        return self.on_color if has_signal else self.off_color
    
    def get_position(self) -> Tuple[int, int]:
        """Retorna posição central da conexão"""
        center_x = (self.start_point[0] + self.end_point[0]) // 2
        center_y = (self.start_point[1] + self.end_point[1]) // 2
        return (center_x, center_y)
    
    def get_size(self) -> Tuple[int, int]:
        """Retorna tamanho da conexão"""
        width = abs(self.end_point[0] - self.start_point[0])
        height = abs(self.end_point[1] - self.start_point[1])
        return (width, height)
    
    def set_signal_source(self, source: LogicInputSource):
        """Define fonte do sinal para a conexão"""
        self.signal_source = source
    
    def update_points(self, start_point: Tuple[int, int], end_point: Tuple[int, int]):
        """Atualiza pontos de início e fim da conexão"""
        self.start_point = start_point
        self.end_point = end_point
        
        # Recriar geometria se já inicializado
        if self._initialized:
            self._create_line_geometry()
            if self.line_vertices is not None and self.line_indices is not None:
                self.connection_renderer.create_quad_vao(self.vao_name, self.line_vertices, self.line_indices)
    
    def _destroy(self):
        """Destrói recursos OpenGL da conexão"""
        if hasattr(self, 'connection_renderer') and self.connection_renderer:
            self.connection_renderer.cleanup() 