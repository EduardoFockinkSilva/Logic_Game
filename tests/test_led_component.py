"""
Testes para o componente LED - Testes unitários simples
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Adicionar o diretório src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from components.led_component import LEDComponent


class TestLEDComponent(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.led = LEDComponent(
            position=(100, 100),
            radius=20,
            off_color=(64, 64, 64),
            on_color=(0, 255, 0),
            window_size=(800, 600)
        )
    
    def test_led_creation(self):
        """Testa se o LED é criado corretamente."""
        self.assertEqual(self.led.position, (100, 100))
        self.assertEqual(self.led.radius, 20)
        self.assertEqual(self.led.off_color, (64, 64, 64))
        self.assertEqual(self.led.on_color, (0, 255, 0))
        self.assertEqual(self.led.window_size, (800, 600))
        self.assertIsNone(self.led.input_source)
    
    def test_led_state_without_input_source(self):
        """Testa o estado do LED quando não há fonte de entrada."""
        self.assertFalse(self.led.get_state())
    
    def test_led_state_with_mock_input_source(self):
        """Testa o estado do LED com uma fonte de entrada simulada."""
        # Mock input source with get_result method
        mock_source = Mock()
        mock_source.get_result.return_value = True
        
        self.led.set_input_source(mock_source)
        self.assertTrue(self.led.get_state())
        
        # Test with get_result method
        mock_source.get_result.return_value = False
        self.assertFalse(self.led.get_state())
    
    def test_led_state_with_get_state_method(self):
        """Testa o estado do LED com fonte que usa get_state."""
        # Mock input source with get_state method
        mock_source = Mock()
        mock_source.get_state.return_value = True
        # Remove get_result if it exists
        if hasattr(mock_source, 'get_result'):
            delattr(mock_source, 'get_result')
        
        self.led.set_input_source(mock_source)
        self.assertTrue(self.led.get_state())
        
        # Test with get_state method
        mock_source.get_state.return_value = False
        self.assertFalse(self.led.get_state())
    
    def test_led_state_with_invalid_source(self):
        """Testa o estado do LED com fonte inválida."""
        # Mock input source without get_result or get_state methods
        mock_source = Mock()
        # Remove any methods that might exist
        if hasattr(mock_source, 'get_result'):
            delattr(mock_source, 'get_result')
        if hasattr(mock_source, 'get_state'):
            delattr(mock_source, 'get_state')
        
        self.led.set_input_source(mock_source)
        self.assertFalse(self.led.get_state())
    
    def test_led_color_selection(self):
        """Testa a seleção de cor baseada no estado."""
        # Test off state
        mock_source = Mock()
        mock_source.get_result.return_value = False
        self.led.set_input_source(mock_source)
        self.assertFalse(self.led.get_state())
        
        # Test on state
        mock_source.get_result.return_value = True
        self.assertTrue(self.led.get_state())


if __name__ == '__main__':
    unittest.main() 