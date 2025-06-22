"""
Level Manager - Handles loading and transitioning between game levels
"""

import json
import os
from src.components.background_component import BackgroundComponent
from src.components.text_component import TextComponent
from src.components.menu_button import MenuButton
from src.components.input_button import InputButton
from src.components.and_gate import ANDGate
from src.components.led_component import LEDComponent


class LevelManager:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.current_level = None
        self.levels_dir = "levels"
        
        # Callback mappings
        self.callbacks = {
            "start_game": self.start_game,
            "exit_game": self.exit_game,
            "back_to_menu": self.back_to_menu,
            "next_level": self.next_level,
            "complete_level": self.complete_level
        }
        
        # Store components for reference
        self.input_buttons = []
        self.and_gates = []
        self.leds = []
        
        # Level progression
        self.level_sequence = ["game_level", "level2"]
        self.current_level_index = 0
    
    def load_level(self, level_name):
        """Load a level from JSON file"""
        level_file = os.path.join(self.levels_dir, f"{level_name}.json")
        
        if not os.path.exists(level_file):
            print(f"Level file not found: {level_file}")
            return False
        
        try:
            with open(level_file, 'r') as f:
                level_data = json.load(f)
            
            # Clear current level
            self.clear_current_level()
            
            # Load background
            if "background" in level_data:
                background = BackgroundComponent(shader_manager=self.game_engine.get_shader_manager())
                self.game_engine.add_component(background)
            
            # Load components
            if "components" in level_data:
                for component_data in level_data["components"]:
                    component = self.create_component(component_data)
                    if component:
                        self.game_engine.add_component(component)
            
            # Connect gates to their input buttons after all components are loaded
            self._connect_gates_to_inputs()
            
            # Connect LEDs to their input sources
            self._connect_leds_to_inputs()
            
            self.current_level = level_name
            print(f"Loaded level: {level_data.get('name', level_name)}")
            return True
            
        except Exception as e:
            print(f"Error loading level {level_name}: {e}")
            return False
    
    def create_component(self, component_data):
        """Create a component from JSON data"""
        component_type = component_data.get("type")
        shader_manager = self.game_engine.get_shader_manager()
        
        if component_type == "text":
            return TextComponent(
                text=component_data["text"],
                font_size=component_data["font_size"],
                color=tuple(component_data["color"]),
                position=tuple(component_data["position"]),
                window_size=tuple(component_data["window_size"]),
                shader_manager=shader_manager
            )
        
        elif component_type == "menu_button":
            callback_name = component_data.get("callback")
            callback = self.callbacks.get(callback_name) if callback_name else None
            
            return MenuButton(
                text=component_data["text"],
                position=tuple(component_data["position"]),
                size=tuple(component_data["size"]),
                color=tuple(component_data["color"]),
                hover_color=tuple(component_data["hover_color"]),
                window_size=tuple(component_data["window_size"]),
                shader_manager=shader_manager,
                callback=callback,
                bg_color=tuple(component_data["bg_color"]),
                border_color=tuple(component_data["border_color"])
            )
        
        elif component_type == "input_button":
            button = InputButton(
                text=component_data["text"],
                position=tuple(component_data["position"]),
                size=tuple(component_data.get("size", [100, 60])),
                off_color=tuple(component_data.get("off_color", [80, 80, 80])),
                on_color=tuple(component_data.get("on_color", [0, 255, 0])),
                text_color=tuple(component_data.get("text_color", [255, 255, 255])),
                window_size=tuple(component_data["window_size"]),
                shader_manager=shader_manager,
                initial_state=component_data.get("initial_state", False)
            )
            self.input_buttons.append(button)
            return button
        
        elif component_type == "and_gate":
            gate = ANDGate(
                position=tuple(component_data["position"]),
                size=tuple(component_data.get("size", [120, 80])),
                off_color=tuple(component_data.get("off_color", [80, 80, 80])),
                on_color=tuple(component_data.get("on_color", [0, 255, 0])),
                text_color=tuple(component_data.get("text_color", [255, 255, 255])),
                window_size=tuple(component_data["window_size"]),
                shader_manager=shader_manager
            )
            self.and_gates.append(gate)
            return gate
        
        elif component_type == "led":
            led = LEDComponent(
                position=tuple(component_data["position"]),
                radius=component_data.get("radius", 20),
                off_color=tuple(component_data.get("off_color", [64, 64, 64])),
                on_color=tuple(component_data.get("on_color", [0, 255, 0])),
                window_size=tuple(component_data["window_size"]),
                shader_manager=shader_manager
            )
            self.leds.append(led)
            return led
        
        elif component_type == "background":
            return BackgroundComponent(shader_manager=shader_manager)
        
        else:
            print(f"Unknown component type: {component_type}")
            return None
    
    def _connect_gates_to_inputs(self):
        """Connect AND gates to their input buttons based on component IDs"""
        # This method can be extended to handle connections based on component IDs
        # For now, we'll connect all input buttons to the first AND gate
        if self.and_gates and self.input_buttons:
            for gate in self.and_gates:
                for button in self.input_buttons:
                    gate.add_input_button(button)
    
    def _connect_leds_to_inputs(self):
        """Connect LEDs to their input sources based on component IDs"""
        # For now, connect all LEDs to the first AND gate
        if self.leds and self.and_gates:
            for led in self.leds:
                led.set_input_source(self.and_gates[0])
    
    def clear_current_level(self):
        """Clear all components from current level"""
        self.game_engine.clear_components()
        self.input_buttons.clear()
        self.and_gates.clear()
        self.leds.clear()
    
    def check_level_completion(self):
        """Check if the current level is completed"""
        if self.current_level == "game_level":
            # Level 1 is completed when the AND gate output is ON (both inputs are ON)
            if self.and_gates and self.and_gates[0].get_result():
                return True
        elif self.current_level == "level2":
            # Level 2 is completed when the AND gate output is ON (both inputs are ON)
            if self.and_gates and self.and_gates[0].get_result():
                return True
        return False
    
    def add_completion_button(self):
        """Add completion button when level is completed"""
        if self.check_level_completion():
            # Add completion button
            if self.current_level == "game_level":
                # Add "Next Level" button for level 1
                next_button = MenuButton(
                    text="Next Level",
                    position=(300, 400),
                    size=(200, 50),
                    color=(255, 255, 255),
                    hover_color=(200, 255, 200),
                    window_size=(800, 600),
                    shader_manager=self.game_engine.get_shader_manager(),
                    callback=self.next_level,
                    bg_color=(60, 120, 60),
                    border_color=(100, 180, 100)
                )
                self.game_engine.add_component(next_button)
                
            elif self.current_level == "level2":
                # Add "Back to Menu" button for final level
                menu_button = MenuButton(
                    text="Back to Menu",
                    position=(300, 400),
                    size=(200, 50),
                    color=(255, 255, 255),
                    hover_color=(200, 200, 255),
                    window_size=(800, 600),
                    shader_manager=self.game_engine.get_shader_manager(),
                    callback=self.back_to_menu,
                    bg_color=(60, 60, 120),
                    border_color=(100, 100, 180)
                )
                self.game_engine.add_component(menu_button)
    
    # Callback methods
    def start_game(self):
        """Callback for start game button"""
        print("Starting game...")
        self.current_level_index = 0
        self.load_level("game_level")
    
    def exit_game(self):
        """Callback for exit game button"""
        print("Exiting game...")
        import sys
        sys.exit(0)
    
    def back_to_menu(self):
        """Callback for back to menu button"""
        print("Returning to menu...")
        self.current_level_index = 0
        self.load_level("menu")
    
    def next_level(self):
        """Callback for next level button"""
        print("Loading next level...")
        self.current_level_index += 1
        if self.current_level_index < len(self.level_sequence):
            next_level = self.level_sequence[self.current_level_index]
            self.load_level(next_level)
        else:
            # All levels completed, go back to menu
            self.back_to_menu()
    
    def complete_level(self):
        """Callback for level completion"""
        print("Level completed!")
        self.add_completion_button() 