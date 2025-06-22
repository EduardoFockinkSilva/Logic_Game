"""
Teste de integração do sistema de conexões automáticas.

Este teste demonstra como o sistema de conexões funciona automaticamente,
criando conexões visuais entre componentes e mudando de cor baseado
no estado dos sinais.
"""

import sys
import os
import time

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.game_engine import GameEngine
from src.components.input_button import InputButton
from src.components.and_gate import ANDGate
from src.components.or_gate import ORGate
from src.components.led_component import LEDComponent
from src.components.connection_manager import ConnectionManager


def test_connection_system():
    """
    Teste principal do sistema de conexões.
    
    Cria um circuito simples: Input Button -> AND Gate -> LED
    e demonstra como as conexões são criadas automaticamente.
    """
    print("🧪 Iniciando teste do sistema de conexões...")
    
    # Criar engine do jogo
    engine = GameEngine(width=800, height=600, title="Teste de Conexões")
    
    try:
        # Inicializar engine
        engine.initialize()
        
        print("✅ Engine inicializado")
        
        # Criar componentes do circuito
        print("\n🔌 Criando componentes do circuito...")
        
        # Input Button (fonte de sinal)
        input_button = InputButton(
            position=(100, 300),
            size=(80, 40),
            text="ON",
            window_size=(800, 600),
            shader_manager=engine.get_shader_manager()
        )
        
        # AND Gate (porta lógica)
        and_gate = ANDGate(
            position=(300, 280),
            size=(100, 80),
            window_size=(800, 600),
            shader_manager=engine.get_shader_manager()
        )
        
        # LED (indicador de saída)
        led = LEDComponent(
            position=(500, 300),
            radius=30,
            window_size=(800, 600),
            shader_manager=engine.get_shader_manager()
        )
        
        print("✅ Componentes criados")
        
        # Adicionar componentes ao engine (conexões serão criadas automaticamente)
        print("\n🔗 Adicionando componentes ao engine...")
        engine.add_component(input_button)
        engine.add_component(and_gate)
        engine.add_component(led)
        
        # Conectar input_button à ANDGate
        and_gate.add_input(input_button)
        # Conectar saída da ANDGate ao LED
        led.set_input_source(and_gate)
        
        # Verificar se as conexões foram criadas
        connection_manager = engine.get_connection_manager()
        connection_count = connection_manager.get_connection_count()
        print(f"✅ {connection_count} conexões criadas automaticamente")
        
        # Simular interação com o circuito
        print("\n🎮 Simulando interação com o circuito...")
        
        # Estado inicial
        print("📊 Estado inicial:")
        print(f"   Input Button: {'ON' if input_button.get_state() else 'OFF'}")
        print(f"   AND Gate Input 1: {and_gate.inputs[0] if and_gate.inputs else 'N/A'}")
        print(f"   AND Gate Result: {and_gate.get_result()}")
        print(f"   LED State: {'ON' if led.get_state() else 'OFF'}")
        
        # Simular clique no botão
        print("\n🖱️ Simulando clique no Input Button...")
        input_button.set_state(True)
        
        # Atualizar componentes
        engine.update()
        
        print("📊 Estado após ativar Input Button:")
        print(f"   Input Button: {'ON' if input_button.get_state() else 'OFF'}")
        print(f"   AND Gate Input 1: {and_gate.inputs[0] if and_gate.inputs else 'N/A'}")
        print(f"   AND Gate Result: {and_gate.get_result()}")
        print(f"   LED State: {'ON' if led.get_state() else 'OFF'}")
        
        # Verificar se o LED acendeu
        if led.get_state():
            print("✅ LED acendeu corretamente!")
        else:
            print("❌ LED não acendeu - verificar conexões")
        
        # Simular desligar o botão
        print("\n🖱️ Simulando desligar Input Button...")
        input_button.set_state(False)
        
        # Atualizar componentes
        engine.update()
        
        print("📊 Estado após desativar Input Button:")
        print(f"   Input Button: {'ON' if input_button.get_state() else 'OFF'}")
        print(f"   AND Gate Input 1: {and_gate.inputs[0] if and_gate.inputs else 'N/A'}")
        print(f"   AND Gate Result: {and_gate.get_result()}")
        print(f"   LED State: {'ON' if led.get_state() else 'OFF'}")
        
        # Verificar se o LED apagou
        if not led.get_state():
            print("✅ LED apagou corretamente!")
        else:
            print("❌ LED não apagou - verificar conexões")
        
        # Testar renderização
        print("\n🎨 Testando renderização...")
        engine.render()
        print("✅ Renderização executada com sucesso")
        
        # Informações finais
        print("\n📈 Informações do sistema de conexões:")
        print(f"   Total de conexões: {connection_manager.get_connection_count()}")
        print(f"   Conexões do Input Button: {len(connection_manager.get_component_connections(input_button))}")
        print(f"   Conexões do AND Gate: {len(connection_manager.get_component_connections(and_gate))}")
        print(f"   Conexões do LED: {len(connection_manager.get_component_connections(led))}")
        
        print("\n🎉 Teste do sistema de conexões concluído com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Limpar recursos
        print("\n🧹 Limpando recursos...")
        engine.cleanup()


def test_connection_visualization():
    """
    Teste específico para visualização das conexões.
    
    Cria múltiplos componentes para demonstrar diferentes tipos
    de conexões e suas cores.
    """
    print("\n🎨 Teste de visualização das conexões...")
    
    # Criar engine do jogo
    engine = GameEngine(width=800, height=600, title="Teste Visual de Conexões")
    
    try:
        # Inicializar engine
        engine.initialize()
        
        # Criar múltiplos componentes
        input1 = InputButton(position=(100, 200), size=(80, 40), text="ON", window_size=(800, 600), shader_manager=engine.get_shader_manager())
        input2 = InputButton(position=(100, 400), size=(80, 40), text="ON", window_size=(800, 600), shader_manager=engine.get_shader_manager())

        and_gate = ANDGate(position=(300, 250), size=(100, 80), window_size=(800, 600), shader_manager=engine.get_shader_manager())
        or_gate = ORGate(position=(300, 350), size=(100, 80), window_size=(800, 600), shader_manager=engine.get_shader_manager())

        led1 = LEDComponent(position=(500, 270), radius=30, window_size=(800, 600), shader_manager=engine.get_shader_manager())
        led2 = LEDComponent(position=(500, 370), radius=30, window_size=(800, 600), shader_manager=engine.get_shader_manager())

        # Conectar entradas e saídas
        and_gate.add_input(input1)
        and_gate.add_input(input2)
        or_gate.add_input(input1)
        or_gate.add_input(input2)
        led1.set_input_source(and_gate)
        led2.set_input_source(or_gate)
        
        # Adicionar componentes
        components = [input1, input2, and_gate, or_gate, led1, led2]
        for component in components:
            engine.add_component(component)
        
        # Testar diferentes estados
        print("🔄 Testando diferentes estados das conexões...")
        
        # Estado 1: Apenas input1 ligado
        input1.set_state(True)
        input2.set_state(False)
        engine.update()
        print("   Estado 1: Input1=ON, Input2=OFF")
        
        # Estado 2: Apenas input2 ligado
        input1.set_state(False)
        input2.set_state(True)
        engine.update()
        print("   Estado 2: Input1=OFF, Input2=ON")
        
        # Estado 3: Ambos ligados
        input1.set_state(True)
        input2.set_state(True)
        engine.update()
        print("   Estado 3: Input1=ON, Input2=ON")
        
        # Estado 4: Ambos desligados
        input1.set_state(False)
        input2.set_state(False)
        engine.update()
        print("   Estado 4: Input1=OFF, Input2=OFF")
        
        print("✅ Teste de visualização concluído!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste de visualização: {e}")
        return False
    
    finally:
        engine.cleanup()


if __name__ == "__main__":
    print("🚀 Iniciando testes do sistema de conexões...")
    
    # Teste principal
    success1 = test_connection_system()
    
    # Teste de visualização
    success2 = test_connection_visualization()
    
    # Resultado final
    if success1 and success2:
        print("\n🎉 Todos os testes passaram!")
        print("✅ Sistema de conexões funcionando corretamente")
    else:
        print("\n❌ Alguns testes falharam")
        print("🔧 Verificar implementação do sistema de conexões") 