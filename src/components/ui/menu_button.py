"""
Botões de menu clicáveis
"""

import pygame
import numpy as np
from OpenGL.GL import *
from src.components.ui.button_base import ButtonBase


class MenuButton(ButtonBase):
    """Botão de menu retangular com efeitos de hover"""
    
    def __init__(self, text, position, size=(200, 50), color=(100, 150, 255), 
                 hover_color=(150, 200, 255), window_size=(800, 600), 
                 shader_manager=None, callback=None, bg_color=(40, 40, 80), border_color=(180, 180, 220)):
        super().__init__(
            text=text,
            position=position,
            size=size,
            off_color=bg_color,
            on_color=color,
            text_color=color,
            window_size=window_size,
            shader_manager=shader_manager,
            callback=callback,
            button_type="rectangle"
        )
        self.hover_color = hover_color
        self.border_color = border_color

    def handle_mouse_event(self, event):
        """Processa eventos do mouse para botão de menu"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if self._check_hover(mouse_x, mouse_y):
                self.is_clicked = True
                if self.callback:
                    self.callback()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_clicked = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.is_hovered = self._check_hover(mouse_x, mouse_y)

    def _render(self, renderer):
        """Renderiza botão com efeitos de hover"""
        if self.button_renderer is None or self.text_renderer is None or self.shader_manager is None or not self.shader_ok:
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
            # Renderizar fundo do botão
            button_shader = self.shader_manager.get_program("button")
            if button_shader:
                glUseProgram(button_shader)
                
                # Escolher cor baseada no hover
                color = self.hover_color if self.is_hovered else self.off_color
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(button_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                # Desenhar botão com cor
                glVertexAttrib4f(2, color[0]/255.0, color[1]/255.0, color[2]/255.0, 0.85)
                self.button_renderer.render_quad(self.vao_name, button_shader)
            
            # Renderizar texto
            text_shader = self.shader_manager.get_program("text")
            if text_shader and self.texture_id:
                glUseProgram(text_shader)
                
                # Setar textura
                location = glGetUniformLocation(text_shader, "textTexture")
                if location != -1:
                    glUniform1i(location, 0)
                
                # Aplicar matriz de projeção
                loc_proj = glGetUniformLocation(text_shader, "uProjection")
                if loc_proj != -1:
                    glUniformMatrix4fv(loc_proj, 1, GL_TRUE, ortho)
                
                self.text_renderer.render_quad(self.text_vao_name, text_shader, self.texture_id)
                
        except Exception as e:
            print(f"Erro na renderização: {e}")
        
        finally:
            self._restore_gl_state()

    def _check_hover(self, mouse_x, mouse_y):
        """Verifica se mouse está sobre o botão"""
        x, y = self.position
        width, height = self.size
        # Hover: Pygame usa origem no topo esquerdo
        if (x <= mouse_x <= x + width and y <= mouse_y <= y + height):
            return True
        else:
            return False

    def _destroy(self):
        """Destrói recursos OpenGL"""
        super()._destroy() 