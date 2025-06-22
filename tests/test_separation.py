#!/usr/bin/env python3
"""
Test script to verify component separation and interface compliance
"""

from src.components.and_gate import ANDGate
from src.components.input_button import InputButton
from src.components.interfaces import RenderableState

def test_component_separation():
    """Test that components are properly separated and implement interfaces"""
    print("Testing component separation and interfaces...")
    
    # Create components directly
    and_gate = ANDGate(position=(100, 100))
    input_button = InputButton(text="Input 1", position=(200, 100))
    
    print(f"Created AND Gate: {type(and_gate)}")
    print(f"Created Input Button: {type(input_button)}")
    
    # Test interface compliance
    print("\nTesting interface compliance...")
    
    # Verificar se implementam RenderableState
    if isinstance(and_gate, RenderableState):
        print("✓ AND Gate implementa RenderableState")
        print(f"  Position: {and_gate.get_position()}")
        print(f"  Size: {and_gate.get_size()}")
    else:
        print("✗ AND Gate não implementa RenderableState")
    
    if isinstance(input_button, RenderableState):
        print("✓ Input Button implementa RenderableState")
        print(f"  Position: {input_button.get_position()}")
        print(f"  Size: {input_button.get_size()}")
    else:
        print("✗ Input Button não implementa RenderableState")
    
    print("\nComponent separation test completed!")


if __name__ == "__main__":
    test_component_separation() 