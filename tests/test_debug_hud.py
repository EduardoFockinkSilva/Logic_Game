"""
Testes para o componente DebugHUD
"""

import pytest
import pygame
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from components.debug_hud import DebugHUD
from shaders.shader_manager import ShaderManager


class TestDebugHUD:
    """Testes para o componente DebugHUD."""
    
    def setup_method(self):
        """Configuração para cada teste."""
        pygame.init()
        self.window_size = (800, 600)
        self.shader_manager = ShaderManager()
        self.debug_hud = DebugHUD(
            window_size=self.window_size,
            shader_manager=self.shader_manager
        )
    
    def teardown_method(self):
        """Limpeza após cada teste."""
        if self.debug_hud:
            self.debug_hud.destroy()
        pygame.quit()
    
    def test_initialization(self):
        """Testa se o DebugHUD inicializa corretamente."""
        assert self.debug_hud is not None
        assert self.debug_hud.enabled is True
        assert self.debug_hud.window_size == self.window_size
        assert self.debug_hud.mouse_pos == (0, 0)
        assert self.debug_hud.fps == 0
    
    def test_mouse_position_update(self):
        """Testa se a posição do mouse é atualizada corretamente."""
        # Simular posição do mouse
        test_mouse_pos = (100, 200)
        
        # Atualizar manualmente
        self.debug_hud.mouse_pos = test_mouse_pos
        
        # Verificar se foi atualizado
        assert self.debug_hud.get_mouse_position() == test_mouse_pos
    
    def test_text_components_creation(self):
        """Testa se os componentes de texto são criados."""
        # Inicializar o HUD
        self.debug_hud.initialize()
        
        # Verificar se os componentes de texto foram criados
        assert self.debug_hud.mouse_pos_text is not None
        assert self.debug_hud.fps_text is not None
    
    def test_toggle_functionality(self):
        """Testa se o toggle do HUD funciona."""
        initial_state = self.debug_hud.enabled
        
        # Alternar estado
        self.debug_hud.toggle()
        assert self.debug_hud.enabled == (not initial_state)
        
        # Alternar novamente
        self.debug_hud.toggle()
        assert self.debug_hud.enabled == initial_state
    
    def test_set_enabled(self):
        """Testa se set_enabled funciona."""
        # Testar desabilitar
        self.debug_hud.set_enabled(False)
        assert self.debug_hud.enabled is False
        
        # Testar habilitar
        self.debug_hud.set_enabled(True)
        assert self.debug_hud.enabled is True
    
    def test_fps_calculation(self):
        """Testa se o cálculo de FPS funciona."""
        # Simular algumas atualizações
        delta_time = 0.016  # ~60 FPS
        
        for _ in range(10):
            self.debug_hud._update(delta_time)
        
        # Verificar se o FPS foi calculado
        assert self.debug_hud.get_fps() > 0
    
    def test_mouse_text_update(self):
        """Testa se o texto da posição do mouse é atualizado."""
        # Inicializar o HUD
        self.debug_hud.initialize()
        
        # Simular posição do mouse
        test_pos = (150, 250)
        self.debug_hud.mouse_pos = test_pos
        
        # Atualizar o HUD
        self.debug_hud._update(0.016)
        
        # Verificar se o texto foi atualizado
        expected_text = f"Mouse: ({test_pos[0]}, {test_pos[1]})"
        assert self.debug_hud.mouse_pos_text.text == expected_text


if __name__ == "__main__":
    pytest.main([__file__]) 