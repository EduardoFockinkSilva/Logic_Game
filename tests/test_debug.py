from unittest.mock import Mock
from src.components.led_component import LEDComponent

# Create LED component
led = LEDComponent(
    position=(100, 100),
    radius=20,
    off_color=(64, 64, 64),
    on_color=(0, 255, 0),
    window_size=(800, 600)
)

# Create mock source
mock_source = Mock()
mock_source.get_result.return_value = False

# Set input source
led.set_input_source(mock_source)

# Test get_state
print(f"LED state: {led.get_state()}")
print(f"Mock source get_result called: {mock_source.get_result.called}")
print(f"Mock source get_result return value: {mock_source.get_result.return_value}")

# Test with True
mock_source.get_result.return_value = True
print(f"LED state after setting True: {led.get_state()}")
print(f"Mock source get_result called: {mock_source.get_result.called}")
print(f"Mock source get_result return value: {mock_source.get_result.return_value}") 