"""
Porta lógica NOT
"""

from src.components.logic.logic_gate import LogicGate
from config.style import Colors


class NOTGate(LogicGate):
    """Porta lógica NOT - inverte o valor da entrada"""
    
    def __init__(self, position=(0, 0), size=None, off_color=None, on_color=None, window_size=(800, 600), shader_manager=None):
        """Inicializa porta NOT com cores padrão"""
        if off_color is None:
            off_color = Colors.NOT_GATE_OFF
        if on_color is None:
            on_color = Colors.NOT_GATE_ON
        
        super().__init__(position, size, off_color, on_color)
        self.window_size = window_size
        self.shader_manager = shader_manager
    
    def _calculate_result(self) -> bool:
        """Calcula resultado da porta NOT"""
        if not self.inputs:
            return False
        # NOT inverte o resultado da primeira entrada
        return not self.inputs[0].get_result()

    add_input_button = LogicGate.add_input 