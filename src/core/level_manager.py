"""
Level Manager - Handles loading and transitioning between game levels
"""

import json
import os
import glob
from src.components.factories import create_component_from_data, create_background
from src.components.background_component import BackgroundComponent
from src.components.text_component import TextComponent
from src.components.menu_button import MenuButton
from src.components.input_button import InputButton
from src.components.and_gate import ANDGate
from src.components.or_gate import ORGate
from src.components.not_gate import NOTGate
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
        
        # Store components for reference with IDs
        self.components_by_id = {}
        self.input_buttons = []
        self.and_gates = []
        self.or_gates = []
        self.not_gates = []
        self.leds = []
        
        # Level progression - automatically detect all levels except menu.json
        self.level_sequence = self._discover_levels()
        self.current_level_index = 0
        
        # Control for completion button to avoid duplicates
        self.completion_button_added = False
    
    def _discover_levels(self):
        """Automatically discover all level files except menu.json, sorted by filename."""
        level_files = glob.glob(os.path.join(self.levels_dir, '*.json'))
        level_names = [os.path.splitext(os.path.basename(f))[0] for f in level_files if os.path.basename(f) != 'menu.json']
        # Sort by filename (you can customize this if you want a different order)
        return sorted(level_names)
    
    def load_level(self, level_name):
        """Load a level from JSON file"""
        print(f"Loading level: {level_name}")
        
        # Clear current level
        self.clear_current_level()
        
        # Reset completion button flag for new level
        self.completion_button_added = False
        
        # Load level file
        level_file = os.path.join(self.levels_dir, f"{level_name}.json")
        if not os.path.exists(level_file):
            print(f"Level file not found: {level_file}")
            return
        
        try:
            with open(level_file, 'r') as f:
                level_data = json.load(f)
            
            # Load background using factory
            if "background" in level_data:
                background_data = level_data["background"]
                if isinstance(background_data, dict):
                    # Background with specific configuration
                    background = create_component_from_data(
                        background_data, 
                        self.game_engine.get_shader_manager()
                    )
                else:
                    # Simple background
                    background = create_background(
                        'BACKGROUND', 
                        shader_manager=self.game_engine.get_shader_manager()
                    )
                
                if background:
                    self.game_engine.add_component(background)
            
            # Load components using factory system
            if "components" in level_data:
                for component_data in level_data["components"]:
                    component = self.create_component(component_data)
                    if component:
                        self.game_engine.add_component(component)
            
            # Process explicit connections from JSON AFTER all components are added to engine
            if "connections" in level_data:
                self._process_explicit_connections(level_data["connections"])
            else:
                # Fallback to automatic connections
                self._connect_gates_to_inputs()
                self._connect_leds_to_inputs()
            
            self.current_level = level_name
            print(f"Loaded level: {level_data.get('name', level_name)}")
            return True
            
        except Exception as e:
            print(f"Error loading level {level_name}: {e}")
            return False
    
    def _process_explicit_connections(self, connections_data):
        """
        Process explicit connections defined in the JSON file.
        
        Expected format:
        "connections": [
            {
                "from": "input_button_1",
                "to": "and_gate_1",
                "input_index": 0
            },
            {
                "from": "and_gate_1", 
                "to": "led_1"
            }
        ]
        """
        print(f"[LevelManager] Processing {len(connections_data)} explicit connections...")
        
        connection_manager = self.game_engine.get_connection_manager()
        
        for connection in connections_data:
            from_id = connection.get("from")
            to_id = connection.get("to")
            input_index = connection.get("input_index", 0)
            
            from_component = self.components_by_id.get(from_id)
            to_component = self.components_by_id.get(to_id)
            
            if not from_component or not to_component:
                print(f"[LevelManager] Warning: Connection {from_id} -> {to_id} failed (component not found)")
                continue
            
            # Connect based on component types
            if hasattr(to_component, 'add_input'):
                # Connecting to a gate
                to_component.add_input(from_component)
                print(f"[LevelManager] Connected {from_id} -> {to_id} (input {input_index})")
                
                # Create visual connection
                connection_manager.create_connection_for_components(from_component, to_component)
                
            elif hasattr(to_component, 'set_input_source'):
                # Connecting to an LED
                to_component.set_input_source(from_component)
                print(f"[LevelManager] Connected {from_id} -> {to_id} (LED input)")
                
                # Create visual connection
                connection_manager.create_connection_for_components(from_component, to_component)
    
    def create_component(self, component_data):
        """Create a component from JSON data using the factory system"""
        component_type = component_data.get("type")
        component_id = component_data.get("id", f"{component_type}_{len(self.components_by_id)}")
        
        # Use factory to create component with callbacks
        component = create_component_from_data(
            component_data, 
            self.game_engine.get_shader_manager(),
            self.callbacks
        )
        
        if component:
            # Store component with ID for connections
            self.components_by_id[component_id] = component
            
            # Add to appropriate lists for automatic connections
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
            
            print(f"[LevelManager] Created {component_type} with ID: {component_id}")
        else:
            print(f"[LevelManager] Failed to create component: {component_type}")
        
        return component
    
    def _connect_gates_to_inputs(self):
        """Connect all gates to their input buttons based on component IDs"""
        # Connect all input buttons to all gates (for now, simple approach)
        all_gates = self.and_gates + self.or_gates + self.not_gates
        if all_gates and self.input_buttons:
            for gate in all_gates:
                for button in self.input_buttons:
                    gate.add_input(button)
            print(f"[LevelManager] Connected {len(self.input_buttons)} inputs to {len(all_gates)} gates")
    
    def _connect_leds_to_inputs(self):
        """Connect LEDs to their input sources based on component IDs"""
        # Connect all LEDs to the first available gate
        all_gates = self.and_gates + self.or_gates + self.not_gates
        if self.leds and all_gates:
            for led in self.leds:
                led.set_input_source(all_gates[0])
            print(f"[LevelManager] Connected {len(self.leds)} LEDs to gates")
    
    def clear_current_level(self):
        """Clear all components from current level"""
        self.game_engine.clear_components()
        self.components_by_id.clear()
        self.input_buttons.clear()
        self.and_gates.clear()
        self.or_gates.clear()
        self.not_gates.clear()
        self.leds.clear()
    
    def check_level_completion(self):
        """Check if the current level is completed (LED must be ON)."""
        # Only check LED state - LED represents the final output of the level
        if self.leds:
            for led in self.leds:
                if hasattr(led, 'get_state') and led.get_state():
                    return True
        return False
    
    def add_completion_button(self):
        """Add completion button when level is completed (dynamic for all levels)."""
        # Only add completion button if level is completed and button hasn't been added yet
        if self.check_level_completion() and not self.completion_button_added:
            # If not last level, show Next Level; else, show Finish
            if self.current_level_index < len(self.level_sequence) - 1:
                next_button = MenuButton(
                    text="Next Level",
                    position=(575, 525),
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
            else:
                finish_button = MenuButton(
                    text="Finish",
                    position=(575, 525),
                    size=(200, 50),
                    color=(255, 255, 255),
                    hover_color=(200, 200, 255),
                    window_size=(800, 600),
                    shader_manager=self.game_engine.get_shader_manager(),
                    callback=self.back_to_menu,
                    bg_color=(60, 60, 120),
                    border_color=(100, 100, 180)
                )
                self.game_engine.add_component(finish_button)
            
            # Mark that completion button has been added
            self.completion_button_added = True
    
    # Callback methods
    def start_game(self):
        """Callback for start game button"""
        print("Starting game...")
        self.current_level_index = 0
        if self.level_sequence:
            first_level = self.level_sequence[0]
            self.load_level(first_level)
        else:
            print("No levels found!")
            self.back_to_menu()
    
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