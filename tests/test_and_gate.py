"""
Testes para componente porta AND
"""

import unittest
from unittest.mock import Mock
from src.components.and_gate import ANDGate
from src.components.input_button import InputButton


class TestANDGate(unittest.TestCase):
    def setUp(self):
        """Configura fixtures de teste"""
        self.gate = ANDGate(
            position=(100, 100),
            size=(120, 80),
            window_size=(800, 600)
        )
        
        # Criar botões de entrada mock
        self.input1 = Mock(spec=InputButton)
        self.input2 = Mock(spec=InputButton)
        
    def test_and_gate_with_no_inputs(self):
        """Testa porta AND sem botões de entrada"""
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_one_input_false(self):
        """Testa porta AND com uma entrada False"""
        self.input1.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_one_input_true(self):
        """Testa porta AND com uma entrada True"""
        self.input1.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_and_gate_with_two_inputs_both_false(self):
        """Testa porta AND com duas entradas False"""
        self.input1.get_state.return_value = False
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_two_inputs_one_true_one_false(self):
        """Testa porta AND com duas entradas - uma True, uma False"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = False
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertFalse(result)
    
    def test_and_gate_with_two_inputs_both_true(self):
        """Testa porta AND com duas entradas True"""
        self.input1.get_state.return_value = True
        self.input2.get_state.return_value = True
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input2)
        
        result = self.gate.get_result()
        self.assertTrue(result)
    
    def test_add_and_remove_input_button(self):
        """Testa adicionar e remover botões de entrada"""
        self.input1.get_state.return_value = True
        
        # Adicionar botão
        self.gate.add_input_button(self.input1)
        self.assertIn(self.input1, self.gate.input_buttons)
        
        # Remover botão
        self.gate.remove_input_button(self.input1)
        self.assertNotIn(self.input1, self.gate.input_buttons)
    
    def test_duplicate_input_button(self):
        """Testa que botões duplicados não são adicionados"""
        self.gate.add_input_button(self.input1)
        self.gate.add_input_button(self.input1)
        
        # Deve ter apenas uma instância
        self.assertEqual(len(self.gate.input_buttons), 1)


if __name__ == '__main__':
    unittest.main() 