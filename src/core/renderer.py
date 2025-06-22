"""
Renderizador OpenGL moderno unificado
"""

import numpy as np
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Dict, Optional


class ModernRenderer:
    """Renderizador OpenGL moderno - gerencia VAOs, VBOs e shaders"""
    
    def __init__(self):
        """Inicializa o renderizador"""
        self.vaos: Dict[str, int] = {}
        self.vbos: Dict[str, int] = {}
        self.ebos: Dict[str, int] = {}
    
    def create_quad_vao(self, name: str, vertices: np.ndarray, indices: np.ndarray) -> None:
        """Cria VAO para quad com dados específicos"""
        # Criar VAO
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        
        # Criar VBO
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        # Criar EBO
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        # Configurar atributos
        stride = 5 * 4  # 5 floats * 4 bytes por float
        
        # Posição (atributo 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)
        glEnableVertexAttribArray(0)
        
        # Coordenadas de textura (atributo 1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        # Armazenar referências
        self.vaos[name] = vao
        self.vbos[name] = vbo
        self.ebos[name] = ebo
        
        glBindVertexArray(0)
    
    def create_text_vao(self, name: str, width: float, height: float, x: float, y: float) -> None:
        """Cria VAO para texto 2D"""
        # Dados do quad 2D para texto
        vertices = np.array([
            # posições        # coordenadas de textura
            x, y, 0.0,        0.0, 1.0,  # topo esquerdo
            x + width, y, 0.0, 1.0, 1.0,  # topo direito
            x + width, y + height, 0.0, 1.0, 0.0,  # baixo direito
            x, y + height, 0.0, 0.0, 0.0   # baixo esquerdo
        ], dtype=np.float32).reshape((4, 5))
        
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        
        self.create_quad_vao(name, vertices, indices)
    
    def render_quad(self, vao_name: str, shader_program: int, texture_id: Optional[int] = None) -> None:
        """Renderiza quad usando VAO"""
        if vao_name not in self.vaos:
            raise ValueError(f"VAO '{vao_name}' não encontrado")
        
        glUseProgram(shader_program)
        
        # Vincular textura se fornecida
        if texture_id is not None:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture_id)
        
        # Renderizar
        glBindVertexArray(self.vaos[vao_name])
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        
        # Limpar
        if texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, 0)
    
    def cleanup(self) -> None:
        """Limpa todos os recursos OpenGL"""
        for vao in self.vaos.values():
            glDeleteVertexArrays(1, [vao])
        for vbo in self.vbos.values():
            glDeleteBuffers(1, [vbo])
        for ebo in self.ebos.values():
            glDeleteBuffers(1, [ebo])
        
        self.vaos.clear()
        self.vbos.clear()
        self.ebos.clear() 