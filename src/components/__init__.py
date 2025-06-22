"""
Módulo components - Sistema de componentes do jogo
"""

from .base_component import Component, RenderableComponent, TexturedComponent
from .logic_gate import LogicGate
from .button_base import ButtonBase
from .debug_hud import DebugHUD
from .text_component import TextComponent
from .menu_button import MenuButton
from .input_button import InputButton
from .background_component import BackgroundComponent
from .and_gate import ANDGate
from .or_gate import ORGate
from .not_gate import NOTGate
from .led_component import LEDComponent
from .utils import (
    flip_surface, create_text_surface, calculate_centered_position,
    is_point_in_rect, is_point_in_circle, clamp, lerp
)
from .factories import (
    component_registry, register_components, create_logic_gate, create_button
)

# Registrar todos os componentes no registry
register_components()

__all__ = [
    # Componentes base
    'Component',
    'RenderableComponent',
    'TexturedComponent',
    'LogicGate',
    'ButtonBase',
    
    # Componentes específicos
    'DebugHUD', 
    'TextComponent',
    'MenuButton',
    'InputButton',
    'BackgroundComponent',
    'ANDGate',
    'ORGate',
    'NOTGate',
    'LEDComponent',
    
    # Factories e Registry
    'component_registry',
    'create_logic_gate',
    'create_button',
    
    # Utilitários
    'flip_surface',
    'create_text_surface',
    'calculate_centered_position',
    'is_point_in_rect',
    'is_point_in_circle',
    'clamp',
    'lerp'
] 