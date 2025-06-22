"""
Utilitários comuns para componentes
"""

import pygame
from typing import Tuple


def flip_surface(surface: pygame.Surface) -> pygame.Surface:
    """
    Inverte a superfície verticalmente (corrige origem do OpenGL).
    
    Args:
        surface: Superfície pygame para inverter
        
    Returns:
        Superfície invertida
    """
    return pygame.transform.flip(surface, False, True)


def create_text_surface(text: str, font_size: int, color: Tuple[int, int, int], 
                       bold: bool = True, font_name: str = 'Arial') -> pygame.Surface:
    """
    Cria uma superfície de texto com configurações padrão.
    
    Args:
        text: Texto a renderizar
        font_size: Tamanho da fonte
        color: Cor do texto (R, G, B)
        bold: Se deve usar fonte em negrito
        font_name: Nome da fonte
        
    Returns:
        Superfície pygame com o texto renderizado
    """
    pygame.font.init()
    font = pygame.font.SysFont(font_name, font_size, bold=bold)
    return font.render(text, True, color)


def calculate_centered_position(text_width: int, text_height: int, 
                               container_width: int, container_height: int) -> Tuple[int, int]:
    """
    Calcula a posição centralizada para um texto dentro de um container.
    
    Args:
        text_width: Largura do texto
        text_height: Altura do texto
        container_width: Largura do container
        container_height: Altura do container
        
    Returns:
        Tupla (x, y) com a posição centralizada
    """
    x = (container_width - text_width) // 2
    y = (container_height - text_height) // 2
    return x, y


def is_point_in_rect(point_x: int, point_y: int, 
                    rect_x: int, rect_y: int, 
                    rect_width: int, rect_height: int) -> bool:
    """
    Verifica se um ponto está dentro de um retângulo.
    
    Args:
        point_x, point_y: Coordenadas do ponto
        rect_x, rect_y: Posição do retângulo
        rect_width, rect_height: Dimensões do retângulo
        
    Returns:
        True se o ponto está dentro do retângulo
    """
    return (rect_x <= point_x <= rect_x + rect_width and 
            rect_y <= point_y <= rect_y + rect_height)


def is_point_in_circle(point_x: int, point_y: int,
                      circle_x: int, circle_y: int, radius: int) -> bool:
    """
    Verifica se um ponto está dentro de um círculo.
    
    Args:
        point_x, point_y: Coordenadas do ponto
        circle_x, circle_y: Centro do círculo
        radius: Raio do círculo
        
    Returns:
        True se o ponto está dentro do círculo
    """
    distance_squared = (point_x - circle_x) ** 2 + (point_y - circle_y) ** 2
    return distance_squared <= radius ** 2


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Restringe um valor entre um mínimo e máximo.
    
    Args:
        value: Valor a restringir
        min_value: Valor mínimo
        max_value: Valor máximo
        
    Returns:
        Valor restringido
    """
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """
    Interpolação linear entre dois valores.
    
    Args:
        start: Valor inicial
        end: Valor final
        t: Fator de interpolação (0-1)
        
    Returns:
        Valor interpolado
    """
    return start + (end - start) * t 