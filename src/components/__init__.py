"""
Módulo components - Sistema de componentes do jogo
"""

from .base_component import Component
from .debug_hud import DebugHUD
from .text_component import TextComponent
from .menu_button import MenuButton
from .background_component import BackgroundComponent

__all__ = [
    'Component',
    'DebugHUD', 
    'TextComponent',
    'MenuButton',
    'BackgroundComponent'
] 