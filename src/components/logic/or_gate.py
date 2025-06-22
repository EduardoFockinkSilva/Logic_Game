"""
Porta lógica OR com feedback visual
"""

from .logic_gate import LogicGate


class ORGate(LogicGate):
    """Porta lógica OR - retorna True quando pelo menos uma entrada é True"""
    
    def __init__(self, position, size=(120, 80), off_color=(128, 128, 128), on_color=(255, 192, 203), **kwargs):
        super().__init__(position=position, size=size, off_color=off_color, on_color=on_color)

    def _calculate_result(self) -> bool:
        if not self.inputs:
            return False
        return any(inp.get_result() if hasattr(inp, 'get_result') else False for inp in self.inputs)

    add_input_button = LogicGate.add_input 