# Módulo de Configurações

Este módulo centraliza todas as constantes e configurações principais do projeto de jogo de Puzzle Lógico, organizando-as de forma lógica e facilitando a manutenção e legibilidade do código.

## Estrutura

```
config/
├── __init__.py          # Módulo Python com exports
├── settings.py          # Configurações principais
├── example_usage.py     # Exemplos de uso
└── README.md           # Esta documentação
```

## Classes de Configuração

### WindowConfig
Configurações da janela do jogo:
- `DEFAULT_WIDTH = 800` - Largura padrão
- `DEFAULT_HEIGHT = 600` - Altura padrão
- `DEFAULT_TITLE = "Puzzle Lógico - CG Game"` - Título padrão
- `BACKGROUND_COLOR = (0.0, 0.0, 0.0, 1.0)` - Cor de fundo (preto)

### Colors
Paleta completa de cores do jogo:
- **Cores básicas**: `WHITE`, `BLACK`, `RED`, `GREEN`, `BLUE`, etc.
- **Cores de componentes**: `INPUT_OFF`, `INPUT_ON`, `LED_OFF`, `LED_ON`
- **Cores de portas lógicas**: `AND_GATE_OFF`, `AND_GATE_ON`, `OR_GATE_OFF`, etc.
- **Cores de texto**: `TEXT_WHITE`, `TEXT_GRAY`, `TEXT_DEBUG`
- **Cores de botões**: `MENU_BUTTON_BG`, `EXIT_BUTTON_BG`, etc.

### ComponentConfig
Configurações padrão dos componentes:
- **Tamanhos**: `DEFAULT_BUTTON_SIZE`, `DEFAULT_GATE_SIZE`, `DEFAULT_LED_RADIUS`
- **Fontes**: `TITLE_FONT_SIZE`, `NORMAL_FONT_SIZE`, `DEBUG_FONT_SIZE`
- **Posições**: `TITLE_POSITION`, `MENU_BUTTON_POSITION`, etc.

### Paths
Caminhos dos arquivos do projeto:
- **Diretórios**: `BASE_DIR`, `SRC_DIR`, `LEVELS_DIR`, `SHADERS_DIR`
- **Shaders**: `SHADER_BUTTON_VERTEX`, `SHADER_TEXT_FRAGMENT`, etc.
- **Níveis**: `LEVEL_MENU`, `LEVEL_1`, `LEVEL_2`, `LEVEL_3`

### PerformanceConfig
Configurações de performance:
- `FPS_UPDATE_INTERVAL = 0.1` - Intervalo de atualização do FPS
- `TARGET_FPS = 60` - FPS alvo
- `ENABLE_VSYNC = True` - Habilitar VSync

### DebugConfig
Configurações de debug:
- `ENABLE_DEBUG_HUD = True` - Habilitar HUD de debug
- `SHOW_FPS = True` - Mostrar FPS
- `SHOW_MOUSE_POS = True` - Mostrar posição do mouse

### GameplayConfig
Configurações de gameplay:
- `DEFAULT_INPUT_STATE = False` - Estado inicial dos inputs
- `START_LEVEL = "menu"` - Nível inicial
- `MAX_LEVELS = 3` - Número máximo de níveis

### ShaderConfig
Configurações dos shaders:
- **Nomes**: `SHADER_BUTTON`, `SHADER_GATE`, `SHADER_TEXT`, etc.
- **Configurações**: `TEXTURE_FILTER`, `TEXTURE_WRAP`

### TestConfig
Configurações para testes:
- `TEST_WINDOW_WIDTH = 800`
- `TEST_WINDOW_HEIGHT = 600`
- `TEST_WINDOW_TITLE = "Teste de Componente"`

### AudioConfig
Configurações de áudio (para implementação futura):
- `ENABLE_SOUND = False`
- `MASTER_VOLUME = 1.0`
- `SAMPLE_RATE = 44100`

## Funções Utilitárias

### get_window_size()
Retorna o tamanho padrão da janela como tupla `(width, height)`.

### get_default_colors()
Retorna dicionário com todas as cores básicas disponíveis.

### get_component_defaults()
Retorna dicionário com configurações padrão dos componentes.

### get_shader_paths()
Retorna dicionário com caminhos de todos os shaders.

### get_level_paths()
Retorna dicionário com caminhos de todos os níveis.

## Como Usar

### Importação Básica
```python
from config import WindowConfig, Colors, ComponentConfig
```

### Exemplo de Uso no GameEngine
```python
from config import WindowConfig

engine = GameEngine(
    width=WindowConfig.DEFAULT_WIDTH,
    height=WindowConfig.DEFAULT_HEIGHT,
    title=WindowConfig.DEFAULT_TITLE
)
```

### Exemplo de Uso em Componentes
```python
from config import Colors, ComponentConfig

button = InputButton(
    position=(100, 100),
    size=ComponentConfig.DEFAULT_BUTTON_SIZE,
    off_color=Colors.INPUT_OFF,
    on_color=Colors.INPUT_ON,
    text_color=Colors.TEXT_WHITE
)
```

### Exemplo de Uso com Funções Utilitárias
```python
from config import get_window_size, get_default_colors

window_size = get_window_size()
colors = get_default_colors()
```

## Benefícios

1. **Centralização**: Todas as constantes em um local
2. **Organização**: Agrupadas por categoria lógica
3. **Manutenibilidade**: Fácil alteração de valores
4. **Legibilidade**: Nomes descritivos e documentados
5. **Consistência**: Valores padronizados em todo o projeto
6. **Reutilização**: Funções utilitárias para casos comuns

## Executar Exemplos

Para ver exemplos práticos de uso, execute:
```bash
python config/example_usage.py
```

## Manutenção

Ao adicionar novas constantes:
1. Identifique a categoria apropriada
2. Adicione a constante na classe correspondente
3. Documente o propósito da constante
4. Atualize o `__init__.py` se necessário
5. Teste o uso em diferentes partes do código

## Boas Práticas

1. **Sempre use as configurações centralizadas** em vez de valores hardcoded
2. **Importe apenas o que precisa** para evitar poluição do namespace
3. **Use as funções utilitárias** para casos comuns
4. **Documente novas constantes** com comentários claros
5. **Mantenha a organização** por categoria 