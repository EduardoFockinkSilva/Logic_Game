"""
Botão de entrada alternável on/off
"""

import pygame
from src.components.ui.button_base import ButtonBase


class InputButton(ButtonBase):
    """Botão de entrada alternável - usado como entrada para portas lógicas"""
    
    def __init__(self, text, position, size=(80, 80), 
                 off_color=(255, 0, 0), on_color=(0, 255, 0),
                 text_color=(255, 255, 255), window_size=(800, 600), 
                 shader_manager=None, initial_state=False):
        super().__init__(
            text=text,
            position=position,
            size=size,
            off_color=off_color,
            on_color=on_color,
            text_color=text_color,
            window_size=window_size,
            shader_manager=shader_manager,
            initial_state=initial_state,
            button_type="circle"
        )

    def handle_mouse_event(self, event):
        """Processa eventos do mouse para alternar estado"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if self._check_hover(mouse_x, mouse_y):
                self.state = not self.state
                self.is_clicked = True
                if self.callback:
                    self.callback(self.state)
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_clicked = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.is_hovered = self._check_hover(mouse_x, mouse_y)
        return False

    def get_result(self) -> bool:
        """Retorna estado lógico do botão"""
        return self.state 