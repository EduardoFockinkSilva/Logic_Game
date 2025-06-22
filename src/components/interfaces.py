"""
Interfaces e Protocols para o sistema de componentes.

Este módulo define as interfaces principais que os componentes devem implementar,
garantindo consistência e facilitando a extensibilidade do sistema.
"""

from typing import Protocol, Tuple, Optional, runtime_checkable

@runtime_checkable
class LogicInputSource(Protocol):
    """
    Protocol para componentes que fornecem valores lógicos (True/False).
    
    Implementado por portas lógicas e outros componentes que podem ser
    usados como fonte de entrada para LEDs e outras portas lógicas.
    
    Examples:
        >>> class ANDGate:
        ...     def get_result(self) -> bool:
        ...         return True
        >>> gate = ANDGate()
        >>> isinstance(gate, LogicInputSource)  # True
    """
    def get_result(self) -> bool:
        """
        Retorna o resultado lógico atual do componente.
        
        Returns:
            True se o componente está ativo/ligado, False caso contrário.
        """
        ...

@runtime_checkable
class RenderableState(Protocol):
    """
    Protocol para componentes que têm estado renderizável.
    
    Combina funcionalidades de estado com informações de renderização,
    permitindo que componentes forneçam dados para renderização baseados
    em seu estado atual.
    
    Examples:
        >>> class LED:
        ...     def __init__(self, on_color=(0,255,0), off_color=(64,64,64)):
        ...         self.on_color = on_color
        ...         self.off_color = off_color
        ...         self._state = False
        ...     def get_render_color(self) -> Tuple[int, int, int]:
        ...         return self.on_color if self._state else self.off_color
        ...     def get_position(self) -> Tuple[int, int]:
        ...         return (100, 100)
        ...     def get_size(self) -> Tuple[int, int]:
        ...         return (40, 40)
        >>> led = LED()
        >>> isinstance(led, RenderableState)  # True
    """
    def get_render_color(self) -> Tuple[int, int, int]:
        """
        Retorna a cor atual para renderização baseada no estado.
        
        Returns:
            Tupla (R, G, B) com a cor atual para renderização.
        """
        ...
    
    def get_position(self) -> Tuple[int, int]:
        """
        Retorna a posição do componente na tela.
        
        Returns:
            Tupla (x, y) com as coordenadas do componente.
        """
        ...
    
    def get_size(self) -> Tuple[int, int]:
        """
        Retorna o tamanho do componente.
        
        Returns:
            Tupla (largura, altura) com as dimensões do componente.
        """
        ... 