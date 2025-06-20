#!/usr/bin/env python3
"""
Jogo de Puzzle Lógico com Pygame e OpenGL
Main entry point - Arquitetura Modular
"""

from src.core.game_engine import GameEngine
from src.components.background_component import BackgroundComponent


def main():
    """Função principal do jogo"""
    print("Iniciando o jogo de Puzzle Lógico...")
    
    # Criar motor do jogo
    engine = GameEngine(
        width=800,
        height=600,
        title="Puzzle Lógico - CG Game"
    )
    
    # Adicionar componente de background animado
    background = BackgroundComponent(shader_manager=engine.get_shader_manager())
    engine.add_component(background)
    
    # Executar o jogo
    engine.run()


if __name__ == "__main__":
    main() 