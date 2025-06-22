# 🎮 Puzzle Lógico - Jogo Educacional de Portas Lógicas

Um jogo educacional desenvolvido em **Python** que ensina conceitos de **lógica digital** através de puzzles interativos com portas lógicas (AND, OR, NOT). O projeto utiliza **OpenGL** para renderização gráfica e implementa uma **arquitetura modular baseada em componentes** com sistema de níveis JSON.

## 🎯 Visão Geral

O jogo permite aos jogadores:
- 🎛️ **Interagir com botões de entrada** (toggle on/off)
- 🔗 **Conectar entradas a portas lógicas** visualmente
- ⚡ **Observar a propagação de sinais** em tempo real
- 💡 **Ver o resultado final em LEDs** com feedback visual
- 📈 **Progredir através de níveis** com complexidade crescente
- 🎨 **Interface gráfica moderna** com shaders OpenGL

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
game/
├── src/                    # Código fonte principal
│   ├── components/         # Sistema de componentes
│   │   ├── core/          # Componentes base e fábricas
│   │   ├── logic/         # Portas lógicas e elementos
│   │   └── ui/            # Componentes de interface
│   ├── core/              # Lógica central do jogo
│   └── shaders/           # Shaders GLSL
├── levels/                # Definições de níveis (JSON)
├── tests/                 # Testes automatizados
└── main.py               # Ponto de entrada
```

### 🧩 Padrões Arquiteturais Implementados

#### 1. **Component-Based Architecture**
Sistema flexível de componentes com hierarquia bem definida:

```python
Component (ABC)
├── RenderableComponent
│   └── TexturedComponent
│       └── LogicGate
│           ├── ANDGate
│           ├── ORGate
│           └── NOTGate
└── ButtonBase
    ├── InputButton
    └── MenuButton
```

#### 2. **Factory Pattern**
Sistema de fábricas para criação dinâmica de componentes:

```python
# Registro de componentes
component_registry.register_logic_gate('AND', ANDGate)
component_registry.register_logic_gate('OR', ORGate)

# Criação via fábrica
gate = create_logic_gate('AND', position=(100, 100))
```

#### 3. **Protocol-Based Interfaces**
Uso de Protocols Python para contratos entre componentes:

```python
@runtime_checkable
class LogicInputSource(Protocol):
    def get_result(self) -> bool: ...

@runtime_checkable
class RenderableState(Protocol):
    def get_render_color(self) -> Tuple[int, int, int]: ...
    def get_position(self) -> Tuple[int, int]: ...
```

#### 4. **Level System**
Sistema de níveis baseado em JSON para fácil criação de puzzles:

```json
{
  "name": "Level 1 - AND Gate Tutorial",
  "components": [
    {
      "id": "input_button_1",
      "type": "input_button",
      "position": [180, 220],
      "size": [60, 60]
    }
  ],
  "connections": [
    {
      "from": "input_button_1",
      "to": "and_gate_1",
      "input_index": 0
    }
  ]
}
```

## 🔧 Componentes Principais

### 🧠 Portas Lógicas

#### AND Gate
- **Lógica**: `all(inputs)` - True apenas se todas as entradas forem True
- **Cores**: Cinza (off) → Amarelo claro (on)
- **Uso**: Detecção de condições múltiplas

#### OR Gate  
- **Lógica**: `any(inputs)` - True se pelo menos uma entrada for True
- **Cores**: Cinza (off) → Rosa claro (on)
- **Uso**: Alternativas ou condições opcionais

#### NOT Gate
- **Lógica**: `not first_input` - Inverte o valor da primeira entrada
- **Cores**: Cinza (off) → Azul claro (on)
- **Uso**: Inversão de lógica

### 🎛️ Elementos de Interface

#### Input Button
- **Função**: Botão toggle para entrada de dados
- **Interação**: Clique para alternar estado
- **Feedback**: Vermelho (off) → Verde (on)

#### LED Component
- **Função**: Indicador visual do resultado
- **Estados**: Apagado (cinza escuro) → Aceso (verde brilhante)
- **Posicionamento**: Geralmente no final do circuito

#### Menu Button
- **Função**: Navegação entre níveis e menu
- **Estados**: Normal → Hover → Clicado
- **Callbacks**: Configuráveis via JSON

## 🎨 Sistema de Renderização

### OpenGL Moderno
- **Vertex Shaders**: Transformação de geometria
- **Fragment Shaders**: Efeitos visuais e cores
- **VAO/VBO**: Renderização eficiente de quads
- **Blending**: Transparências e efeitos visuais

### Shaders Implementados
- `background_*`: Fundo gradiente animado
- `button_*`: Botões com efeitos de hover
- `gate_*`: Portas lógicas com feedback visual
- `led_*`: LEDs com brilho e animação
- `text_*`: Renderização de texto

## 🎮 Como Jogar

### Controles
- **Mouse**: Clique para interagir com botões
- **ESC**: Sair do jogo
- **F1**: Alternar HUD de debug
- **F2**: Mostrar informações das conexões

### Objetivo
1. **Analise o circuito** apresentado no nível
2. **Clique nos botões de entrada** para testar diferentes combinações
3. **Observe o LED final** - ele deve acender quando a condição for verdadeira
4. **Complete o nível** quando entender a lógica
5. **Avance para o próximo nível** com complexidade crescente

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- OpenGL 3.3+ (suporte a shaders)

### Instalação
```bash
# Clone o repositório
git clone <repository-url>
cd game

