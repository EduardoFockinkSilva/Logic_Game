"""
Botões de menu clicáveis
"""

import pygame
import numpy as np
from OpenGL.GL import *
from src.components.ui.button_base import ButtonBase
from src.core.renderer import ModernRenderer
from src.core.shader_manager import ShaderManager
from config.style import Colors, ComponentStyle


class MenuButton(ButtonBase):
    """Botão de menu retangular com efeitos de hover e aparência 3D"""
    
    def __init__(self, text, position, size=ComponentStyle.DEFAULT_MENU_BUTTON_SIZE, 
                 color=Colors.TEXT_WHITE, hover_color=Colors.MENU_BUTTON_HOVER, 
                 window_size=(800, 600), shader_manager=None, callback=None, 
                 bg_color=Colors.MENU_BUTTON_BG, border_color=Colors.MENU_BUTTON_BORDER):
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
        """Renderiza botão com efeitos 3D e hover"""
        if self.shader_manager is None or not self.shader_ok:
            return
            
        self._setup_gl_state()
        
        # Converter coordenadas da tela para OpenGL (canto superior esquerdo)
        x, y = self.position
        width, height = self.size
        win_w, win_h = self.window_size

        # OpenGL: origem no centro, Y invertido em relação ao Pygame
        # Pygame (x, y) = canto superior esquerdo
        # OpenGL (gl_x, gl_y) = canto inferior esquerdo
        # Precisamos converter:
        #   - gl_x = (x / win_w) * 2 - 1
        #   - gl_y = 1 - ((y + height) / win_h) * 2
        gl_x = (x / win_w) * 2 - 1
        gl_y = 1 - ((y + height) / win_h) * 2
        gl_width = (width / win_w) * 2
        gl_height = (height / win_h) * 2
        
        # Definir cores para efeito 3D
        base_color = self.hover_color if self.is_hovered else self.off_color
        light_color = tuple(min(255, c + 80) for c in base_color)  # Mais claro
        dark_color = tuple(max(0, c - 80) for c in base_color)     # Mais escuro
        
        # Normalizar cores para OpenGL (0-1)
        base_color_gl = (base_color[0]/255.0, base_color[1]/255.0, base_color[2]/255.0)
        light_color_gl = (light_color[0]/255.0, light_color[1]/255.0, light_color[2]/255.0)
        dark_color_gl = (dark_color[0]/255.0, dark_color[1]/255.0, dark_color[2]/255.0)
        
        # Desabilitar shaders para renderização OpenGL direta
        glUseProgram(0)
        
        # Desabilitar texturas
        glDisable(GL_TEXTURE_2D)
        
        # Configurar projeção ortográfica
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Bevel size (5 pixels convertido para coordenadas OpenGL)
        bevel_size = (5 / self.window_size[0]) * 2
        
        # Ajustar bevel para ser mais visível
        bevel_size = max(bevel_size, 0.02)  # Mínimo de 2% da largura da tela
        
        try:
            # Base do botão
            glColor3fv(base_color_gl)
            glBegin(GL_QUADS)
            glVertex2f(gl_x, gl_y)
            glVertex2f(gl_x + gl_width, gl_y)
            glVertex2f(gl_x + gl_width, gl_y + gl_height)
            glVertex2f(gl_x, gl_y + gl_height)
            glEnd()

            # Top-left light bevel
            glColor3fv(light_color_gl)
            glBegin(GL_QUADS)
            glVertex2f(gl_x, gl_y + gl_height)              # topo esquerdo
            glVertex2f(gl_x + gl_width, gl_y + gl_height)   # topo direito
            glVertex2f(gl_x + gl_width - bevel_size, gl_y + gl_height - bevel_size)
            glVertex2f(gl_x + bevel_size, gl_y + gl_height - bevel_size)
            glEnd()

            glBegin(GL_QUADS)
            glVertex2f(gl_x, gl_y + gl_height)
            glVertex2f(gl_x + bevel_size, gl_y + gl_height - bevel_size)
            glVertex2f(gl_x + bevel_size, gl_y + bevel_size)
            glVertex2f(gl_x, gl_y)
            glEnd()

            # Bottom-right dark bevel
            glColor3fv(dark_color_gl)
            glBegin(GL_QUADS)
            glVertex2f(gl_x + gl_width, gl_y)
            glVertex2f(gl_x + gl_width - bevel_size, gl_y + bevel_size)
            glVertex2f(gl_x + gl_width - bevel_size, gl_y + gl_height - bevel_size)
            glVertex2f(gl_x + gl_width, gl_y + gl_height)
            glEnd()

            glBegin(GL_QUADS)
            glVertex2f(gl_x, gl_y)
            glVertex2f(gl_x + gl_width, gl_y)
            glVertex2f(gl_x + gl_width - bevel_size, gl_y + bevel_size)
            glVertex2f(gl_x + bevel_size, gl_y + bevel_size)
            glEnd()
            
            # Debug: verificar se a renderização 3D foi executada
            print(f"MenuButton 3D renderizado: pos=({self.position}), size=({self.size}), hover={self.is_hovered}")
            
        except Exception as e:
            print(f"Erro na renderização 3D: {e}")
        
        finally:
            # Restaurar matrizes
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            
            # Restaurar cor
            glColor3f(1.0, 1.0, 1.0)
            
            # Reabilitar texturas
            glEnable(GL_TEXTURE_2D)
        
        # Renderizar texto usando o sistema de shaders existente
        self._render_text()
        
        self._restore_gl_state()

    def _render_text(self):
        """Renderiza o texto do botão usando shaders"""
        if self.text_renderer is None or self.shader_manager is None or not self.texture_id:
            return
            
        # Matriz de projeção ortográfica
        ortho = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        try:
            # Renderizar texto
            text_shader = self.shader_manager.get_program("text")
            if text_shader:
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
            print(f"Erro na renderização do texto: {e}")

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