"""
Gerenciador de shaders OpenGL
"""

import os
from typing import Dict, Optional
from OpenGL.GL import *
from OpenGL.GLU import *


class ShaderManager:
    """Gerenciador de shaders OpenGL - carrega, compila e gerencia shaders"""
    
    def __init__(self):
        """Inicializa gerenciador de shaders"""
        self.shaders: Dict[str, int] = {}
        self.programs: Dict[str, int] = {}
    
    def load_shader(self, name: str, vertex_path: str, fragment_path: str) -> int:
        """Carrega e compila programa de shader"""
        # Verificar se já foi carregado
        if name in self.programs:
            program_id = self.programs[name]
            if program_id is not None:
                return program_id
        
        # Ler arquivos de shader
        vertex_source = self._read_shader_file(vertex_path)
        fragment_source = self._read_shader_file(fragment_path)
        
        # Compilar shaders
        vertex_shader = self._compile_shader(GL_VERTEX_SHADER, vertex_source)
        fragment_shader = self._compile_shader(GL_FRAGMENT_SHADER, fragment_source)
        
        # Criar programa
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        
        # Verificar se linkou corretamente
        if not glGetProgramiv(program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(program)
            raise RuntimeError(f"Erro ao linkar shader '{name}': {error}")
        
        # Limpar shaders
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        
        # Armazenar programa
        self.programs[name] = program
        return program
    
    def has_program(self, name: str) -> bool:
        """Verifica se programa de shader existe"""
        return name in self.programs
    
    def _read_shader_file(self, filepath: str) -> str:
        """Lê conteúdo de arquivo de shader"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de shader não encontrado: {filepath}")
    
    def _compile_shader(self, shader_type: int, source: str) -> int:
        """Compila shader individual"""
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        
        # Verificar se compilou corretamente
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader)
            raise RuntimeError(f"Erro ao compilar shader: {error}")
        
        return shader
    
    def use_program(self, name: str) -> None:
        """Ativa programa de shader"""
        if name in self.programs:
            program_id = self.programs[name]
            if program_id is not None:
                glUseProgram(program_id)
            else:
                raise ValueError(f"Programa de shader '{name}' é inválido")
        else:
            raise ValueError(f"Programa de shader '{name}' não encontrado")
    
    def get_program(self, name: str) -> Optional[int]:
        """Obtém ID de programa de shader"""
        return self.programs.get(name)
    
    def set_uniform_1f(self, name: str, value: float) -> None:
        """Define uniform float"""
        current_program = glGetInteger(GL_CURRENT_PROGRAM)
        if current_program is not None:
            location = glGetUniformLocation(current_program, name)
            if location != -1:
                glUniform1f(location, value)
    
    def set_uniform_2f(self, name: str, x: float, y: float) -> None:
        """Define uniform vec2"""
        current_program = glGetInteger(GL_CURRENT_PROGRAM)
        if current_program is not None:
            location = glGetUniformLocation(current_program, name)
            if location != -1:
                glUniform2f(location, x, y)
    
    def set_uniform_3f(self, name: str, x: float, y: float, z: float) -> None:
        """Define uniform vec3"""
        current_program = glGetInteger(GL_CURRENT_PROGRAM)
        if current_program is not None:
            location = glGetUniformLocation(current_program, name)
            if location != -1:
                glUniform3f(location, x, y, z)
    
    def set_uniform_4f(self, name: str, x: float, y: float, z: float, w: float) -> None:
        """Define uniform vec4"""
        current_program = glGetInteger(GL_CURRENT_PROGRAM)
        if current_program is not None:
            location = glGetUniformLocation(current_program, name)
            if location != -1:
                glUniform4f(location, x, y, z, w)
    
    def cleanup(self) -> None:
        """Limpa todos os shaders e programas"""
        for program in self.programs.values():
            if program is not None:
                glDeleteProgram(program)
        self.programs.clear() 