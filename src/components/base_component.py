"""
Componente base para todos os componentes do jogo
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class Component(ABC):
    """
    Classe base para todos os componentes do jogo.
    Implementa o padrão Component para arquitetura modular.
    """
    
    def __init__(self, entity: Optional[Any] = None):
        """
        Inicializa o componente.
        
        Args:
            entity: Entidade pai que possui este componente
        """
        self.entity = entity
        self.enabled = True
        self._initialized = False
    
    def initialize(self) -> None:
        """Inicializa o componente. Chamado uma vez após a criação."""
        if not self._initialized:
            self._initialize()
            self._initialized = True
    
    @abstractmethod
    def _initialize(self) -> None:
        """Implementação específica da inicialização."""
        pass
    
    def update(self, delta_time: float) -> None:
        """
        Atualiza o componente a cada frame.
        
        Args:
            delta_time: Tempo desde o último frame em segundos
        """
        if self.enabled and self._initialized:
            self._update(delta_time)
    
    def _update(self, delta_time: float) -> None:
        """Implementação específica da atualização."""
        pass
    
    def render(self, renderer: Any) -> None:
        """
        Renderiza o componente.
        
        Args:
            renderer: Renderizador OpenGL
        """
        if self.enabled and self._initialized:
            self._render(renderer)
    
    def _render(self, renderer: Any) -> None:
        """Implementação específica da renderização."""
        pass
    
    def destroy(self) -> None:
        """Destrói o componente e libera recursos."""
        if self._initialized:
            self._destroy()
            self._initialized = False
    
    def _destroy(self) -> None:
        """Implementação específica da destruição."""
        pass 