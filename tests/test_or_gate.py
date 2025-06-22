"""
Test for OR Gate component
"""

import unittest
from unittest.mock import Mock
from src.components.or_gate import ORGate
from src.components.input_button import InputButton


class TestORGate(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.gate = ORGate(
            position=(100, 100),
            size=(120, 80),
            window_size=(800, 600)
        )
        
        # Create mock input buttons
        self.input1 = Mock(spec=InputButton)
        self.input2 = Mock(spec=InputButton)
        
    def test_or_gate_with_no_inputs(self):
        """Test OR gate with no input buttons"""
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_or_gate_with_one_input_false(self):
        """Test OR gate with one input button set to False"""
        self.input1.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_or_gate_with_one_input_true(self):
        """Test OR gate with one input button set to True"""
        self.input1.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_or_gate_with_two_inputs_both_false(self):
        """Test OR gate with two input buttons both False"""
        self.input1.get_state.return_value = False
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_or_gate_with_two_inputs_one_true_one_false(self):
        """Test OR gate with two input buttons - one True, one False"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_or_gate_with_two_inputs_both_true(self):
        """Test OR gate with two input buttons both True"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_or_gate_with_three_inputs_mixed(self):
        """Test OR gate with three input buttons - mixed states"""
        input3 = Mock(spec=InputButton)
        self.input1.get_state.return_value = False
        self.input2.get_state.return_value = False
        input3.get_state.return_value = True
        
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        self.gate.add_input_button(input3)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_or_gate_with_three_inputs_all_false(self):
        """Test OR gate with three input buttons all False"""
        input3 = Mock(spec=InputButton)
        self.input1.get_state.return_value = False
        self.input2.get_state.return_value = False
        input3.get_state.return_value = False
        
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        self.gate.add_input_button(input3)
        
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
    
    def test_duplicate_input_button(self):
        """Test that duplicate input buttons are not added"""
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input1)
        
        # Should only have one instance
        self.assertEqual(len(self.gate.input_buttons), 1)
    
    def test_or_gate_initialization(self):
        """Test OR gate initialization with custom colors"""
        gate = ORGate(
            position=(200, 200),
            size=(150, 100),
            off_color=(100, 100, 100),
            on_color=(255, 150, 150),
            window_size=(1024, 768)
        )
        
        self.assertEqual(gate.position, (200, 200))
        self.assertEqual(gate.size, (150, 100))
        self.assertEqual(gate.off_color, (100, 100, 100))
        self.assertEqual(gate.on_color, (255, 150, 150))
        self.assertEqual(gate.window_size, (1024, 768))
        self.assertEqual(gate.input_buttons, [])
    
    def test_or_gate_with_input_buttons_parameter(self):
        """Test OR gate initialization with input buttons parameter"""
        self.input1.get_state.return_value = True
        gate = ORGate(
            position=(100, 100),
            input_buttons=[self.input1]
        )
        
        self.assertIn(self.input1, gate.input_buttons)
        self.assertTrue(gate.get_result())


if __name__ == '__main__':
    unittest.main() 