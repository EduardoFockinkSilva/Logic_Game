#!/usr/bin/env python3
"""
Jogo de Puzzle Lógico com Pygame e OpenGL
Main entry point - Arquitetura Modular com Sistema de Níveis
"""

from src.core.game_engine import GameEngine
from src.core.level_manager import LevelManager


def main():
    """Função principal do jogo"""
    print("Iniciando o jogo de Puzzle Lógico...")
    
    # Criar motor do jogo
    engine = GameEngine(
        width=800,
        height=600,
        title="Puzzle Lógico - CG Game"
    )
    
    # Criar gerenciador de níveis
    level_manager = LevelManager(engine)
    
    # Carregar o menu inicial
    level_manager.load_level("menu")
    
    # Executar o jogo
    engine.run()


if __name__ == "__main__":
    main() 