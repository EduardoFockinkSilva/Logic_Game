"""
Sistema de Fábricas para Criação de Componentes

Implementa o padrão Factory para criação centralizada de componentes,
permitindo registro dinâmico de novos tipos e facilitando extensibilidade.

O sistema usa um registro global que mapeia tipos de componentes para suas
classes construtoras, permitindo criação dinâmica baseada em configurações
JSON ou outros formatos de dados.

Examples:
    >>> # Registro de componentes
    >>> from .and_gate import ANDGate
    >>> component_registry.register_logic_gate('AND', ANDGate)
    >>> 
    >>> # Criação via fábrica
    >>> gate = create_logic_gate('AND', position=(100, 100))
    >>> isinstance(gate, ANDGate)  # True
"""

from typing import Dict, Type, Any, Optional, Tuple
from src.components.core.interfaces import LogicInputSource
from src.components.logic.logic_gate import LogicGate
from src.components.ui.button_base import ButtonBase
from src.components.core.base_component import Component
from src.core.renderer import ModernRenderer
from src.core.shader_manager import ShaderManager


class ComponentRegistry:
    """Registro global para mapeamento de tipos de componentes para suas classes"""
    
    def __init__(self):
        """Inicializa registro com dicionários vazios para cada categoria"""
        self._logic_gates: Dict[str, Type[LogicGate]] = {}
        self._buttons: Dict[str, Type[ButtonBase]] = {}
        self._leds: Dict[str, Type[Component]] = {}
        self._texts: Dict[str, Type[Component]] = {}
        self._backgrounds: Dict[str, Type[Component]] = {}
    
    def register_logic_gate(self, name: str, gate_class: Type[LogicGate]) -> None:
        """Registra classe de porta lógica com tipo específico"""
        if name.upper() in self._logic_gates:
            raise ValueError(f"Porta lógica '{name}' já está registrada")
        self._logic_gates[name.upper()] = gate_class
        print(f"Registrada porta lógica: {name} -> {gate_class.__name__}")
    
    def register_button(self, name: str, button_class: Type[ButtonBase]) -> None:
        """Registra classe de botão com tipo específico"""
        if name.upper() in self._buttons:
            raise ValueError(f"Botão '{name}' já está registrado")
        self._buttons[name.upper()] = button_class
        print(f"Registrado botão: {name} -> {button_class.__name__}")
    
    def register_led(self, name: str, led_class: Type[Component]) -> None:
        """Registra classe de LED com tipo específico"""
        if name.upper() in self._leds:
            raise ValueError(f"LED '{name}' já está registrado")
        self._leds[name.upper()] = led_class
        print(f"Registrado LED: {name} -> {led_class.__name__}")
    
    def register_text(self, name: str, text_class: Type[Component]) -> None:
        """Registra classe de texto com tipo específico"""
        if name.upper() in self._texts:
            raise ValueError(f"Texto '{name}' já está registrado")
        self._texts[name.upper()] = text_class
        print(f"Registrado texto: {name} -> {text_class.__name__}")
    
    def register_background(self, name: str, background_class: Type[Component]) -> None:
        """Registra classe de background com tipo específico"""
        if name.upper() in self._backgrounds:
            raise ValueError(f"Background '{name}' já está registrado")
        self._backgrounds[name.upper()] = background_class
        print(f"Registrado background: {name} -> {background_class.__name__}")
    
    def create_logic_gate(self, gate_type: str, **kwargs) -> Optional[LogicGate]:
        """Cria instância de porta lógica pelo tipo"""
        gate_class = self._logic_gates.get(gate_type.upper())
        if gate_class is None:
            raise ValueError(f"Porta lógica '{gate_type}' não está registrada")
        return gate_class(**kwargs)
    
    def create_button(self, button_type: str, **kwargs) -> Optional[ButtonBase]:
        """Cria instância de botão pelo tipo"""
        button_class = self._buttons.get(button_type.upper())
        if button_class is None:
            raise ValueError(f"Botão '{button_type}' não está registrado")
        return button_class(**kwargs)
    
    def create_led(self, led_type: str, **kwargs) -> Optional[Component]:
        """Cria instância de LED pelo tipo"""
        led_class = self._leds.get(led_type.upper())
        if led_class is None:
            raise ValueError(f"LED '{led_type}' não está registrado")
        return led_class(**kwargs)
    
    def create_text(self, text_type: str, **kwargs) -> Optional[Component]:
        """Cria instância de texto pelo tipo"""
        text_class = self._texts.get(text_type.upper())
        if text_class is None:
            raise ValueError(f"Texto '{text_type}' não está registrado")
        return text_class(**kwargs)
    
    def create_background(self, background_type: str, **kwargs) -> Optional[Component]:
        """Cria instância de background pelo tipo"""
        background_class = self._backgrounds.get(background_type.upper())
        if background_class is None:
            raise ValueError(f"Background '{background_type}' não está registrado")
        return background_class(**kwargs)
    
    def list_logic_gates(self) -> list[str]:
        """Lista todos os tipos de portas lógicas registradas"""
        return list(self._logic_gates.keys())
    
    def list_buttons(self) -> list[str]:
        """Lista todos os tipos de botões registrados"""
        return list(self._buttons.keys())
    
    def list_leds(self) -> list[str]:
        """Lista todos os tipos de LEDs registrados"""
        return list(self._leds.keys())
    
    def list_texts(self) -> list[str]:
        """Lista todos os tipos de textos registrados"""
        return list(self._texts.keys())
    
    def list_backgrounds(self) -> list[str]:
        """Lista todos os tipos de backgrounds registrados"""
        return list(self._backgrounds.keys())


