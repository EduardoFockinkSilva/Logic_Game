"""
Componente de background animado usando shaders OpenGL moderno
"""

import numpy as np
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *

from src.components.base_component import Component
import sys
import os

# Adicionar o diretório src ao path para imports absolutos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shaders.shader_manager import ShaderManager
from graphics.renderer import ModernRenderer


class BackgroundComponent(Component):
    """
    Componente que renderiza um background animado usando shaders modernos.
    """
    
    def __init__(self, entity=None, shader_manager: ShaderManager = None):
        """
        Inicializa o componente de background.
        
        Args:
            entity: Entidade pai
            shader_manager: Gerenciador de shaders
        """
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
        """Inicializa o renderizador e carrega o shader."""
        # Inicializar renderer
        self.renderer = ModernRenderer()
        
        # Carregar shader se não foi fornecido
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shader de background apenas se não foi carregado antes
        try:
            if not self.shader_manager.has_program("background"):
                self.shader_manager.load_shader(
                    "background",
                    "src/shaders/background_vertex.glsl",
                    "src/shaders/background_fragment.glsl"
                )
        except FileNotFoundError as e:
            print(f"[BackgroundComponent] Erro ao carregar shader: {e}")
            return
        
        # Criar VAO para o background
        self.renderer.create_quad_vao("background", self.vertices, self.indices)
    
    def _update(self, delta_time: float) -> None:
        """Atualiza o tempo para animação."""
        self.time += delta_time
    
    def _render(self, renderer) -> None:
        """Renderiza o background usando renderizador moderno."""
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
            self.shader_manager.set_uniform_2f("uResolution", 800.0, 600.0)
            
            # Renderizar usando renderer moderno
            self.renderer.render_quad("background", shader_program)
            
        except Exception as e:
            print(f"[BackgroundComponent] Erro ao renderizar background: {e}")
        finally:
            glUseProgram(0)
    
    def _destroy(self) -> None:
        """Libera recursos OpenGL."""
        if self.renderer:
            self.renderer.cleanup() 