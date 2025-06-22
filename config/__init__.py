"""
Módulo de configurações do jogo de Puzzle Lógico
"""

from .settings import (
    WindowConfig,
    Paths,
    PerformanceConfig,
    DebugConfig,
    GameplayConfig,
    ShaderConfig,
    TestConfig,
    AudioConfig,
    get_window_size,
    get_default_colors,
    get_component_defaults,
    get_shader_paths,
    get_level_paths
)
from .style import Colors, ComponentStyle

__all__ = [
    'WindowConfig',
    'Colors',
    'ComponentStyle',
    'Paths',
    'PerformanceConfig',
    'DebugConfig',
    'GameplayConfig',
    'ShaderConfig',
    'TestConfig',
    'AudioConfig',
    'get_window_size',
    'get_default_colors',
    'get_component_defaults',
    'get_shader_paths',
    'get_level_paths'
] 