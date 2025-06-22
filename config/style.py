"""
Configurações de estilo visual: cores, tamanhos, posições e fontes
"""
# CORES
class Colors:
    """Paleta de cores do jogo"""
    # Cores básicas
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)

    # Cores de estado dos componentes
    COMPONENT_OFF = (128, 128, 128)
    COMPONENT_ON = (255, 255, 255)

    # Cores específicas para botões de entrada
    INPUT_OFF = (255, 0, 0)      # Vermelho quando desligado
    INPUT_ON = (0, 255, 0)       # Verde quando ligado

    # Cores específicas para LEDs
    LED_OFF = (40, 40, 40)       # Cinza escuro
    LED_ON = (0, 255, 100)       # Verde brilhante

    # Cores específicas para portas lógicas
    AND_GATE_OFF = (100, 100, 120)
    AND_GATE_ON = (255, 255, 180)
    OR_GATE_OFF = (128, 128, 128)
    OR_GATE_ON = (255, 192, 203)
    NOT_GATE_OFF = (128, 128, 128)
    NOT_GATE_ON = (173, 216, 230)

    # Cores para texto
    TEXT_WHITE = (255, 255, 255)
    TEXT_GRAY = (180, 180, 200)
    TEXT_DEBUG = (255, 255, 0)   # Amarelo para debug

    # Cores para botões do menu
    MENU_BUTTON_BG = (60, 60, 120)
    MENU_BUTTON_BORDER = (100, 100, 180)
    MENU_BUTTON_HOVER = (200, 200, 255)

    EXIT_BUTTON_BG = (120, 60, 60)
    EXIT_BUTTON_BORDER = (180, 100, 100)
    EXIT_BUTTON_HOVER = (255, 200, 200)

    BACK_BUTTON_BG = (70, 70, 100)
    BACK_BUTTON_BORDER = (120, 120, 160)
    BACK_BUTTON_HOVER = (220, 220, 255)

    # Cores para conexões
    CONNECTION_OFF = (64, 64, 64)
    CONNECTION_ON = (0, 255, 0)

# TAMANHOS, POSIÇÕES E FONTES
class ComponentStyle:
    """Configurações padrão de tamanho, posição e fonte dos componentes"""
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
    BUTTON_FONT_SIZE = 24
    GATE_FONT_SIZE = 18
    MENU_BUTTON_FONT_SIZE = 28

    # Configurações de fonte
    DEFAULT_FONT_FAMILY = 'Segoe UI'  # Fonte moderna do Windows
    MENU_FONT_FAMILY = 'Segoe UI'     # Fonte moderna para botões de menu
    FONT_BOLD = True
    FONT_ITALIC = False
    
    # Lista de fontes preferidas (em ordem de preferência)
    PREFERRED_FONTS = [
        'Segoe UI',      # Moderna e legível
        'Calibri',       # Excelente para interface
        'Verdana',       # Muito legível
        'Tahoma',        # Boa para interface
        'Trebuchet MS',  # Moderna e elegante
        'Arial',         # Fallback padrão
        'Helvetica'      # Fallback universal
    ]

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