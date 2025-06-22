"""
Componente de background animado usando shaders OpenGL
"""

import numpy as np
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *

from src.components.core.base_component import Component
from src.core.shader_manager import ShaderManager
from src.core.renderer import ModernRenderer
from config import WindowConfig

class BackgroundComponent(Component):
    """Componente que renderiza background animado usando shaders modernos"""
    
    def __init__(self, entity=None, shader_manager=None):
        """Inicializa componente de background"""
        super().__init__(entity)
        self.shader_manager = shader_manager
        self.renderer = None
        self.time = 0.0
        
        # Dados do quad que cobre toda a tela
        self.vertices = np.array([
            # posições        # coordenadas de textura
            -1.0, -1.0, 0.0,  0.0, 0.0,  # inferior esquerdo
             1.0, -1.0, 0.0,  1.0, 0.0,  # inferior direito
             1.0,  1.0, 0.0,  1.0, 1.0,  # superior direito
            -1.0,  1.0, 0.0,  0.0, 1.0   # superior esquerdo
        ], dtype=np.float32)
        
        self.indices = np.array([
            0, 1, 2,  # primeiro triângulo
            2, 3, 0   # segundo triângulo
        ], dtype=np.uint32)
    
    def _initialize(self) -> None:
        """Inicializa renderizador e carrega shader"""
        # Inicializar renderer
        self.renderer = ModernRenderer()
        
        # Carregar shader se não foi fornecido
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shader de background
        try:
            if not self.shader_manager.has_program("background"):
                self.shader_manager.load_shader(
                    "background",
                    "src/shaders/background_vertex.glsl",
                    "src/shaders/background_fragment.glsl"
                )
        except FileNotFoundError as e:
            print(f"Erro ao carregar shader: {e}")
            return
        
        # Criar VAO para o background
        self.renderer.create_quad_vao("background", self.vertices, self.indices)
    
    def _update(self, delta_time: float) -> None:
        """Atualiza tempo para animação"""
        self.time += delta_time
    
    def _render(self, renderer) -> None:
        """Renderiza background usando renderizador moderno"""
        if self.renderer is None or self.shader_manager is None:
            return
            
        try:
            # Obter programa de shader
            shader_program = self.shader_manager.get_program("background")
            if not shader_program:
                return
                
            # Definir uniforms
            self.shader_manager.use_program("background")
            self.shader_manager.set_uniform_1f("uTime", self.time)
            self.shader_manager.set_uniform_2f("uResolution", 
                                              float(WindowConfig.DEFAULT_WIDTH), 
                                              float(WindowConfig.DEFAULT_HEIGHT))
            
            # Renderizar usando renderer moderno
            self.renderer.render_quad("background", shader_program)
            
        except Exception as e:
            print(f"Erro ao renderizar background: {e}")
        finally:
            glUseProgram(0)
    
    def _destroy(self) -> None:
        """Libera recursos OpenGL"""
        if self.renderer:
            self.renderer.cleanup() 