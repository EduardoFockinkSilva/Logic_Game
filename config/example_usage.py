"""
Exemplo de uso das configurações centralizadas
Este arquivo demonstra como usar as constantes organizadas em diferentes partes do projeto
"""

from config import (
    WindowConfig, Colors, ComponentConfig, Paths, 
    PerformanceConfig, DebugConfig, get_window_size,
    get_default_colors, get_component_defaults
)


def exemplo_game_engine():
    """Exemplo de como usar configurações no GameEngine"""
    print("=== Exemplo GameEngine ===")
    
    # Usar configurações de janela
    width = WindowConfig.DEFAULT_WIDTH
    height = WindowConfig.DEFAULT_HEIGHT
    title = WindowConfig.DEFAULT_TITLE
    
    print(f"Janela: {width}x{height} - {title}")
    
    # Usar função utilitária
    window_size = get_window_size()
    print(f"Tamanho da janela: {window_size}")


def exemplo_componentes():
    """Exemplo de como usar configurações nos componentes"""
    print("\n=== Exemplo Componentes ===")
    
    # Cores para botões de entrada
    input_off_color = Colors.INPUT_OFF
    input_on_color = Colors.INPUT_ON
    print(f"Cores do botão de entrada: OFF={input_off_color}, ON={input_on_color}")
    
    # Cores para LEDs
    led_off_color = Colors.LED_OFF
    led_on_color = Colors.LED_ON
    print(f"Cores do LED: OFF={led_off_color}, ON={led_on_color}")
    
    # Tamanhos padrão
    button_size = ComponentConfig.DEFAULT_BUTTON_SIZE
    gate_size = ComponentConfig.DEFAULT_GATE_SIZE
    led_radius = ComponentConfig.DEFAULT_LED_RADIUS
    print(f"Tamanhos: Botão={button_size}, Porta={gate_size}, LED={led_radius}")
    
    # Tamanhos de fonte
    title_font = ComponentConfig.TITLE_FONT_SIZE
    debug_font = ComponentConfig.DEBUG_FONT_SIZE
    print(f"Fontes: Título={title_font}, Debug={debug_font}")


def exemplo_debug():
    """Exemplo de como usar configurações de debug"""
    print("\n=== Exemplo Debug ===")
    
    # Configurações de debug
    debug_enabled = DebugConfig.ENABLE_DEBUG_HUD
    show_fps = DebugConfig.SHOW_FPS
    show_mouse = DebugConfig.SHOW_MOUSE_POS
    
    print(f"Debug HUD: {debug_enabled}")
    print(f"Mostrar FPS: {show_fps}")
    print(f"Mostrar posição do mouse: {show_mouse}")
    
    # Configurações de performance
    fps_interval = PerformanceConfig.FPS_UPDATE_INTERVAL
    target_fps = PerformanceConfig.TARGET_FPS
    print(f"Intervalo FPS: {fps_interval}s")
    print(f"FPS alvo: {target_fps}")


def exemplo_cores():
    """Exemplo de como usar a paleta de cores"""
    print("\n=== Exemplo Cores ===")
    
    # Obter todas as cores padrão
    cores = get_default_colors()
    print("Cores disponíveis:")
    for nome, cor in cores.items():
        print(f"  {nome}: {cor}")
    
    # Cores específicas para componentes
    print(f"\nCores de componentes:")
    print(f"  AND Gate OFF: {Colors.AND_GATE_OFF}")
    print(f"  AND Gate ON: {Colors.AND_GATE_ON}")
    print(f"  OR Gate OFF: {Colors.OR_GATE_OFF}")
    print(f"  OR Gate ON: {Colors.OR_GATE_ON}")
    print(f"  NOT Gate OFF: {Colors.NOT_GATE_OFF}")
    print(f"  NOT Gate ON: {Colors.NOT_GATE_ON}")


