"""
Porta lógica AND com feedback visual
"""

from src.components.logic_gate import LogicGate


class ANDGate(LogicGate):
    """Porta lógica AND - retorna True apenas quando todas as entradas são True"""
    
    def __init__(self, position, size=(120, 80), off_color=(128, 128, 128), on_color=(255, 255, 224), **kwargs):
        super().__init__(position=position, size=size, off_color=off_color, on_color=on_color)

    def _calculate_result(self) -> bool:
        if not self.inputs:
            return False
        return all(inp.get_result() if hasattr(inp, 'get_result') else False for inp in self.inputs)

    add_input_button = LogicGate.add_input 