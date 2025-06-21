#!/usr/bin/env python3
"""
Test script to verify positioning of input buttons and AND gates
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from src.core.game_engine import GameEngine
from src.core.level_manager import LevelManager
from src.components.input_button import InputButton
from src.components.and_gate import ANDGate


def test_positioning():
    """Test the positioning of components"""
    print("Testing component positioning...")
    
    # Create a simple test setup
    engine = GameEngine(width=800, height=600, title="Positioning Test")
    engine.initialize()
    
    # Create test components with known positions
    input_button = InputButton(
        text="Test",
        position=(100, 100),
        size=(80, 80),
        window_size=(800, 600),
        shader_manager=engine.get_shader_manager()
    )
    
    and_gate = ANDGate(
        position=(300, 100),
        size=(120, 80),
        window_size=(800, 600),
        shader_manager=engine.get_shader_manager()
    )
    
    # Add components to engine
    engine.add_component(input_button)
    engine.add_component(and_gate)
    
    print(f"Input button position: {input_button.position}")
    print(f"AND gate position: {and_gate.position}")
    print("Components added successfully!")
    
    # Test coordinate conversion
    x, y = input_button.position
    gl_x = (x / 800) * 2 - 1
    gl_y = 1 - (y / 600) * 2
    print(f"Input button OpenGL coords: ({gl_x:.3f}, {gl_y:.3f})")
    
    x, y = and_gate.position
    gl_x = (x / 800) * 2 - 1
    gl_y = 1 - (y / 600) * 2
    print(f"AND gate OpenGL coords: ({gl_x:.3f}, {gl_y:.3f})")
    
    print("Positioning test completed!")


if __name__ == "__main__":
    test_positioning() 