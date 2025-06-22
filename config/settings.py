"""
Configurações centralizadas do jogo de Puzzle Lógico
Todas as constantes principais do projeto estão organizadas aqui para facilitar
manutenção e legibilidade do código.
"""

from typing import Tuple, Dict, Any
import os
from config.style import Colors, ComponentStyle

# CONFIGURAÇÕES DA JANELA E DISPLAY
class WindowConfig:
    """Configurações da janela do jogo"""
    
    # Dimensões padrão da janela
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    
    # Título padrão do jogo
    DEFAULT_TITLE = "Puzzle Lógico - CG Game"
    
    # Configurações OpenGL
    OPENGL_FLAGS = "DOUBLEBUF | OPENGL"
    
    # Cor de fundo padrão (preto)
    BACKGROUND_COLOR = (0.0, 0.0, 0.0, 1.0)


# CONFIGURAÇÕES DE COMPONENTES
class ComponentConfig:
    """Configurações padrão dos componentes"""
    
    # Tamanhos padrão
    DEFAULT_BUTTON_SIZE = (80, 80)
    DEFAULT_GATE_SIZE = (120, 80)
    DEFAULT_LED_RADIUS = 30
    DEFAULT_MENU_BUTTON_SIZE = (100, 45)
    DEFAULT_LARGE_BUTTON_SIZE = (300, 75)
    
    # Tamanhos de fonte
    TITLE_FONT_SIZE = 60
    SUBTITLE_FONT_SIZE = 42
    NORMAL_FONT_SIZE = 36
    SMALL_FONT_SIZE = 18
    DEBUG_FONT_SIZE = 16
    BUTTON_FONT_SIZE = 14
    GATE_FONT_SIZE = 18
    
    # Posições padrão (relativas à janela)
    TITLE_POSITION = (0.5, 0.15)
    SUBTITLE_POSITION = (0.5, 0.08)
    INSTRUCTION_POSITION = (0.5, 0.22)
    MENU_BUTTON_POSITION = (20, 530)
    
    # Posições dos botões do menu principal
    START_BUTTON_POSITION = (250, 250)
    EXIT_BUTTON_POSITION = (250, 340)
    
    # Posições padrão para componentes de teste
    TEST_INPUT_1_POSITION = (180, 220)
    TEST_INPUT_2_POSITION = (180, 320)
    TEST_INPUT_3_POSITION = (180, 420)
    TEST_GATE_POSITION = (330, 260)
    TEST_LED_POSITION = (550, 270)

# CONFIGURAÇÕES DE ARQUIVOS E PATHS
class Paths:
    """Caminhos dos arquivos do projeto"""
    
    # Diretórios principais
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SRC_DIR = os.path.join(BASE_DIR, "src")
    LEVELS_DIR = os.path.join(BASE_DIR, "levels")
    SHADERS_DIR = os.path.join(SRC_DIR, "shaders")
    TESTS_DIR = os.path.join(BASE_DIR, "tests")
    
    # Arquivos de shader
    SHADER_BUTTON_VERTEX = os.path.join(SHADERS_DIR, "button_vertex.glsl")
    SHADER_BUTTON_FRAGMENT = os.path.join(SHADERS_DIR, "button_fragment.glsl")
    SHADER_GATE_VERTEX = os.path.join(SHADERS_DIR, "gate_vertex.glsl")
    SHADER_GATE_FRAGMENT = os.path.join(SHADERS_DIR, "gate_fragment.glsl")
    SHADER_LED_VERTEX = os.path.join(SHADERS_DIR, "led_fragment.glsl")
    SHADER_LED_FRAGMENT = os.path.join(SHADERS_DIR, "led_fragment.glsl")
    SHADER_TEXT_VERTEX = os.path.join(SHADERS_DIR, "text_vertex.glsl")
    SHADER_TEXT_FRAGMENT = os.path.join(SHADERS_DIR, "text_fragment.glsl")
    SHADER_BACKGROUND_VERTEX = os.path.join(SHADERS_DIR, "background_vertex.glsl")
    SHADER_BACKGROUND_FRAGMENT = os.path.join(SHADERS_DIR, "background_fragment.glsl")
    
    # Arquivos de nível
    LEVEL_MENU = os.path.join(LEVELS_DIR, "menu.json")
    LEVEL_1 = os.path.join(LEVELS_DIR, "level1.json")
    LEVEL_2 = os.path.join(LEVELS_DIR, "level2.json")
    LEVEL_3 = os.path.join(LEVELS_DIR, "level3.json")

# CONFIGURAÇÕES DE PERFORMANCE
class PerformanceConfig:
    """Configurações de performance e timing"""
    
    # Taxa de atualização do FPS
    FPS_UPDATE_INTERVAL = 0.1  # Atualizar FPS a cada 100ms
    
    # Taxa de atualização do debug HUD
    DEBUG_UPDATE_INTERVAL = 0.1
    
    # Limite de FPS (0 = sem limite)
    TARGET_FPS = 60
    
    # Configurações de renderização
    ENABLE_VSYNC = True
    ENABLE_ANTIALIASING = False

