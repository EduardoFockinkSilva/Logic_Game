"""
Test for NOT Gate component
"""

import unittest
from unittest.mock import Mock
from src.components.not_gate import NOTGate
from src.components.input_button import InputButton


class TestNOTGate(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.gate = NOTGate(
            position=(100, 100),
            size=(120, 80),
            window_size=(800, 600)
        )
        
        # Create mock input buttons
        self.input1 = Mock(spec=InputButton)
        self.input2 = Mock(spec=InputButton)
        
    def test_not_gate_with_no_inputs(self):
        """Test NOT gate with no input buttons - should default to True"""
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_not_gate_with_one_input_false(self):
        """Test NOT gate with one input button set to False - should return True"""
        self.input1.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_not_gate_with_one_input_true(self):
        """Test NOT gate with one input button set to True - should return False"""
        self.input1.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_not_gate_with_multiple_inputs_uses_first(self):
        """Test NOT gate with multiple input buttons - should use only the first one"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertFalse(result)  # Should invert the first input (True -> False)
    
    def test_not_gate_with_multiple_inputs_first_false(self):
        """Test NOT gate with multiple input buttons - first False, others True"""
        self.input1.get_state.return_value = False
        self.input2.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertTrue(result)  # Should invert the first input (False -> True)
    
    def test_not_gate_inversion_logic(self):
        """Test NOT gate inversion logic thoroughly"""
        # Test False -> True
        self.input1.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        result = self.gate.get_result()
        self.assertTrue(result)
        
        # Test True -> False
        self.input1.get_state.return_value = True
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_add_and_remove_input_button(self):
        """Test adding and removing input buttons"""
        self.input1.get_state.return_value = True
        
        # Add button
        self.gate.add_input_button(self.input1)
        self.assertIn(self.input1, self.gate.input_buttons)
        
        # Remove button
        self.gate.remove_input_button(self.input1)
        self.assertNotIn(self.input1, self.gate.input_buttons)
        
        # After removal, should default to True
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_duplicate_input_button(self):
        """Test that duplicate input buttons are not added"""
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input1)
        
        # Should only have one instance
        self.assertEqual(len(self.gate.input_buttons), 1)
    
    def test_not_gate_initialization(self):
        """Test NOT gate initialization with custom colors"""
        gate = NOTGate(
            position=(200, 200),
            size=(150, 100),
            off_color=(100, 100, 100),
            on_color=(150, 200, 255),
            window_size=(1024, 768)
        )
        
        self.assertEqual(gate.position, (200, 200))
        self.assertEqual(gate.size, (150, 100))
        self.assertEqual(gate.off_color, (100, 100, 100))
        self.assertEqual(gate.on_color, (150, 200, 255))
        self.assertEqual(gate.window_size, (1024, 768))
        self.assertEqual(gate.input_buttons, [])
    
    def test_not_gate_with_input_buttons_parameter(self):
        """Test NOT gate initialization with input buttons parameter"""
        self.input1.get_state.return_value = False
        gate = NOTGate(
            position=(100, 100),
            input_buttons=[self.input1]
        )
        
        self.assertIn(self.input1, gate.input_buttons)
        self.assertTrue(gate.get_result())  # False -> True
    
    def test_not_gate_behavior_with_invalid_input(self):
        """Test NOT gate behavior when input button doesn't have get_state method"""
        class InvalidInput:
            pass
        
        invalid_input = InvalidInput()
        # This object has no get_state method
        self.gate.add_input_button(invalid_input)
        
        result = self.gate.get_result()
        # When input doesn't have get_state method, hasattr returns False, so result should be True
        self.assertTrue(result)
    
    def test_not_gate_multiple_operations(self):
        """Test NOT gate with multiple operations on the same input"""
        self.input1.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        
        # First operation
        result1 = self.gate.get_result()
        self.assertTrue(result1)
        
        # Change input state
        self.input1.get_state.return_value = True
        
        # Second operation
        result2 = self.gate.get_result()
        self.assertFalse(result2)
        
        # Change back
        self.input1.get_state.return_value = False
        result3 = self.gate.get_result()
        self.assertTrue(result3)


if __name__ == '__main__':
    unittest.main() 