# Instale as dependências
pip install -r requirements.txt
```

### Execução
```bash
# Execute o jogo
python main.py
```

### Dependências
```
pygame>=2.5.0          # Sistema de janelas e eventos
PyOpenGL>=3.1.6        # Renderização OpenGL
numpy>=1.24.0          # Operações matemáticas
pytest>=7.0.0          # Testes automatizados
pytest-cov>=4.0.0      # Cobertura de testes
```

## 🧪 Testes

O projeto inclui uma suíte completa de testes:

```bash
# Executar todos os testes
pytest tests/

# Executar com cobertura
pytest tests/ --cov=src

# Testes específicos
pytest tests/test_and_gate.py
pytest tests/test_game_integration.py
```

### Cobertura de Testes
- ✅ **Portas lógicas**: AND, OR, NOT
- ✅ **Componentes de interface**: Botões, LEDs, Textos
- ✅ **Sistema de conexões**: Visual e lógica
- ✅ **Integração**: Carregamento de níveis
- ✅ **Renderização**: Shaders e OpenGL

## 📁 Estrutura de Níveis

### Nível 1: Tutorial AND
- **Objetivo**: Aprender porta AND
- **Componentes**: 2 inputs + 1 AND gate + 1 LED
- **Lógica**: LED acende apenas quando ambos inputs estão ON

### Nível 2: OR + NOT
- **Objetivo**: Combinar portas OR e NOT
- **Componentes**: 2 inputs + 1 OR gate + 1 NOT gate + 1 LED
- **Lógica**: `(Input1 OR Input2) AND (NOT Input2)`

### Nível 3: Circuito Complexo
- **Objetivo**: Múltiplas portas em cascata
- **Componentes**: 3+ inputs + múltiplas portas + LED
- **Lógica**: Expressão booleana complexa

## 🔧 Desenvolvimento

### Adicionando Novos Componentes
1. Crie a classe do componente herdando de `Component`
2. Implemente as interfaces necessárias (`LogicInputSource`, `RenderableState`, etc.)
3. Registre no `ComponentRegistry`
4. Adicione shaders se necessário
5. Crie testes unitários

### Criando Novos Níveis
1. Crie arquivo JSON em `levels/`
2. Defina componentes e suas propriedades
3. Especifique conexões entre componentes
4. Teste o nível com `test_level_system.py`

### Arquitetura de Extensibilidade
- **Componentes**: Fácil adição de novos tipos
- **Shaders**: Sistema modular de renderização
- **Níveis**: Configuração via JSON
- **Testes**: Cobertura completa para validação

## 🎯 Objetivos Educacionais

### Conceitos de Lógica Digital
- **Álgebra Booleana**: Operações AND, OR, NOT
- **Tabelas Verdade**: Relação entre entradas e saídas
- **Propagação de Sinais**: Como valores se propagam pelo circuito
- **Design de Circuitos**: Organização lógica de componentes

### Habilidades Desenvolvidas
- **Pensamento Lógico**: Análise de condições
- **Resolução de Problemas**: Debugging de circuitos
- **Visualização**: Compreensão de fluxo de dados
- **Experimentação**: Teste de diferentes cenários

## 📊 Métricas do Projeto

- **Linhas de Código**: ~2000+ linhas
- **Componentes**: 10+ tipos diferentes
- **Shaders**: 8 shaders GLSL
- **Níveis**: 3+ níveis configuráveis
- **Testes**: 90%+ cobertura de código
- **Arquitetura**: 5 padrões de design implementados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- **Pygame**: Sistema de janelas e eventos
- **PyOpenGL**: Renderização OpenGL
- **NumPy**: Operações matemáticas eficientes
- **Pytest**: Framework de testes

---

**Desenvolvido com ❤️ para educação em computação gráfica e lógica digital** 