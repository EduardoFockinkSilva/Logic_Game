"""
Componentes do jogo de lógica

Pacote contendo todos os componentes visuais e lógicos do jogo:
portas lógicas, botões, LEDs, conexões e elementos de interface.
"""

# Componentes base
from .core.base_component import Component, RenderableComponent, TexturedComponent
from .core.interfaces import LogicInputSource, RenderableState

# Portas lógicas
from .logic.logic_gate import LogicGate
from .logic.and_gate import ANDGate
from .logic.or_gate import ORGate
from .logic.not_gate import NOTGate

# Botões
from .ui.button_base import ButtonBase
from .logic.input_button import InputButton
from .ui.menu_button import MenuButton

# Componentes visuais
from .logic.led_component import LEDComponent
from .ui.text_component import TextComponent
from .ui.background_component import BackgroundComponent

# Sistema de conexões
from .ui.connection_component import ConnectionComponent
from .core.connection_manager import ConnectionManager

# Debug
from .ui.debug_hud import DebugHUD

__all__ = [
    # Componentes base
    'Component',
    'RenderableComponent', 
    'TexturedComponent',
    'LogicInputSource',
    'RenderableState',
    
    # Portas lógicas
    'LogicGate',
    'ANDGate',
    'ORGate', 
    'NOTGate',
    
    # Botões
    'ButtonBase',
    'InputButton',
    'MenuButton',
    
    # Componentes visuais
    'LEDComponent',
    'TextComponent',
    'BackgroundComponent',
    
    # Sistema de conexões
    'ConnectionComponent',
    'ConnectionManager',
    
    # Debug
    'DebugHUD',
] 