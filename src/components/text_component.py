"""
Componente para renderizar texto usando OpenGL moderno
"""

import pygame
import numpy as np
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_component import Component
from ..graphics.renderer import ModernRenderer
from ..shaders.shader_manager import ShaderManager


class TextComponent(Component):
    def __init__(self, text, font_size=48, color=(255,255,255), position=(0.5, 0.05), window_size=(800,600), shader_manager=None):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position  # Normalizado (0-1)
        self.window_size = window_size
        self.texture_id = None
        self.width = 0
        self.height = 0
        self.renderer = None
        self.shader_manager = shader_manager  # Usar o shader manager do GameEngine
        self.vao_name = f"text_{id(self)}"
        self.shader_ok = False
        self._texture_created = False

    def initialize(self):
        print("[TextComponent] Chamou initialize()")
        super().initialize()

    def _initialize(self):
        print("[TextComponent] Inicializando...")
        
        # Usar o renderer do GameEngine ou criar um novo
        self.renderer = ModernRenderer()
        
        # Usar o shader manager fornecido ou criar um novo
        if self.shader_manager is None:
            self.shader_manager = ShaderManager()
        
        # Carregar shader de texto apenas se não foi carregado antes
        try:
            if not self.shader_manager.has_program("text"):
                program = self.shader_manager.load_shader(
                    "text",
                    "src/shaders/text_vertex.glsl",
                    "src/shaders/text_fragment.glsl"
                )
                print(f"[TextComponent] Shader de texto carregado: {program}")
            else:
                print("[TextComponent] Shader de texto já carregado")
            self.shader_ok = True
        except Exception as e:
            print(f"[TextComponent] Erro ao carregar shader de texto: {e}")
            self.shader_ok = False
            return
        
        # Criar textura do texto apenas uma vez
        if not self._texture_created:
            self._create_texture()
            self._texture_created = True
        
        # Calcular posição centralizada
        x = (self.window_size[0] - self.width) // 2
        y = int(self.window_size[1] * self.position[1])
        print(f"[TextComponent] Posição do texto: x={x}, y={y}")
        
        # Criar VAO para o texto
        self.renderer.create_text_vao(self.vao_name, self.width, self.height, x, y)
        print(f"[TextComponent] VAO criado: {self.vao_name}")

    def _create_texture(self):
        """Cria a textura do texto."""
        pygame.font.init()
        font = pygame.font.SysFont('Arial', self.font_size, bold=True)
        text_surface = font.render(self.text, True, self.color)
        self.width, self.height = text_surface.get_size()
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        # Criar textura OpenGL
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        print(f"[TextComponent] Textura criada: {self.texture_id}, tamanho: {self.width}x{self.height}")

    def _update(self, delta_time):
        pass

    def _render(self, renderer):
        print("[TextComponent] Chamou _render()")
        if self.renderer is None or self.shader_manager is None or not self.shader_ok:
            print("[TextComponent] Renderer ou shader não inicializado corretamente.")
            return
        
        # Salvar estado OpenGL atual
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glPushMatrix()
        
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
                    print(f"[TextComponent] Uniform 'textTexture' setado em {location}")
                else:
                    print("[TextComponent] Uniform 'textTexture' não encontrado!")
                
                loc_proj = glGetUniformLocation(shader_program, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                    print(f"[TextComponent] Uniform 'uProjection' setado em {loc_proj}")
                else:
                    print("[TextComponent] Uniform 'uProjection' não encontrado!")
                
                print(f"[TextComponent] Renderizando quad VAO: {self.vao_name}, shader: {shader_program}, textura: {self.texture_id}")
                self.renderer.render_quad(self.vao_name, shader_program, self.texture_id)
            else:
                print("[TextComponent] Shader program não encontrado!")
        except Exception as e:
            print(f"[TextComponent] Erro ao renderizar texto: {e}")
        finally:
            # Restaurar estado OpenGL
            glPopMatrix()
            glPopAttrib()

    def _destroy(self):
        if self.texture_id:
            glDeleteTextures([self.texture_id])
        if self.renderer:
            self.renderer.cleanup() 