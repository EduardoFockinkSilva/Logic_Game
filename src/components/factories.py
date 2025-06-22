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


class ComponentRegistry:
    """
    Registro global para mapeamento de tipos de componentes para suas classes.
    
    Mantém dicionários separados para portas lógicas e botões, permitindo
    criação dinâmica de componentes baseada em configurações. O registro
    facilita a extensibilidade do sistema, permitindo adicionar novos tipos
    de componentes sem modificar o código principal.
    
    Attributes:
        _logic_gates: Dicionário que mapeia tipos para classes de portas lógicas
        _buttons: Dicionário que mapeia tipos para classes de botões
    """
    
    def __init__(self):
        """Inicializa o registro com dicionários vazios para cada categoria."""
        self._logic_gates: Dict[str, Type[LogicGate]] = {}
        self._buttons: Dict[str, Type[ButtonBase]] = {}
    
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
    
    # Registrar portas lógicas
    component_registry.register_logic_gate('AND', ANDGate)
    component_registry.register_logic_gate('OR', ORGate)
    component_registry.register_logic_gate('NOT', NOTGate)
    
    # Registrar botões
    component_registry.register_button('INPUT', InputButton)
    component_registry.register_button('MENU', MenuButton)


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


# Auto-registro de componentes quando o módulo for importado
# register_components()  # Comentado para evitar registro duplo 