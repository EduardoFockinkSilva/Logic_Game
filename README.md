# 🎮 Puzzle Lógico

Jogo educacional que ensina portas lógicas (AND, OR, NOT) através de puzzles interativos.

## 🎯 O que é?

- **Jogo educativo** para aprender lógica digital
- **Interface visual** com botões, portas lógicas e LEDs
- **Níveis progressivos** de dificuldade
- **Feedback em tempo real** da propagação de sinais

## 🚀 Como executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o jogo
python main.py
```

## 🎮 Como jogar

1. **Clique nos botões** para ligar/desligar entradas
2. **Observe o LED final** - ele acende quando a condição é verdadeira
3. **Complete o nível** quando entender a lógica
4. **Avance** para o próximo nível

## 🎛️ Controles

- **Mouse**: Clique para interagir
- **ESC**: Sair
- **F1**: Debug HUD

## 📁 Estrutura

```
game/
├── src/           # Código fonte
├── levels/        # Níveis do jogo
├── tests/         # Testes
└── main.py        # Executar aqui
```

## 🧪 Testes

```bash
pytest tests/
```

## 📋 Pré-requisitos

- Python 3.8+
- OpenGL 3.3+

---

**Desenvolvido para educação em computação gráfica e lógica digital** 