#!/usr/bin/env python3
"""
Jogo de Puzzle Lógico com Pygame e OpenGL
Main entry point - Arquitetura Modular com Sistema de Níveis
"""

from src.core.game_engine import GameEngine
from src.core.level_manager import LevelManager
from src.components.core.factories import component_registry


def main():
    """Função principal do jogo"""
    print("Iniciando o jogo de Puzzle Lógico...")
    
    # Verificar se o sistema de fábricas está inicializado
    print(f"[Factory] Componentes registrados:")
    print(f"  - Portas lógicas: {component_registry.list_logic_gates()}")
    print(f"  - Botões: {component_registry.list_buttons()}")
    print(f"  - LEDs: {component_registry.list_leds()}")
    print(f"  - Textos: {component_registry.list_texts()}")
    print(f"  - Backgrounds: {component_registry.list_backgrounds()}")
    
    # Criar motor do jogo
    engine = GameEngine(
        width=800,
        height=600,
        title="Puzzle Lógico - CG Game"
    )
    
    # Criar gerenciador de níveis
    level_manager = LevelManager(engine)
    
    # Conectar level manager ao engine
    engine.set_level_manager(level_manager)
    
    # Carregar o menu inicial
    level_manager.load_level("menu")
    
    # Executar o jogo
    engine.run()


if __name__ == "__main__":
    main() 