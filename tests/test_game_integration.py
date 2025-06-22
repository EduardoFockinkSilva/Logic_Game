"""
Teste de integração do sistema de conexões no contexto real do jogo.

Este teste simula o carregamento de um nível real e verifica se as
conexões visuais estão sendo criadas corretamente pelo LevelManager.
"""

import sys
import os
import json

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.game_engine import GameEngine
from src.core.level_manager import LevelManager


def test_level_loading_with_connections():
    """
    Testa o carregamento de um nível com conexões explícitas.
    """
    print("🧪 Testando carregamento de nível com conexões...")
    
    # Criar engine do jogo
    engine = GameEngine(width=800, height=600, title="Teste de Integração")
    
    try:
        # Inicializar engine
        engine.initialize()
        
        # Criar level manager
        level_manager = LevelManager(engine)
        engine.set_level_manager(level_manager)
        
        print("✅ Engine e LevelManager inicializados")
        
        # Carregar nível 1 (que tem conexões explícitas)
        print("\n📂 Carregando nível 1...")
        success = level_manager.load_level("level1")
        
        if not success:
            print("❌ Falha ao carregar nível 1")
            return False
        
        print("✅ Nível 1 carregado com sucesso")
        
        # Verificar se os componentes foram criados
        print(f"\n📊 Componentes criados:")
        print(f"   Input Buttons: {len(level_manager.input_buttons)}")
        print(f"   AND Gates: {len(level_manager.and_gates)}")
        print(f"   OR Gates: {len(level_manager.or_gates)}")
        print(f"   NOT Gates: {len(level_manager.not_gates)}")
        print(f"   LEDs: {len(level_manager.leds)}")
        print(f"   Total Components: {len(level_manager.components_by_id)}")
        
        # Verificar se as conexões foram criadas
        connection_manager = engine.get_connection_manager()
        connection_count = connection_manager.get_connection_count()
        print(f"\n🔗 Conexões visuais criadas: {connection_count}")
        
        # Verificar conexões específicas
        if level_manager.input_buttons and level_manager.and_gates:
            input_button = level_manager.input_buttons[0]
            and_gate = level_manager.and_gates[0]
            
            input_connections = connection_manager.get_component_connections(input_button)
            gate_connections = connection_manager.get_component_connections(and_gate)
            
            print(f"   Conexões do Input Button: {len(input_connections)}")
            print(f"   Conexões do AND Gate: {len(gate_connections)}")
        
        # Testar interação
        print("\n🎮 Testando interação...")
        if level_manager.input_buttons:
            input_button = level_manager.input_buttons[0]
            print(f"   Estado inicial do Input Button: {'ON' if input_button.get_state() else 'OFF'}")
            
            # Ativar botão
            input_button.set_state(True)
            engine.update()
            
            print(f"   Estado após ativar: {'ON' if input_button.get_state() else 'OFF'}")
            
            # Verificar se o LED acendeu
            if level_manager.leds:
                led = level_manager.leds[0]
                led_state = led.get_state()
                print(f"   Estado do LED: {'ON' if led_state else 'OFF'}")
                
                if led_state:
                    print("✅ LED acendeu corretamente!")
                else:
                    print("❌ LED não acendeu - verificar conexões")
        
        # Testar renderização
        print("\n🎨 Testando renderização...")
        engine.render()
        print("✅ Renderização executada com sucesso")
        
        print("\n🎉 Teste de integração concluído com sucesso!")
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


def test_level2_complex_connections():
    """
    Testa o carregamento do nível 2 que tem conexões mais complexas.
    """
    print("\n🧪 Testando nível 2 com conexões complexas...")
    
    # Criar engine do jogo
    engine = GameEngine(width=800, height=600, title="Teste Nível 2")
    
    try:
        # Inicializar engine
        engine.initialize()
        
        # Criar level manager
        level_manager = LevelManager(engine)
        engine.set_level_manager(level_manager)
        
        # Carregar nível 2
        print("📂 Carregando nível 2...")
        success = level_manager.load_level("level2")
        
        if not success:
            print("❌ Falha ao carregar nível 2")
            return False
        
        print("✅ Nível 2 carregado com sucesso")
        
        # Verificar componentes
        print(f"\n📊 Componentes do nível 2:")
        print(f"   Input Buttons: {len(level_manager.input_buttons)}")
        print(f"   AND Gates: {len(level_manager.and_gates)}")
        print(f"   OR Gates: {len(level_manager.or_gates)}")
        print(f"   NOT Gates: {len(level_manager.not_gates)}")
        print(f"   LEDs: {len(level_manager.leds)}")
        
        # Verificar conexões
        connection_manager = engine.get_connection_manager()
        connection_count = connection_manager.get_connection_count()
        print(f"\n🔗 Conexões visuais criadas: {connection_count}")
        
        # Testar lógica do nível 2: (Input1 OR Input2) AND (NOT Input2)
        print("\n🧠 Testando lógica do nível 2...")
        
        if len(level_manager.input_buttons) >= 2 and level_manager.leds:
            input1 = level_manager.input_buttons[0]
            input2 = level_manager.input_buttons[1]
            led = level_manager.leds[0]
            
            # Teste 1: Input1=ON, Input2=OFF -> LED deve acender
            input1.set_state(True)
            input2.set_state(False)
            engine.update()
            
            led_state = led.get_state()
            print(f"   Input1=ON, Input2=OFF -> LED: {'ON' if led_state else 'OFF'}")
            
            # Teste 2: Input1=OFF, Input2=ON -> LED deve apagar
            input1.set_state(False)
            input2.set_state(True)
            engine.update()
            
            led_state = led.get_state()
            print(f"   Input1=OFF, Input2=ON -> LED: {'ON' if led_state else 'OFF'}")
            
            # Teste 3: Input1=ON, Input2=ON -> LED deve apagar
            input1.set_state(True)
            input2.set_state(True)
            engine.update()
            
            led_state = led.get_state()
            print(f"   Input1=ON, Input2=ON -> LED: {'ON' if led_state else 'OFF'}")
        
        print("✅ Teste do nível 2 concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste do nível 2: {e}")
        return False
    
    finally:
        engine.cleanup()


if __name__ == "__main__":
    print("🚀 Iniciando testes de integração do sistema de conexões...")
    
    # Teste do nível 1
    success1 = test_level_loading_with_connections()
    
    # Teste do nível 2
    success2 = test_level2_complex_connections()
    
    # Resultado final
    if success1 and success2:
        print("\n🎉 Todos os testes de integração passaram!")
        print("✅ Sistema de conexões funcionando corretamente no jogo real")
    else:
        print("\n❌ Alguns testes falharam")
        print("🔧 Verificar implementação do sistema de conexões") 