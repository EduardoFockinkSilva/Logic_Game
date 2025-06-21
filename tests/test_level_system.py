import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game_engine import GameEngine
from src.core.level_manager import LevelManager

def test_level_loading():
    """Test if levels can be loaded correctly"""
    print("=== Testing Level System ===")
    
    # Create game engine
    engine = GameEngine(width=800, height=600, title="Level System Test")
    
    # Create level manager
    level_manager = LevelManager(engine)
    
    # Test loading menu level
    print("Loading menu level...")
    success = level_manager.load_level("menu")
    if success:
        print("✅ Menu level loaded successfully")
        print(f"Current level: {level_manager.current_level}")
        print(f"Components loaded: {len(engine.components)}")
    else:
        print("❌ Failed to load menu level")
    
    # Test loading game level
    print("\nLoading game level...")
    success = level_manager.load_level("game_level")
    if success:
        print("✅ Game level loaded successfully")
        print(f"Current level: {level_manager.current_level}")
        print(f"Components loaded: {len(engine.components)}")
    else:
        print("❌ Failed to load game level")
    
    # Test going back to menu
    print("\nGoing back to menu...")
    success = level_manager.load_level("menu")
    if success:
        print("✅ Returned to menu successfully")
        print(f"Current level: {level_manager.current_level}")
        print(f"Components loaded: {len(engine.components)}")
    else:
        print("❌ Failed to return to menu")
    
    print("\n=== Level System Test Complete ===")

if __name__ == "__main__":
    test_level_loading() 