"""
Componente para porta lógica NOT com feedback visual
"""

from src.components.logic_gate import LogicGate


class NOTGate(LogicGate):
    """
    Porta lógica NOT que inverte o valor da entrada.
    """
    
    def __init__(self, position, size=(120, 80), off_color=(128, 128, 128), on_color=(173, 216, 230), **kwargs):
        super().__init__(position=position, size=size, off_color=off_color, on_color=on_color)

    def _calculate_result(self) -> bool:
        if not self.inputs:
            return True
        inp = self.inputs[0]
        return not (inp.get_result() if hasattr(inp, 'get_result') else False)

    add_input_button = LogicGate.add_input 