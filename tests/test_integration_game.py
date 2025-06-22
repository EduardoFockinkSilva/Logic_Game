import pytest
from src.components.and_gate import ANDGate
from src.components.or_gate import ORGate
from src.components.not_gate import NOTGate
from src.components.input_button import InputButton
from src.components.led_component import LEDComponent

@pytest.mark.integration
def test_signal_propagation_and_led_update():
    # Cria botões de entrada
    btn1 = InputButton(text="A", position=(0, 0))
    btn2 = InputButton(text="B", position=(0, 0))
    
    # Cria uma porta AND e conecta os botões
    and_gate = ANDGate(position=(100, 100))
    and_gate.add_input(btn1)
    and_gate.add_input(btn2)
    
    # Cria um LED conectado à saída da AND
    led = LEDComponent(position=(200, 200), input_source=and_gate)
    
    # Estado inicial: ambos botões desligados
    btn1.state = False
    btn2.state = False
    assert not and_gate.get_result()
    assert not led.get_state()
    
    # Liga apenas um botão
    btn1.state = True
    assert not and_gate.get_result()
    assert not led.get_state()
    
    # Liga ambos
    btn2.state = True
    assert and_gate.get_result()
    assert led.get_state()
    
    # Desliga um botão
    btn1.state = False
    assert not and_gate.get_result()
    assert not led.get_state() 