"""
Sistema de Fábricas para Criação de Componentes.

Este módulo implementa o padrão Factory para criação centralizada de componentes,
permitindo registro dinâmico de novos tipos de componentes e facilitando
a extensibilidade do sistema.

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
from src.components.interfaces import LogicInputSource
from src.components.logic_gate import LogicGate
from src.components.button_base import ButtonBase
from src.components.base_component import Component


class ComponentRegistry:
    """
    Registro global para mapeamento de tipos de componentes para suas classes.
    
    Mantém dicionários separados para diferentes categorias de componentes, permitindo
    criação dinâmica de componentes baseada em configurações. O registro
    facilita a extensibilidade do sistema, permitindo adicionar novos tipos
    de componentes sem modificar o código principal.
    
    Attributes:
        _logic_gates: Dicionário que mapeia tipos para classes de portas lógicas
        _buttons: Dicionário que mapeia tipos para classes de botões
        _leds: Dicionário que mapeia tipos para classes de LEDs
        _texts: Dicionário que mapeia tipos para classes de texto
        _backgrounds: Dicionário que mapeia tipos para classes de background
    """
    
    def __init__(self):
        """Inicializa o registro com dicionários vazios para cada categoria."""
        self._logic_gates: Dict[str, Type[LogicGate]] = {}
        self._buttons: Dict[str, Type[ButtonBase]] = {}
        self._leds: Dict[str, Type[Component]] = {}
        self._texts: Dict[str, Type[Component]] = {}
        self._backgrounds: Dict[str, Type[Component]] = {}
    
    def register_logic_gate(self, name: str, gate_class: Type[LogicGate]) -> None:
        """
        Registra uma classe de porta lógica com um tipo específico.
        
        Args:
            name: Nome único para identificar o tipo de porta (ex: 'AND', 'OR', 'NOT')
            gate_class: Classe da porta lógica a ser registrada
            
        Raises:
            ValueError: Se o tipo já estiver registrado
        """
        if name.upper() in self._logic_gates:
            raise ValueError(f"Porta lógica '{name}' já está registrada")
        self._logic_gates[name.upper()] = gate_class
        print(f"[ComponentRegistry] Registrada porta lógica: {name} -> {gate_class.__name__}")
    
    def register_button(self, name: str, button_class: Type[ButtonBase]) -> None:
        """
        Registra uma classe de botão com um tipo específico.
        
        Args:
            name: Nome único para identificar o tipo de botão (ex: 'INPUT', 'MENU')
            button_class: Classe do botão a ser registrada
            
        Raises:
            ValueError: Se o tipo já estiver registrado
        """
        if name.upper() in self._buttons:
            raise ValueError(f"Botão '{name}' já está registrado")
        self._buttons[name.upper()] = button_class
        print(f"[ComponentRegistry] Registrado botão: {name} -> {button_class.__name__}")
    
    def register_led(self, name: str, led_class: Type[Component]) -> None:
        """
        Registra uma classe de LED com um tipo específico.
        
        Args:
            name: Nome único para identificar o tipo de LED (ex: 'LED')
            led_class: Classe do LED a ser registrada
            
        Raises:
            ValueError: Se o tipo já estiver registrado
        """
        if name.upper() in self._leds:
            raise ValueError(f"LED '{name}' já está registrado")
        self._leds[name.upper()] = led_class
        print(f"[ComponentRegistry] Registrado LED: {name} -> {led_class.__name__}")
    
    def register_text(self, name: str, text_class: Type[Component]) -> None:
        """
        Registra uma classe de texto com um tipo específico.
        
        Args:
            name: Nome único para identificar o tipo de texto (ex: 'TEXT')
            text_class: Classe do texto a ser registrada
            
        Raises:
            ValueError: Se o tipo já estiver registrado
        """
        if name.upper() in self._texts:
            raise ValueError(f"Texto '{name}' já está registrado")
        self._texts[name.upper()] = text_class
        print(f"[ComponentRegistry] Registrado texto: {name} -> {text_class.__name__}")
    
    def register_background(self, name: str, background_class: Type[Component]) -> None:
        """
        Registra uma classe de background com um tipo específico.
        
        Args:
            name: Nome único para identificar o tipo de background (ex: 'BACKGROUND')
            background_class: Classe do background a ser registrada
            
        Raises:
            ValueError: Se o tipo já estiver registrado
        """
        if name.upper() in self._backgrounds:
            raise ValueError(f"Background '{name}' já está registrado")
        self._backgrounds[name.upper()] = background_class
        print(f"[ComponentRegistry] Registrado background: {name} -> {background_class.__name__}")
    
    def create_logic_gate(self, gate_type: str, **kwargs) -> Optional[LogicGate]:
        """
        Cria uma instância de porta lógica pelo tipo.
        
        Args:
            gate_type: Tipo da porta lógica registrada (ex: 'AND', 'OR', 'NOT')
            **kwargs: Argumentos para passar ao construtor da porta
            
        Returns:
            Instância da porta lógica ou None se não encontrada
            
        Raises:
            ValueError: Se a porta lógica não estiver registrada
        """
        gate_class = self._logic_gates.get(gate_type.upper())
        if gate_class is None:
            raise ValueError(f"Porta lógica '{gate_type}' não está registrada")
        return gate_class(**kwargs)
    
    def create_button(self, button_type: str, **kwargs) -> Optional[ButtonBase]:
        """
        Cria uma instância de botão pelo tipo.
        
        Args:
            button_type: Tipo do botão registrado (ex: 'INPUT', 'MENU')
            **kwargs: Argumentos para passar ao construtor do botão
            
        Returns:
            Instância do botão ou None se não encontrado
            
        Raises:
            ValueError: Se o botão não estiver registrado
        """
        button_class = self._buttons.get(button_type.upper())
        if button_class is None:
            raise ValueError(f"Botão '{button_type}' não está registrado")
        return button_class(**kwargs)
    
    def create_led(self, led_type: str, **kwargs) -> Optional[Component]:
        """
        Cria uma instância de LED pelo tipo.
        
        Args:
            led_type: Tipo do LED registrado (ex: 'LED')
            **kwargs: Argumentos para passar ao construtor do LED
            
        Returns:
            Instância do LED ou None se não encontrado
            
        Raises:
            ValueError: Se o LED não estiver registrado
        """
        led_class = self._leds.get(led_type.upper())
        if led_class is None:
            raise ValueError(f"LED '{led_type}' não está registrado")
        return led_class(**kwargs)
    
    def create_text(self, text_type: str, **kwargs) -> Optional[Component]:
        """
        Cria uma instância de texto pelo tipo.
        
        Args:
            text_type: Tipo do texto registrado (ex: 'TEXT')
            **kwargs: Argumentos para passar ao construtor do texto
            
        Returns:
            Instância do texto ou None se não encontrado
            
        Raises:
            ValueError: Se o texto não estiver registrado
        """
        text_class = self._texts.get(text_type.upper())
        if text_class is None:
            raise ValueError(f"Texto '{text_type}' não está registrado")
        return text_class(**kwargs)
    
    def create_background(self, background_type: str, **kwargs) -> Optional[Component]:
        """
        Cria uma instância de background pelo tipo.
        
        Args:
            background_type: Tipo do background registrado (ex: 'BACKGROUND')
            **kwargs: Argumentos para passar ao construtor do background
            
        Returns:
            Instância do background ou None se não encontrado
            
        Raises:
            ValueError: Se o background não estiver registrado
        """
        background_class = self._backgrounds.get(background_type.upper())
        if background_class is None:
            raise ValueError(f"Background '{background_type}' não está registrado")
        return background_class(**kwargs)
    
    def list_logic_gates(self) -> list[str]:
        """
        Lista todos os tipos de portas lógicas registradas.
        
        Returns:
            Lista com os tipos de todas as portas lógicas registradas
        """
        return list(self._logic_gates.keys())
    
    def list_buttons(self) -> list[str]:
        """
        Lista todos os tipos de botões registrados.
        
        Returns:
            Lista com os tipos de todos os botões registrados
        """
        return list(self._buttons.keys())
    
    def list_leds(self) -> list[str]:
        """
        Lista todos os tipos de LEDs registrados.
        
        Returns:
            Lista com os tipos de todos os LEDs registrados
        """
        return list(self._leds.keys())
    
    def list_texts(self) -> list[str]:
        """
        Lista todos os tipos de textos registrados.
        
        Returns:
            Lista com os tipos de todos os textos registrados
        """
        return list(self._texts.keys())
    
    def list_backgrounds(self) -> list[str]:
        """
        Lista todos os tipos de backgrounds registrados.
        
        Returns:
            Lista com os tipos de todos os backgrounds registrados
        """
        return list(self._backgrounds.keys())


# Instância global do registro
component_registry = ComponentRegistry()


def register_components():
    """
    Registra todos os componentes disponíveis no registry.
    
    Esta função deve ser chamada após importar todos os componentes para
    garantir que todos estejam disponíveis no sistema de fábricas.
    O registro é feito automaticamente quando este módulo é importado.
    """
    # Importar classes das portas lógicas
    from src.components.and_gate import ANDGate
    from src.components.or_gate import ORGate
    from src.components.not_gate import NOTGate
    
    # Importar classes dos botões
    from src.components.input_button import InputButton
    from src.components.menu_button import MenuButton
    
    # Importar classes de outros componentes
    from src.components.led_component import LEDComponent
    from src.components.text_component import TextComponent
    from src.components.background_component import BackgroundComponent
    
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
    """
    Função de conveniência para criar portas lógicas.
    
    Esta função simplifica a criação de portas lógicas, garantindo que
    a posição seja sempre passada como primeiro argumento posicional.
    
    Args:
        gate_type: Tipo da porta ('AND', 'OR', 'NOT')
        position: Posição (x, y) da porta na tela
        **kwargs: Outros argumentos para o construtor da porta
        
    Returns:
        Instância da porta lógica ou None se não encontrada
        
    Examples:
        >>> gate = create_logic_gate('AND', position=(100, 100), size=(60, 40))
        >>> gate.position  # (100, 100)
    """
    return component_registry.create_logic_gate(gate_type, position=position, **kwargs)


def create_button(button_type: str, position: Tuple[int, int], **kwargs) -> Optional[ButtonBase]:
    """
    Função de conveniência para criar botões.
    
    Esta função simplifica a criação de botões, garantindo que
    a posição seja sempre passada como primeiro argumento posicional.
    
    Args:
        button_type: Tipo do botão ('INPUT', 'MENU')
        position: Posição (x, y) do botão na tela
        **kwargs: Outros argumentos para o construtor do botão
        
    Returns:
        Instância do botão ou None se não encontrado
        
    Examples:
        >>> button = create_button('INPUT', position=(200, 150), text="Toggle")
        >>> button.position  # (200, 150)
    """
    return component_registry.create_button(button_type, position=position, **kwargs)


def create_led(led_type: str, position: Tuple[int, int], **kwargs) -> Optional[Component]:
    """
    Função de conveniência para criar LEDs.
    
    Esta função simplifica a criação de LEDs, garantindo que
    a posição seja sempre passada como primeiro argumento posicional.
    
    Args:
        led_type: Tipo do LED ('LED')
        position: Posição (x, y) do LED na tela
        **kwargs: Outros argumentos para o construtor do LED
        
    Returns:
        Instância do LED ou None se não encontrado
        
    Examples:
        >>> led = create_led('LED', position=(300, 200), radius=20)
        >>> led.position  # (300, 200)
    """
    return component_registry.create_led(led_type, position=position, **kwargs)


def create_text(text_type: str, **kwargs) -> Optional[Component]:
    """
    Função de conveniência para criar textos.
    
    Args:
        text_type: Tipo do texto ('TEXT')
        **kwargs: Argumentos para o construtor do texto
        
    Returns:
        Instância do texto ou None se não encontrado
        
    Examples:
        >>> text = create_text('TEXT', text="Hello World", position=(0.5, 0.1))
        >>> text.text  # "Hello World"
    """
    return component_registry.create_text(text_type, **kwargs)


def create_background(background_type: str, **kwargs) -> Optional[Component]:
    """
    Função de conveniência para criar backgrounds.
    
    Args:
        background_type: Tipo do background ('BACKGROUND')
        **kwargs: Argumentos para o construtor do background
        
    Returns:
        Instância do background ou None se não encontrado
        
    Examples:
        >>> bg = create_background('BACKGROUND', shader_manager=shader_manager)
    """
    return component_registry.create_background(background_type, **kwargs)


def create_component_from_data(component_data: dict, shader_manager=None, callbacks=None) -> Optional[Component]:
    """
    Cria um componente baseado em dados JSON usando o sistema de fábricas.
    
    Args:
        component_data: Dicionário com dados do componente
        shader_manager: Gerenciador de shaders (opcional)
        callbacks: Dicionário de callbacks para botões (opcional)
        
    Returns:
        Instância do componente ou None se não puder ser criado
        
    Examples:
        >>> data = {"type": "AND", "position": [100, 100], "size": [60, 40]}
        >>> gate = create_component_from_data(data, shader_manager)
    """
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
            print(f"[Factory] Tipo de componente desconhecido: {component_type} (mapeado para: {factory_type})")
            return None
            
    except Exception as e:
        print(f"[Factory] Erro ao criar componente {component_type}: {e}")
        return None


# Auto-registro de componentes quando o módulo for importado
register_components() 