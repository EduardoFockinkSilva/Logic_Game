"""
Teste do sistema de factories para componentes
"""

from src.components import component_registry, create_logic_gate, create_button

def test_factory():
    """Testa o sistema de factories."""
    print("=== Teste do Sistema de Factories ===")
    
    # Listar componentes registrados
    print(f"Portas lógicas registradas: {component_registry.list_logic_gates()}")
    print(f"Botões registrados: {component_registry.list_buttons()}")
    print()
    
    # Criar portas lógicas usando factory
    print("Criando portas lógicas...")
    and_gate = create_logic_gate('AND', position=(100, 100))
    or_gate = create_logic_gate('OR', position=(200, 100))
    not_gate = create_logic_gate('NOT', position=(300, 100))
    
    print(f"AND Gate criada: {and_gate}")
    print(f"OR Gate criada: {or_gate}")
    print(f"NOT Gate criada: {not_gate}")
    print()
    
    # Criar botões usando factory
    print("Criando botões...")
    input_button = create_button('INPUT', position=(100, 200), text="Input 1")
    menu_button = create_button('MENU', position=(200, 200), text="Menu")
    
    print(f"Input Button criado: {input_button}")
    print(f"Menu Button criado: {menu_button}")
    print()
    
    # Testar criação com parâmetros customizados
    print("Criando porta com parâmetros customizados...")
    custom_gate = create_logic_gate(
        'AND', 
        position=(400, 100),
        size=(150, 100),
        off_color=(100, 100, 100),
        on_color=(255, 255, 0)
    )
    print(f"Porta customizada criada: {custom_gate}")
    print()
    
    # Testar porta inexistente
    print("Testando porta inexistente...")
    invalid_gate = create_logic_gate('XOR', position=(500, 100))
    print(f"Porta inexistente: {invalid_gate}")
    
    print("\n=== Teste Concluído ===")

if __name__ == "__main__":
    test_factory() 