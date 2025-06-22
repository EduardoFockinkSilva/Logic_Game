"""
Porta lógica OR
"""

from src.components.logic.logic_gate import LogicGate
from config.style import Colors


class ORGate(LogicGate):
    """Porta lógica OR - retorna True se pelo menos uma entrada for True"""
    
    def __init__(self, position=(0, 0), size=None, off_color=None, on_color=None, window_size=(800, 600), shader_manager=None):
        """Inicializa porta OR com cores padrão"""
        if off_color is None:
            off_color = Colors.OR_GATE_OFF
        if on_color is None:
            on_color = Colors.OR_GATE_ON
        
        super().__init__(position, size, off_color, on_color)
        self.window_size = window_size
        self.shader_manager = shader_manager
    
    def _calculate_result(self) -> bool:
        """Calcula resultado da porta OR"""
        if not self.inputs:
            return False
        return any(input_source.get_result() for input_source in self.inputs)

    add_input_button = LogicGate.add_input 