# Instância global do registro
component_registry = ComponentRegistry()


def register_components():
    """Registra todos os componentes disponíveis no registry"""
    # Importar classes das portas lógicas
    from src.components.logic.and_gate import ANDGate
    from src.components.logic.or_gate import ORGate
    from src.components.logic.not_gate import NOTGate
    
    # Importar classes dos botões
    from src.components.logic.input_button import InputButton
    from src.components.ui.menu_button import MenuButton
    
    # Importar classes de outros componentes
    from src.components.logic.led_component import LEDComponent
    from src.components.ui.text_component import TextComponent
    from src.components.ui.background_component import BackgroundComponent
    
    # Registrar portas lógicas
    component_registry.register_logic_gate('AND', ANDGate)
    component_registry.register_logic_gate('OR', ORGate)
    component_registry.register_logic_gate('NOT', NOTGate)
    
    # Registrar botões
    component_registry.register_button('INPUT', InputButton)
    component_registry.register_button('MENU', MenuButton)
    
    # Registrar outros componentes
    component_registry.register_led('LED', LEDComponent)
    component_registry.register_text('TEXT', TextComponent)
    component_registry.register_background('BACKGROUND', BackgroundComponent)


def create_logic_gate(gate_type: str, position: Tuple[int, int], **kwargs) -> Optional[LogicGate]:
    """Função de conveniência para criar portas lógicas"""
    return component_registry.create_logic_gate(gate_type, position=position, **kwargs)


def create_button(button_type: str, position: Tuple[int, int], **kwargs) -> Optional[ButtonBase]:
    """Função de conveniência para criar botões"""
    return component_registry.create_button(button_type, position=position, **kwargs)


def create_led(led_type: str, position: Tuple[int, int], **kwargs) -> Optional[Component]:
    """Função de conveniência para criar LEDs"""
    return component_registry.create_led(led_type, position=position, **kwargs)


def create_text(text_type: str, **kwargs) -> Optional[Component]:
    """Função de conveniência para criar textos"""
    return component_registry.create_text(text_type, **kwargs)


def create_background(background_type: str, **kwargs) -> Optional[Component]:
    """Função de conveniência para criar backgrounds"""
    return component_registry.create_background(background_type, **kwargs)


def create_component_from_data(component_data: dict, shader_manager=None, callbacks=None) -> Optional[Component]:
    """Cria componente baseado em dados JSON usando sistema de fábricas"""
    component_type = component_data.get("type", "").lower()
    
    # Map JSON types to factory types
    type_mapping = {
        "and_gate": "AND",
        "or_gate": "OR", 
        "not_gate": "NOT",
        "input_button": "INPUT",
        "menu_button": "MENU",
        "led": "LED",
        "text": "TEXT",
        "background": "BACKGROUND"
    }
    
    # Convert to factory type
    factory_type = type_mapping.get(component_type, component_type.upper())
    
    # Adicionar shader_manager se fornecido
    kwargs = component_data.copy()
    if shader_manager:
        kwargs["shader_manager"] = shader_manager
    
    # Handle callbacks for menu buttons
    if component_type == "menu_button" and callbacks:
        callback_name = kwargs.get("callback")
        if callback_name and callback_name in callbacks:
            kwargs["callback"] = callbacks[callback_name]
    
    # Remover o tipo dos kwargs pois não é um parâmetro do construtor
    kwargs.pop("type", None)
    kwargs.pop("id", None)  # ID não é usado no construtor
    
    try:
        # Tentar criar baseado no tipo
        if factory_type in component_registry.list_logic_gates():
            position = kwargs.pop("position", (0, 0))
            return create_logic_gate(factory_type, position, **kwargs)
        
        elif factory_type in component_registry.list_buttons():
            position = kwargs.pop("position", (0, 0))
            return create_button(factory_type, position, **kwargs)
        
        elif factory_type in component_registry.list_leds():
            position = kwargs.pop("position", (0, 0))
            return create_led(factory_type, position, **kwargs)
        
        elif factory_type in component_registry.list_texts():
            return create_text(factory_type, **kwargs)
        
        elif factory_type in component_registry.list_backgrounds():
            return create_background(factory_type, **kwargs)
        
        else:
            print(f"Tipo de componente desconhecido: {component_type} (mapeado para: {factory_type})")
            return None
            
    except Exception as e:
        print(f"Erro ao criar componente {component_type}: {e}")
        return None


# Auto-registro de componentes quando o módulo for importado
register_components() 