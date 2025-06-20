"""
Componente de background animado usando shaders OpenGL
"""

import numpy as np
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *

from .base_component import Component
from ..shaders.shader_manager import ShaderManager


class BackgroundComponent(Component):
    """
    Componente que renderiza um background animado usando shaders.
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
        self.vao = None
        self.vbo = None
        self.ebo = None
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
        """Inicializa os buffers OpenGL e carrega o shader."""
        # Carregar shader se não foi fornecido
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shader de background
        try:
            self.shader_manager.load_shader(
                "background",
                "src/shaders/background_vertex.glsl",
                "src/shaders/background_fragment.glsl"
            )
        except FileNotFoundError as e:
            print(f"Erro ao carregar shader: {e}")
            return
        
        # Criar VAO (Vertex Array Object)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Criar VBO (Vertex Buffer Object)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # Criar EBO (Element Buffer Object)
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        
        # Configurar atributos do vertex shader
        # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, None)
        glEnableVertexAttribArray(0)
        
        # Coordenadas de textura
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        # Desvincular VAO
        glBindVertexArray(0)
    
    def _update(self, delta_time: float) -> None:
        """Atualiza o tempo para animação."""
        self.time += delta_time
    
    def _render(self, renderer) -> None:
        """Renderiza o background."""
        # Usar shader de background
        try:
            self.shader_manager.use_program("background")
            
            # Definir uniforms
            self.shader_manager.set_uniform_1f("uTime", self.time)
            self.shader_manager.set_uniform_2f("uResolution", 800.0, 600.0)  # TODO: obter da janela
            
            # Renderizar quad
            glBindVertexArray(self.vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
        except Exception as e:
            print(f"Erro ao renderizar background: {e}")
    
    def _destroy(self) -> None:
        """Libera recursos OpenGL."""
        if self.vao is not None:
            glDeleteVertexArrays(1, [self.vao])
        if self.vbo is not None:
            glDeleteBuffers(1, [self.vbo])
        if self.ebo is not None:
            glDeleteBuffers(1, [self.ebo]) 