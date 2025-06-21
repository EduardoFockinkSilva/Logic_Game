"""
Level Manager - Handles loading and transitioning between game levels
"""

import json
import os
from src.components.background_component import BackgroundComponent
from src.components.text_component import TextComponent
from src.components.menu_button import MenuButton


class LevelManager:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.current_level = None
        self.levels_dir = "levels"
        
        # Callback mappings
        self.callbacks = {
            "start_game": self.start_game,
            "exit_game": self.exit_game,
            "back_to_menu": self.back_to_menu
        }
    
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
        
        elif component_type == "background":
            return BackgroundComponent(shader_manager=shader_manager)
        
        else:
            print(f"Unknown component type: {component_type}")
            return None
    
    def clear_current_level(self):
        """Clear all components from current level"""
        self.game_engine.clear_components()
    
    # Callback methods
    def start_game(self):
        """Callback for start game button"""
        print("Starting game...")
        self.load_level("game_level")
    
    def exit_game(self):
        """Callback for exit game button"""
        print("Exiting game...")
        import sys
        sys.exit(0)
    
    def back_to_menu(self):
        """Callback for back to menu button"""
        print("Returning to menu...")
        self.load_level("menu") 