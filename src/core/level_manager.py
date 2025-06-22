"""
Gerenciador de níveis - carrega e transiciona entre níveis
"""

import json
import os
import glob
from src.components.core.factories import create_component_from_data, create_background
from src.components.ui.menu_button import MenuButton


class LevelManager:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.current_level = None
        self.levels_dir = "levels"
        
        # Callbacks
        self.callbacks = {
            "start_game": self.start_game,
            "exit_game": self.exit_game,
            "back_to_menu": self.back_to_menu,
            "next_level": self.next_level,
            "complete_level": self.complete_level
        }
        
        # Componentes por ID
        self.components_by_id = {}
        self.input_buttons = []
        self.and_gates = []
        self.or_gates = []
        self.not_gates = []
        self.leds = []
        
        # Sequência de níveis
        self.level_sequence = self._discover_levels()
        self.current_level_index = 0
        self.completion_button_added = False
    
    def _discover_levels(self):
        """Descobre automaticamente todos os arquivos de nível exceto menu.json"""
        level_files = glob.glob(os.path.join(self.levels_dir, '*.json'))
        level_names = [os.path.splitext(os.path.basename(f))[0] for f in level_files if os.path.basename(f) != 'menu.json']
        return sorted(level_names)
    
    def load_level(self, level_name):
        """Carrega nível do arquivo JSON"""
        print(f"Carregando nível: {level_name}")
        
        self.clear_current_level()
        self.completion_button_added = False
        
        level_file = os.path.join(self.levels_dir, f"{level_name}.json")
        if not os.path.exists(level_file):
            print(f"Arquivo de nível não encontrado: {level_file}")
            return
        
        try:
            with open(level_file, 'r') as f:
                level_data = json.load(f)
            
            # Carregar background
            if "background" in level_data:
                background_data = level_data["background"]
                if isinstance(background_data, dict):
                    background = create_component_from_data(
                        background_data, 
                        self.game_engine.get_shader_manager()
                    )
                else:
                    background = create_background(
                        'BACKGROUND', 
                        shader_manager=self.game_engine.get_shader_manager()
                    )
                
                if background:
                    self.game_engine.add_component(background)
            
            # Carregar componentes
            if "components" in level_data:
                for component_data in level_data["components"]:
                    component = self.create_component(component_data)
                    if component:
                        self.game_engine.add_component(component)
            
            # Processar conexões
            if "connections" in level_data:
                self._process_explicit_connections(level_data["connections"])
            else:
                self._connect_gates_to_inputs()
                self._connect_leds_to_inputs()
            
            self.current_level = level_name
            print(f"Nível carregado: {level_data.get('name', level_name)}")
            return True
            
        except Exception as e:
            print(f"Erro ao carregar nível {level_name}: {e}")
            return False
    
    def _process_explicit_connections(self, connections_data):
        """Processa conexões explícitas definidas no JSON"""
        print(f"Processando {len(connections_data)} conexões explícitas...")
        
        connection_manager = self.game_engine.get_connection_manager()
        
        for connection in connections_data:
            from_id = connection.get("from")
            to_id = connection.get("to")
            input_index = connection.get("input_index", 0)
            
            from_component = self.components_by_id.get(from_id)
            to_component = self.components_by_id.get(to_id)
            
            if not from_component or not to_component:
                print(f"Aviso: Conexão {from_id} -> {to_id} falhou (componente não encontrado)")
                continue
            
            # Conectar baseado no tipo de componente
            if hasattr(to_component, 'add_input'):
                to_component.add_input(from_component)
                print(f"Conectado {from_id} -> {to_id} (entrada {input_index})")
                connection_manager.create_connection_for_components(from_component, to_component)
                
            elif hasattr(to_component, 'set_input_source'):
                to_component.set_input_source(from_component)
                print(f"Conectado {from_id} -> {to_id} (entrada LED)")
                connection_manager.create_connection_for_components(from_component, to_component)
    
    def create_component(self, component_data):
        """Cria componente a partir de dados JSON usando factory"""
        component_type = component_data.get("type")
        component_id = component_data.get("id", f"{component_type}_{len(self.components_by_id)}")
        
        component = create_component_from_data(
            component_data, 
            self.game_engine.get_shader_manager(),
            self.callbacks
        )
        
        if component:
            self.components_by_id[component_id] = component
            
            # Adicionar às listas apropriadas
            if component_type == "input_button":
                self.input_buttons.append(component)
            elif component_type == "and_gate":
                self.and_gates.append(component)
            elif component_type == "or_gate":
                self.or_gates.append(component)
            elif component_type == "not_gate":
                self.not_gates.append(component)
            elif component_type == "led":
                self.leds.append(component)
            
            print(f"Criado {component_type} com ID: {component_id}")
        else:
            print(f"Falha ao criar componente: {component_type}")
        
        return component
    
    def _connect_gates_to_inputs(self):
        """Conecta todas as portas aos botões de entrada"""
        all_gates = self.and_gates + self.or_gates + self.not_gates
        if all_gates and self.input_buttons:
            for gate in all_gates:
                for button in self.input_buttons:
                    gate.add_input(button)
            print(f"Conectados {len(self.input_buttons)} inputs a {len(all_gates)} portas")
    
    def _connect_leds_to_inputs(self):
        """Conecta LEDs às suas fontes de entrada"""
        all_gates = self.and_gates + self.or_gates + self.not_gates
        if self.leds and all_gates:
            for led in self.leds:
                led.set_input_source(all_gates[0])
            print(f"Conectados {len(self.leds)} LEDs às portas")
    
    def clear_current_level(self):
        """Limpa todos os componentes do nível atual"""
        self.game_engine.clear_components()
        self.components_by_id.clear()
        self.input_buttons.clear()
        self.and_gates.clear()
        self.or_gates.clear()
        self.not_gates.clear()
        self.leds.clear()
    
    def check_level_completion(self):
        """Verifica se o nível atual foi completado (LED deve estar ON)"""
        if self.leds:
            for led in self.leds:
                if hasattr(led, 'get_state') and led.get_state():
                    return True
        return False
    
    def add_completion_button(self):
        """Adiciona botão de conclusão quando nível é completado"""
        if self.check_level_completion() and not self.completion_button_added:
            if self.current_level_index < len(self.level_sequence) - 1:
                next_button = MenuButton(
                    text="Next Level",
                    position=(675, 525),
                    size=(100, 45),
                    color=(255, 255, 255),
                    hover_color=(200, 255, 200),
                    window_size=(800, 600),
                    shader_manager=self.game_engine.get_shader_manager(),
                    callback=self.next_level,
                    bg_color=(60, 120, 60),
                    border_color=(100, 180, 100)
                )
                self.game_engine.add_component(next_button)
            else:
                finish_button = MenuButton(
                    text="Finish",
                    position=(675, 525),
                    size=(100, 45),
                    color=(255, 255, 255),
                    hover_color=(200, 200, 255),
                    window_size=(800, 600),
                    shader_manager=self.game_engine.get_shader_manager(),
                    callback=self.back_to_menu,
                    bg_color=(60, 60, 120),
                    border_color=(100, 100, 180)
                )
                self.game_engine.add_component(finish_button)
            
            self.completion_button_added = True
    
    # Callbacks
    def start_game(self):
        """Callback para botão iniciar jogo"""
        print("Iniciando jogo...")
        self.current_level_index = 0
        if self.level_sequence:
            first_level = self.level_sequence[0]
            self.load_level(first_level)
        else:
            print("Nenhum nível encontrado!")
            self.back_to_menu()
    
    def exit_game(self):
        """Callback para botão sair do jogo"""
        print("Saindo do jogo...")
        import sys
        sys.exit(0)
    
    def back_to_menu(self):
        """Callback para botão voltar ao menu"""
        print("Voltando ao menu...")
        self.current_level_index = 0
        self.load_level("menu")
    
    def next_level(self):
        """Callback para botão próximo nível"""
        print("Carregando próximo nível...")
        self.current_level_index += 1
        if self.current_level_index < len(self.level_sequence):
            next_level = self.level_sequence[self.current_level_index]
            self.load_level(next_level)
        else:
            self.back_to_menu()
    
    def complete_level(self):
        """Callback para conclusão de nível"""
        print("Nível completado!")
        self.add_completion_button() 