def exemplo_paths():
    """Exemplo de como usar os caminhos dos arquivos"""
    print("\n=== Exemplo Paths ===")
    
    # Caminhos dos shaders
    print("Shaders:")
    print(f"  Button Vertex: {Paths.SHADER_BUTTON_VERTEX}")
    print(f"  Button Fragment: {Paths.SHADER_BUTTON_FRAGMENT}")
    print(f"  Text Vertex: {Paths.SHADER_TEXT_VERTEX}")
    print(f"  Text Fragment: {Paths.SHADER_TEXT_FRAGMENT}")
    
    # Caminhos dos níveis
    print("\nNíveis:")
    print(f"  Menu: {Paths.LEVEL_MENU}")
    print(f"  Level 1: {Paths.LEVEL_1}")
    print(f"  Level 2: {Paths.LEVEL_2}")
    print(f"  Level 3: {Paths.LEVEL_3}")


def exemplo_configuracoes_componentes():
    """Exemplo de como usar configurações padrão dos componentes"""
    print("\n=== Exemplo Configurações de Componentes ===")
    
    # Obter configurações padrão
    defaults = get_component_defaults()
    print("Configurações padrão:")
    for nome, valor in defaults.items():
        print(f"  {nome}: {valor}")
    
    # Posições padrão
    print(f"\nPosições padrão:")
    print(f"  Título: {ComponentConfig.TITLE_POSITION}")
    print(f"  Subtítulo: {ComponentConfig.SUBTITLE_POSITION}")
    print(f"  Instruções: {ComponentConfig.INSTRUCTION_POSITION}")
    print(f"  Botão Menu: {ComponentConfig.MENU_BUTTON_POSITION}")


def exemplo_uso_real():
    """Exemplo de como seria usado em código real"""
    print("\n=== Exemplo Uso Real ===")
    
    # Simular criação de um botão de entrada
    def criar_input_button(texto, posicao):
        from config import Colors, ComponentConfig
        
        return {
            "type": "input_button",
            "text": texto,
            "position": posicao,
            "size": ComponentConfig.DEFAULT_BUTTON_SIZE,
            "off_color": Colors.INPUT_OFF,
            "on_color": Colors.INPUT_ON,
            "text_color": Colors.TEXT_WHITE,
            "window_size": get_window_size(),
            "initial_state": False
        }
    
    # Simular criação de uma porta AND
    def criar_and_gate(posicao):
        from config import Colors, ComponentConfig
        
        return {
            "type": "and_gate",
            "position": posicao,
            "size": ComponentConfig.DEFAULT_GATE_SIZE,
            "off_color": Colors.AND_GATE_OFF,
            "on_color": Colors.AND_GATE_ON,
            "text_color": Colors.TEXT_WHITE,
            "window_size": get_window_size()
        }
    
    # Simular criação de um LED
    def criar_led(posicao):
        from config import Colors, ComponentConfig
        
        return {
            "type": "led",
            "position": posicao,
            "radius": ComponentConfig.DEFAULT_LED_RADIUS,
            "off_color": Colors.LED_OFF,
            "on_color": Colors.LED_ON,
            "window_size": get_window_size()
        }
    
    # Criar componentes usando configurações
    input1 = criar_input_button("Input 1", ComponentConfig.TEST_INPUT_1_POSITION)
    input2 = criar_input_button("Input 2", ComponentConfig.TEST_INPUT_2_POSITION)
    and_gate = criar_and_gate(ComponentConfig.TEST_GATE_POSITION)
    led = criar_led(ComponentConfig.TEST_LED_POSITION)
    
    print("Componentes criados com configurações centralizadas:")
    print(f"  Input 1: {input1['position']} - {input1['size']}")
    print(f"  Input 2: {input2['position']} - {input2['size']}")
    print(f"  AND Gate: {and_gate['position']} - {and_gate['size']}")
    print(f"  LED: {led['position']} - raio={led['radius']}")


if __name__ == "__main__":
    """Executar todos os exemplos"""
    print("EXEMPLOS DE USO DAS CONFIGURAÇÕES CENTRALIZADAS")
    print("=" * 60)
    
    exemplo_game_engine()
    exemplo_componentes()
    exemplo_debug()
    exemplo_cores()
    exemplo_paths()
    exemplo_configuracoes_componentes()
    exemplo_uso_real()
    
    print("\n" + "=" * 60)
    print("Todos os exemplos executados com sucesso!")
    print("As configurações centralizadas facilitam a manutenção e")
    print("tornam o código mais legível e organizado.") 