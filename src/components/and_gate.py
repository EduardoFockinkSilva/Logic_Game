"""
Componente para porta lógica AND com feedback visual
"""

from .logic_gate import LogicGate, and_logic


class ANDGate(LogicGate):
    """
    Porta lógica AND que retorna True apenas quando todas as entradas são True.
    """
    
    def __init__(self, position, size=(120, 80), 
                 off_color=(128, 128, 128), on_color=(255, 255, 224),
                 text_color=(255, 255, 255), window_size=(800, 600), 
                 shader_manager=None, input_buttons=None):
        super().__init__(
            gate_type="AND",
            position=position,
            size=size,
            off_color=off_color,
            on_color=on_color,
            text_color=text_color,
            window_size=window_size,
            shader_manager=shader_manager,
            input_buttons=input_buttons,
            logic_function=and_logic
        ) 