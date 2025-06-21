"""
Componente para renderizar texto usando OpenGL moderno
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_component import Component
from ..graphics.renderer import ModernRenderer
from ..shaders.shader_manager import ShaderManager


class TextComponent(Component):
    def __init__(self, text, font_size=48, color=(255,255,255), position=(0.5, 0.05), window_size=(800,600), shader_manager=None, centered=True):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position  # Normalizado (0-1)
        self.window_size = window_size
        self.centered = centered  # Se o texto deve ser centralizado
        self.texture_id = None
        self.width = 0
        self.height = 0
        self.renderer = None
        self.shader_manager = shader_manager
        self.vao_name = f"text_{id(self)}"
        self.shader_ok = False
        self._texture_created = False
        self._last_text = None  # Para detectar mudanças no texto

    def initialize(self):
        super().initialize()

    def _initialize(self):
        # Inicializar renderer
        self.renderer = ModernRenderer()
        
        # Usar o shader manager fornecido ou criar um novo
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shader de texto apenas se não foi carregado antes
        try:
            if not self.shader_manager.has_program("text"):
                self.shader_manager.load_shader(
                    "text",
                    "src/shaders/text_vertex.glsl",
                    "src/shaders/text_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"[TextComponent] Erro ao carregar shader de texto: {e}")
            self.shader_ok = False
            return
        
        # Criar textura inicial
        self._create_texture()
        self._last_text = self.text
        
        # Calcular posição usando coordenadas normalizadas
        if self.centered:
            # Centralizar o texto
            x = int(self.window_size[0] * self.position[0] - self.width // 2)
        else:
            # Usar posição absoluta
            x = int(self.window_size[0] * self.position[0])
        
        y = int(self.window_size[1] * self.position[1])
        
        # Criar VAO para o texto
        self.renderer.create_text_vao(self.vao_name, self.width, self.height, x, y)

    def _create_texture(self):
        """Cria a textura do texto."""
        pygame.font.init()
        font = pygame.font.SysFont('Arial', self.font_size, bold=True)
        text_surface = font.render(self.text, True, self.color)
        self.width, self.height = text_surface.get_size()
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        # Deletar textura anterior se existir
        if self.texture_id:
            glDeleteTextures([self.texture_id])

        # Criar textura OpenGL
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

    def _update_texture_if_needed(self):
        """Recria a textura se o texto mudou."""
        if self.text != self._last_text:
            self._create_texture()
            self._last_text = self.text
            
            # Recalcular posição e recriar VAO
            if self.centered:
                # Centralizar o texto
                x = int(self.window_size[0] * self.position[0] - self.width // 2)
            else:
                # Usar posição absoluta
                x = int(self.window_size[0] * self.position[0])
            
            y = int(self.window_size[1] * self.position[1])
            
            # Limpar VAO anterior
            if self.vao_name in self.renderer.vaos:
                glDeleteVertexArrays(1, [self.renderer.vaos[self.vao_name]])
                glDeleteBuffers(1, [self.renderer.vbos[self.vao_name]])
                glDeleteBuffers(1, [self.renderer.ebos[self.vao_name]])
                del self.renderer.vaos[self.vao_name]
                del self.renderer.vbos[self.vao_name]
                del self.renderer.ebos[self.vao_name]
            
            # Criar novo VAO
            self.renderer.create_text_vao(self.vao_name, self.width, self.height, x, y)

    def _update(self, delta_time):
        # Verificar se o texto mudou e atualizar textura se necessário
        self._update_texture_if_needed()

    def _render(self, renderer):
        if self.renderer is None or self.shader_manager is None or not self.shader_ok:
            return
        
        # Salvar estado OpenGL atual (compatível com OpenGL 3.3+)
        prev_viewport = glGetIntegerv(GL_VIEWPORT)
        prev_blend = glIsEnabled(GL_BLEND)
        prev_depth_test = glIsEnabled(GL_DEPTH_TEST)
        
        # Configurar para renderização 2D
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        
        # Matriz de projeção ortográfica
        left, right = 0, self.window_size[0]
        top, bottom = 0, self.window_size[1]
        near, far = -1, 1
        ortho = np.array([
            [2/(right-left), 0, 0, -(right+left)/(right-left)],
            [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
            [0, 0, -2/(far-near), -(far+near)/(far-near)],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        try:
            shader_program = self.shader_manager.get_program("text")
            if shader_program:
                glUseProgram(shader_program)
                
                # Setar uniforms
                location = glGetUniformLocation(shader_program, "textTexture")
                if location != -1:
                    glUniform1i(location, 0)
                
                loc_proj = glGetUniformLocation(shader_program, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                self.renderer.render_quad(self.vao_name, shader_program, self.texture_id)
        except Exception as e:
            print(f"[TextComponent] Erro ao renderizar texto: {e}")
        finally:
            # Restaurar estado OpenGL
            glViewport(prev_viewport[0], prev_viewport[1], prev_viewport[2], prev_viewport[3])
            if prev_blend:
                glEnable(GL_BLEND)
            else:
                glDisable(GL_BLEND)
            if prev_depth_test:
                glEnable(GL_DEPTH_TEST)
            else:
                glDisable(GL_DEPTH_TEST)

    def _destroy(self):
        if self.texture_id:
            glDeleteTextures([self.texture_id])
        if self.renderer:
            self.renderer.cleanup() 