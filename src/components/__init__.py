"""
Componentes do jogo de lógica.

Este pacote contém todos os componentes visuais e lógicos do jogo,
incluindo portas lógicas, botões, LEDs, conexões e elementos de interface.
"""

# Componentes base
from .base_component import Component, RenderableComponent, TexturedComponent
from .interfaces import LogicInputSource, RenderableState

# Portas lógicas
from .logic_gate import LogicGate
from .and_gate import ANDGate
from .or_gate import ORGate
from .not_gate import NOTGate

# Botões
from .button_base import ButtonBase
from .input_button import InputButton
from .menu_button import MenuButton

# Componentes visuais
from .led_component import LEDComponent
from .text_component import TextComponent
from .background_component import BackgroundComponent

# Sistema de conexões
from .connection_component import ConnectionComponent
from .connection_manager import ConnectionManager

# Utilitários e fábricas
from .utils import *
from .factories import component_registry, register_components, create_logic_gate, create_button

# Debug
from .debug_hud import DebugHUD

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
    
    # Utilitários
    'component_registry',
    'register_components',
    'create_logic_gate',
    'create_button',
    'DebugHUD',
] 