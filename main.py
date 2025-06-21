#!/usr/bin/env python3
"""
Jogo de Puzzle Lógico com Pygame e OpenGL
Main entry point - Arquitetura Modular
"""

from src.core.game_engine import GameEngine
from src.components.background_component import BackgroundComponent
from src.components.text_component import TextComponent
from src.components.menu_button import MenuButton


def start_game():
    """Callback para iniciar o jogo."""
    print("Iniciando o jogo...")
    # Aqui você pode adicionar lógica para iniciar as fases

def exit_game():
    """Callback para sair do jogo."""
    print("Saindo do jogo...")
    # Aqui você pode adicionar lógica para sair do jogo
    import sys
    sys.exit(0)


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

    # Adicionar componente de texto centralizado no topo
    title = TextComponent(
        text="Logic Game",
        font_size=48,
        color=(255,255,255),
        position=(0.5, 0.05),
        window_size=(800,600),
        shader_manager=engine.get_shader_manager()
    )
    engine.add_component(title)
    
    # Adicionar botão Start centralizado (em cima)
    start_button = MenuButton(
        text="Start",
        position=(300, 320),  # Em cima (Y maior = mais para cima)
        size=(200, 50),
        color=(255, 255, 255),  # Texto branco
        hover_color=(200, 200, 255),  # Texto azul claro no hover
        window_size=(800, 600),
        shader_manager=engine.get_shader_manager(),
        callback=start_game,
        bg_color=(60, 60, 120),  # Azul escuro para combinar com background
        border_color=(100, 100, 180)
    )
    engine.add_component(start_button)
    
    # Adicionar botão Exit centralizado (embaixo)
    exit_button = MenuButton(
        text="Exit",
        position=(300, 250),  # Em baixo (Y menor = mais para baixo)
        size=(200, 50),
        color=(255, 255, 255),  # Texto branco
        hover_color=(255, 200, 200),  # Texto vermelho claro no hover
        window_size=(800, 600),
        shader_manager=engine.get_shader_manager(),
        callback=exit_game,
        bg_color=(120, 60, 60),  # Vermelho escuro para combinar com background
        border_color=(180, 100, 100)
    )
    engine.add_component(exit_button)
    
    # Executar o jogo
    engine.run()


if __name__ == "__main__":
    main() 