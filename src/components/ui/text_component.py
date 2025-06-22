"""
Componente para renderizar texto usando OpenGL moderno
"""

import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from src.components.core.base_component import TexturedComponent
from src.core.renderer import ModernRenderer
from src.core.shader_manager import ShaderManager

class TextComponent(TexturedComponent):
    """Componente para renderizar texto usando OpenGL moderno"""
    
    def __init__(self, text, font_size=48, color=(255,255,255), position=(0.5, 0.05), 
                 window_size=(800,600), shader_manager=None, centered=True):
        super().__init__(window_size, shader_manager)
        
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position  # Normalizado (0-1)
        self.centered = centered  # Se o texto deve ser centralizado
        self.renderer = None
        self.vao_name = f"text_{id(self)}"
        self._last_text = None  # Para detectar mudanças no texto

    def _initialize(self):
        """Inicializa renderizador e carrega shader"""
        # Inicializar renderer
        self.renderer = ModernRenderer()
        
        # Carregar shader de texto
        try:
            if not self.shader_manager.has_program("text"):
                self.shader_manager.load_shader(
                    "text",
                    "src/shaders/text_vertex.glsl",
                    "src/shaders/text_fragment.glsl"
                )
            self.shader_ok = True
        except Exception as e:
            print(f"Erro ao carregar shader de texto: {e}")
            self.shader_ok = False
            return
        
        # Criar textura inicial
        self._create_texture()
        self._last_text = self.text
        
        # Calcular posição usando coordenadas normalizadas
        if self.centered:
            # Centralizar o texto
            x = int(self.window_size[0] * self.position[0] - self.text_width // 2)
        else:
            # Usar posição absoluta
            x = int(self.window_size[0] * self.position[0])
        
        y = int(self.window_size[1] * self.position[1])
        
        # Criar VAO para o texto
        self.renderer.create_text_vao(self.vao_name, self.text_width, self.text_height, x, y)

    def _create_texture(self):
        """Cria textura do texto"""
        pygame.font.init()
        font = pygame.font.SysFont('Arial', self.font_size, bold=True)
        text_surface = font.render(self.text, True, self.color)
        self.create_texture_from_surface(text_surface)

    def _update_texture_if_needed(self):
        """Recria textura se texto mudou"""
        if self.text != self._last_text:
            self._create_texture()
            self._last_text = self.text
            
            # Recalcular posição e recriar VAO
            if self.centered:
                # Centralizar o texto
                x = int(self.window_size[0] * self.position[0] - self.text_width // 2)
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
            self.renderer.create_text_vao(self.vao_name, self.text_width, self.text_height, x, y)

    def _update(self, delta_time):
        """Verifica se texto mudou e atualiza textura se necessário"""
        self._update_texture_if_needed()

    def _render(self, renderer):
        if self.renderer is None or self.shader_manager is None or not self.shader_ok:
            return
        
        self._setup_gl_state()
        
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
            print(f"Erro ao renderizar texto: {e}")
        finally:
            self._restore_gl_state()

    def _destroy(self):
        """Libera recursos OpenGL"""
        super()._destroy()
        if self.renderer:
            self.renderer.cleanup() 