# CONFIGURAÇÕES DE DEBUG
class DebugConfig:
    """Configurações de debug e desenvolvimento"""
    
    # Habilitar HUD de debug
    ENABLE_DEBUG_HUD = True
    
    # Mostrar informações de debug
    SHOW_FPS = True
    SHOW_MOUSE_POS = True
    SHOW_COMPONENT_INFO = True
    
    # Configurações de log
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_TO_FILE = False
    LOG_FILE = "game.log"

# CONFIGURAÇÕES DE GAMEPLAY
class GameplayConfig:
    """Configurações de gameplay"""
    
    # Estados iniciais dos componentes
    DEFAULT_INPUT_STATE = False
    
    # Configurações de interação
    ENABLE_MOUSE_HOVER = True
    ENABLE_CLICK_FEEDBACK = True
    
    # Configurações de níveis
    START_LEVEL = "menu"
    MAX_LEVELS = 3

# CONFIGURAÇÕES DE SHADER
class ShaderConfig:
    """Configurações dos shaders"""
    
    # Nomes dos programas de shader
    SHADER_BUTTON = "button"
    SHADER_CIRCLE = "circle"
    SHADER_GATE = "gate"
    SHADER_LED = "led"
    SHADER_TEXT = "text"
    SHADER_BACKGROUND = "background"
    
    # Configurações de textura
    TEXTURE_FILTER = "LINEAR"
    TEXTURE_WRAP = "CLAMP"

# CONFIGURAÇÕES DE TESTE
class TestConfig:
    """Configurações para testes"""
    
    # Dimensões da janela de teste
    TEST_WINDOW_WIDTH = 800
    TEST_WINDOW_HEIGHT = 600
    
    # Título da janela de teste
    TEST_WINDOW_TITLE = "Teste de Componente"
    
    # Configurações de teste de integração
    INTEGRATION_TEST_TITLE = "Teste de Integração"
    LEVEL_TEST_TITLE = "Teste de Nível"
    CONNECTION_TEST_TITLE = "Teste de Conexões"

# CONFIGURAÇÕES DE AUDIO (FUTURO)
class AudioConfig:
    """Configurações de áudio (para implementação futura)"""
    
    # Configurações de som
    ENABLE_SOUND = False
    ENABLE_MUSIC = False
    
    # Volumes
    MASTER_VOLUME = 1.0
    SFX_VOLUME = 0.8
    MUSIC_VOLUME = 0.6
    
    # Frequência de amostragem
    SAMPLE_RATE = 44100
    CHANNELS = 2

# FUNÇÕES UTILITÁRIAS
def get_window_size() -> Tuple[int, int]:
    """Retorna o tamanho padrão da janela"""
    return (WindowConfig.DEFAULT_WIDTH, WindowConfig.DEFAULT_HEIGHT)

def get_default_colors() -> Dict[str, Tuple[int, int, int]]:
    """Retorna dicionário com as cores padrão"""
    return {
        'white': Colors.WHITE,
        'black': Colors.BLACK,
        'red': Colors.RED,
        'green': Colors.GREEN,
        'blue': Colors.BLUE,
        'yellow': Colors.YELLOW,
        'gray': Colors.GRAY,
        'dark_gray': Colors.DARK_GRAY,
        'light_gray': Colors.LIGHT_GRAY
    }

def get_component_defaults() -> Dict[str, Any]:
    """Retorna configurações padrão dos componentes"""
    return {
        'button_size': ComponentStyle.DEFAULT_BUTTON_SIZE,
        'gate_size': ComponentStyle.DEFAULT_GATE_SIZE,
        'led_radius': ComponentStyle.DEFAULT_LED_RADIUS,
        'title_font_size': ComponentStyle.TITLE_FONT_SIZE,
        'normal_font_size': ComponentStyle.NORMAL_FONT_SIZE,
        'debug_font_size': ComponentStyle.DEBUG_FONT_SIZE
    }

def get_shader_paths() -> Dict[str, str]:
    """Retorna caminhos dos shaders"""
    return {
        'button_vertex': Paths.SHADER_BUTTON_VERTEX,
        'button_fragment': Paths.SHADER_BUTTON_FRAGMENT,
        'gate_vertex': Paths.SHADER_GATE_VERTEX,
        'gate_fragment': Paths.SHADER_GATE_FRAGMENT,
        'text_vertex': Paths.SHADER_TEXT_VERTEX,
        'text_fragment': Paths.SHADER_TEXT_FRAGMENT,
        'background_vertex': Paths.SHADER_BACKGROUND_VERTEX,
        'background_fragment': Paths.SHADER_BACKGROUND_FRAGMENT
    }

def get_level_paths() -> Dict[str, str]:
    """Retorna caminhos dos arquivos de nível"""
    return {
        'menu': Paths.LEVEL_MENU,
        'level1': Paths.LEVEL_1,
        'level2': Paths.LEVEL_2,
        'level3': Paths.LEVEL_3
    } 