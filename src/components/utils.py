"""
Utilitários comuns para componentes
"""

import pygame
from typing import Tuple


def flip_surface(surface: pygame.Surface) -> pygame.Surface:
    """Inverte superfície verticalmente (corrige origem do OpenGL)"""
    return pygame.transform.flip(surface, False, True)


def create_text_surface(text: str, font_size: int, color: Tuple[int, int, int], 
                       bold: bool = True, font_name: str = 'Arial') -> pygame.Surface:
    """Cria superfície de texto com configurações padrão"""
    pygame.font.init()
    font = pygame.font.SysFont(font_name, font_size, bold=bold)
    return font.render(text, True, color)


def calculate_centered_position(text_width: int, text_height: int, 
                               container_width: int, container_height: int) -> Tuple[int, int]:
    """Calcula posição centralizada para texto dentro de container"""
    x = (container_width - text_width) // 2
    y = (container_height - text_height) // 2
    return x, y


def is_point_in_rect(point_x: int, point_y: int, 
                    rect_x: int, rect_y: int, 
                    rect_width: int, rect_height: int) -> bool:
    """Verifica se ponto está dentro de retângulo"""
    return (rect_x <= point_x <= rect_x + rect_width and 
            rect_y <= point_y <= rect_y + rect_height)


def is_point_in_circle(point_x: int, point_y: int,
                      circle_x: int, circle_y: int, radius: int) -> bool:
    """Verifica se ponto está dentro de círculo"""
    distance_squared = (point_x - circle_x) ** 2 + (point_y - circle_y) ** 2
    return distance_squared <= radius ** 2


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Restringe valor entre mínimo e máximo"""
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """Interpolação linear entre dois valores"""
    return start + (end - start) * t 