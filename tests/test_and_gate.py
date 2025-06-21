"""
Test for AND Gate component
"""

import unittest
from unittest.mock import Mock
from src.components.and_gate import ANDGate
from src.components.input_button import InputButton


class TestANDGate(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.gate = ANDGate(
            position=(100, 100),
            size=(120, 80),
            window_size=(800, 600)
        )
        
        # Create mock input buttons
        self.input1 = Mock(spec=InputButton)
        self.input2 = Mock(spec=InputButton)
        
    def test_and_gate_with_no_inputs(self):
        """Test AND gate with no input buttons"""
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_one_input_false(self):
        """Test AND gate with one input button set to False"""
        self.input1.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_one_input_true(self):
        """Test AND gate with one input button set to True"""
        self.input1.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_and_gate_with_two_inputs_both_false(self):
        """Test AND gate with two input buttons both False"""
        self.input1.get_state.return_value = False
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_two_inputs_one_true_one_false(self):
        """Test AND gate with two input buttons - one True, one False"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_two_inputs_both_true(self):
        """Test AND gate with two input buttons both True"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_add_and_remove_input_button(self):
        """Test adding and removing input buttons"""
        self.input1.get_state.return_value = True
        
        # Add button
        self.gate.add_input_button(self.input1)
        self.assertIn(self.input1, self.gate.input_buttons)
        
        # Remove button
        self.gate.remove_input_button(self.input1)
        self.assertNotIn(self.input1, self.gate.input_buttons)
    
    def test_duplicate_input_button(self):
        """Test that duplicate input buttons are not added"""
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input1)
        
        # Should only have one instance
        self.assertEqual(len(self.gate.input_buttons), 1)


if __name__ == '__main__':
    unittest.main() 