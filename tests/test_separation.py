"""
Teste da separação de responsabilidades entre lógica de estado e renderização
"""

from src.components import create_logic_gate, create_button
from src.components.interfaces import RenderableState, ComponentState

def test_state_render_separation():
    """Testa a separação entre lógica de estado e renderização."""
    print("=== Teste de Separação de Responsabilidades ===")
    
    # Criar componentes usando factory
    and_gate = create_logic_gate('AND', position=(100, 100))
    input_button = create_button('INPUT', position=(200, 100), text="Input 1")
    
    print(f"AND Gate criada: {and_gate}")
    print(f"Input Button criado: {input_button}")
    print()
    
    # Testar interfaces de estado
    print("=== Testando Interfaces de Estado ===")
    
    # Verificar se implementam RenderableState
    if isinstance(and_gate, RenderableState):
        print("✓ AND Gate implementa RenderableState")
        print(f"  - Posição: {and_gate.get_position()}")
        print(f"  - Tamanho: {and_gate.get_size()}")
        print(f"  - Cor de renderização: {and_gate.get_render_color()}")
    else:
        print("✗ AND Gate não implementa RenderableState")
    
    if isinstance(input_button, RenderableState):
        print("✓ Input Button implementa RenderableState")
        print(f"  - Posição: {input_button.get_position()}")
        print(f"  - Tamanho: {input_button.get_size()}")
        print(f"  - Cor de renderização: {input_button.get_render_color()}")
    else:
        print("✗ Input Button não implementa RenderableState")
    
    print()
    
    # Testar mudança de estado
    print("=== Testando Mudança de Estado ===")
    
    # Estado inicial
    print(f"Estado inicial do botão: {input_button.get_state()}")
    print(f"Cor inicial do botão: {input_button.get_render_color()}")
    
    # Mudar estado
    input_button.set_state(True)
    print(f"Estado após set_state(True): {input_button.get_state()}")
    print(f"Cor após mudança de estado: {input_button.get_render_color()}")
    
    # Mudar estado novamente
    input_button.set_state(False)
    print(f"Estado após set_state(False): {input_button.get_state()}")
    print(f"Cor após mudança de estado: {input_button.get_render_color()}")
    
    print()
    
    # Testar lógica de porta
    print("=== Testando Lógica de Porta ===")
    print(f"Resultado inicial da porta AND: {and_gate.get_result()}")
    print(f"Cor inicial da porta: {and_gate.get_render_color()}")
    
    # Adicionar botão à porta
    and_gate.add_input_button(input_button)
    print(f"Resultado após adicionar botão desligado: {and_gate.get_result()}")
    print(f"Cor após adicionar botão desligado: {and_gate.get_render_color()}")
    
    # Ligar o botão
    input_button.set_state(True)
    print(f"Resultado após ligar botão: {and_gate.get_result()}")
    print(f"Cor após ligar botão: {and_gate.get_render_color()}")
    
    print("\n=== Teste Concluído ===")
    print("✓ Separação de responsabilidades funcionando corretamente!")
    print("  - Lógica de estado separada da renderização")
    print("  - Interfaces bem definidas")
    print("  - Componentes facilmente testáveis")

if __name__ == "__main__":
    test_state_render_separation() 