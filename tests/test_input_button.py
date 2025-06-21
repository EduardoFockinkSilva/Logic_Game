"""
Test for Input Button component
"""

import unittest
from unittest.mock import Mock, patch
import pygame
from src.components.input_button import InputButton


class TestInputButton(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.button = InputButton(
            text="Test Button",
            position=(100, 100),
            size=(100, 60),
            window_size=(800, 600)
        )
    
    def test_initial_state(self):
        """Test initial state of input button"""
        self.assertFalse(self.button.state)
        self.assertFalse(self.button.is_hovered)
        self.assertFalse(self.button.is_clicked)
    
    def test_set_state(self):
        """Test setting button state"""
        self.button.set_state(True)
        self.assertTrue(self.button.state)
        
        self.button.set_state(False)
        self.assertFalse(self.button.state)
    
    def test_get_state(self):
        """Test getting button state"""
        self.button.state = True
        self.assertTrue(self.button.get_state())
        
        self.button.state = False
        self.assertFalse(self.button.get_state())
    
    def test_check_hover(self):
        """Test hover detection"""
        # Test hover inside button
        result = self.button._check_hover(150, 130)
        self.assertTrue(result)
        
        # Test hover outside button (left)
        result = self.button._check_hover(50, 130)
        self.assertFalse(result)
        
        # Test hover outside button (right)
        result = self.button._check_hover(250, 130)
        self.assertFalse(result)
        
        # Test hover outside button (above)
        result = self.button._check_hover(150, 50)
        self.assertFalse(result)
        
        # Test hover outside button (below)
        result = self.button._check_hover(150, 200)
        self.assertFalse(result)
    
    def test_handle_mouse_event_click(self):
        """Test mouse click event handling"""
        # Create a mock mouse click event
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (150, 130)  # Inside button
        
        # Test click inside button
        result = self.button.handle_mouse_event(event)
        self.assertTrue(result)
        self.assertTrue(self.button.is_clicked)
        self.assertTrue(self.button.state)  # Should toggle to True
        
        # Test click outside button
        event.pos = (50, 50)  # Outside button
        result = self.button.handle_mouse_event(event)
        self.assertFalse(result)
    
    def test_handle_mouse_event_release(self):
        """Test mouse release event handling"""
        # Set up button as clicked
        self.button.is_clicked = True
        
        # Create a mock mouse release event
        event = Mock()
        event.type = pygame.MOUSEBUTTONUP
        event.button = 1
        
        result = self.button.handle_mouse_event(event)
        self.assertFalse(result)
        self.assertFalse(self.button.is_clicked)
    
    def test_handle_mouse_event_motion(self):
        """Test mouse motion event handling"""
        # Create a mock mouse motion event
        event = Mock()
        event.type = pygame.MOUSEMOTION
        
        # Test motion inside button
        event.pos = (150, 130)
        result = self.button.handle_mouse_event(event)
        self.assertFalse(result)
        self.assertTrue(self.button.is_hovered)
        
        # Test motion outside button
        event.pos = (50, 50)
        result = self.button.handle_mouse_event(event)
        self.assertFalse(result)
        self.assertFalse(self.button.is_hovered)
    
    def test_toggle_behavior(self):
        """Test that clicking toggles the button state"""
        # Initial state should be False
        self.assertFalse(self.button.state)
        
        # Create click event
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1
        event.pos = (150, 130)
        
        # First click should set to True
        self.button.handle_mouse_event(event)
        self.assertTrue(self.button.state)
        
        # Second click should set to False
        self.button.handle_mouse_event(event)
        self.assertFalse(self.button.state)
    
    def test_initial_state_parameter(self):
        """Test that initial_state parameter works correctly"""
        # Test with initial_state=True
        button_true = InputButton(
            text="True Button",
            position=(100, 100),
            initial_state=True,
            window_size=(800, 600)
        )
        self.assertTrue(button_true.state)
        
        # Test with initial_state=False
        button_false = InputButton(
            text="False Button",
            position=(100, 100),
            initial_state=False,
            window_size=(800, 600)
        )
        self.assertFalse(button_false.state)


if __name__ == '__main__':
    unittest.main() 