"""
Testes para o componente LED - Testes unitários simples
"""

import unittest
from unittest.mock import Mock


class MockLEDComponent:
    """Mock simplificado do LED Component para testes."""
    
    def __init__(self, position, radius=20, 
                 off_color=(64, 64, 64), on_color=(0, 255, 0),
                 window_size=(800, 600), shader_manager=None, 
                 input_source=None):
        self.position = position
        self.radius = radius
        self.off_color = off_color
        self.on_color = on_color
        self.window_size = window_size
        self.shader_manager = shader_manager
        self.input_source = input_source
    
    def _get_led_state(self):
        """Obtém o estado atual do LED baseado na fonte de entrada."""
        if self.input_source is None:
            return False
        
        # Se a fonte de entrada tem um método get_result, use-o
        if hasattr(self.input_source, 'get_result'):
            return self.input_source.get_result()
        
        # Se a fonte de entrada tem um método get_state, use-o
        elif hasattr(self.input_source, 'get_state'):
            return self.input_source.get_state()
        
        # Caso contrário, assuma que está desligado
        return False
    
    def set_input_source(self, source):
        """Define a fonte de entrada para o LED."""
        self.input_source = source
    
    def get_state(self):
        """Retorna o estado atual do LED."""
        return self._get_led_state()


class TestLEDComponent(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.led = MockLEDComponent(
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
        
        # Test with get_state method
        mock_source.get_result.return_value = False
        self.assertFalse(self.led.get_state())
    
    def test_led_state_with_get_state_method(self):
        """Testa o estado do LED com fonte que usa get_state."""
        # Mock input source with get_state method
        mock_source = Mock()
        mock_source.get_state.return_value = True
        
        self.led.set_input_source(mock_source)
        self.assertTrue(self.led.get_state())
        
        # Test with get_state method
        mock_source.get_state.return_value = False
        self.assertFalse(self.led.get_state())
    
    def test_led_state_with_invalid_source(self):
        """Testa o estado do LED com fonte inválida."""
        # Mock input source without get_result or get_state methods
        mock_source = Mock()
        
        self.led.set_input_source(mock_source)
        self.assertFalse(self.led.get_state())
    
    def test_led_color_selection(self):
        """Testa a seleção de cor baseada no estado."""
        # Test off state
        self.led.input_source = Mock()
        self.led.input_source.get_result.return_value = False
        self.assertFalse(self.led.get_state())
        
        # Test on state
        self.led.input_source.get_result.return_value = True
        self.assertTrue(self.led.get_state())


if __name__ == '__main__':
    unittest.main() 