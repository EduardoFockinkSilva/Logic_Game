"""
Gerenciador de conexões visuais entre componentes lógicos.

Este módulo implementa um sistema que automaticamente detecta e cria
conexões visuais entre componentes, gerenciando sua renderização e
atualização baseada no estado dos sinais.
"""

from typing import Dict, List, Tuple, Optional
from src.components.connection_component import ConnectionComponent
from src.components.interfaces import LogicInputSource, RenderableState
from src.components.base_component import Component


class ConnectionManager:
    """
    Gerenciador de conexões visuais entre componentes.
    
    Detecta automaticamente conexões entre componentes e cria
    representações visuais que mudam de cor baseado no estado
    do sinal sendo transmitido.
    
    Attributes:
        connections: Lista de todas as conexões ativas
        component_connections: Mapeamento de componentes para suas conexões
        connection_points: Pontos de conexão de cada componente
    """
    
    def __init__(self, window_size: Tuple[int, int] = (800, 600), shader_manager=None):
        """
        Inicializa o gerenciador de conexões.
        
        Args:
            window_size: Tamanho da janela
            shader_manager: Gerenciador de shaders
        """
        self.connections: List[ConnectionComponent] = []
        self.component_connections: Dict[Component, List[ConnectionComponent]] = {}
        self.connection_points: Dict[Component, Dict[str, Tuple[int, int]]] = {}
        self.window_size = window_size
        self.shader_manager = shader_manager
        
        print("[ConnectionManager] Initialized")
    
    def add_component(self, component: Component):
        """
        Adiciona um componente ao gerenciador de conexões.
        
        Args:
            component: Componente a ser adicionado
        """
        # Definir pontos de conexão baseado no tipo de componente
        self._define_connection_points(component)
        
        # Não criar conexões automáticas - apenas quando explicitamente solicitado
        # self._check_for_connections(component)
        
        print(f"[ConnectionManager] Added component: {component.__class__.__name__}")
    
    def remove_component(self, component: Component):
        """
        Remove um componente e suas conexões.
        
        Args:
            component: Componente a ser removido
        """
        if component in self.component_connections:
            # Remover todas as conexões do componente
            for connection in self.component_connections[component]:
                if connection in self.connections:
                    self.connections.remove(connection)
                    connection.destroy()
            
            del self.component_connections[component]
        
        if component in self.connection_points:
            del self.connection_points[component]
        
        print(f"[ConnectionManager] Removed component: {component.__class__.__name__}")
    
    def _define_connection_points(self, component: Component):
        """
        Define os pontos de conexão de um componente.
        
        Args:
            component: Componente para definir pontos de conexão
        """
        position = component.get_position()
        size = component.get_size()
        
        if not position or not size:
            return
        
        x, y = position
        width, height = size
        
        # Definir pontos de conexão baseado no tipo de componente
        if hasattr(component, 'set_input_source'):  # LEDs - verificar primeiro
            # Para LEDs, adicionar ponto de entrada (lado esquerdo)
            self.connection_points[component] = {
                'input_0': (x, y + height // 2)
            }
            # LEDs não têm saída, apenas entrada
            
        elif hasattr(component, 'get_result'):  # Portas lógicas
            # Ponto de saída (lado direito)
            self.connection_points[component] = {
                'output': (x + width, y + height // 2)
            }
            
            # Para portas lógicas, adicionar pontos de entrada (lado esquerdo)
            if hasattr(component, 'inputs'):
                input_points = {}
                for i in range(len(component.inputs) + 1):  # +1 para permitir novas entradas
                    input_points[f'input_{i}'] = (x, y + height // 2)
                self.connection_points[component].update(input_points)
            else:
                # Se não tem inputs definidos, criar pelo menos um ponto de entrada
                self.connection_points[component]['input_0'] = (x, y + height // 2)
                
        elif hasattr(component, 'get_state'):  # Botões
            # Ponto de saída (lado direito)
            self.connection_points[component] = {
                'output': (x + width, y + height // 2)
            }
    
    def create_connection_for_components(self, source: Component, target: Component):
        """
        Cria uma conexão visual entre dois componentes específicos.
        
        Args:
            source: Componente fonte do sinal
            target: Componente destino do sinal
        """
        # Verificar se ambos os componentes estão registrados
        if source not in self.connection_points or target not in self.connection_points:
            return
        
        source_points = self.connection_points[source]
        target_points = self.connection_points[target]
        
        # Verificar se há pontos compatíveis para conexão
        if 'output' in source_points and any(key.startswith('input_') for key in target_points.keys()):
            # Source tem saída, target tem entrada - conexão direta
            self._create_connection(source, target, source_points['output'], target_points)
        elif 'output' in target_points and any(key.startswith('input_') for key in source_points.keys()):
            # Target tem saída, source tem entrada - conexão invertida
            self._create_connection(target, source, target_points['output'], source_points)
        else:
            # Tentar criar conexão baseada na proximidade
            self._create_connection_if_compatible(source, target)
    
    def _check_for_connections(self, new_component: Component):
        """
        Verifica se o novo componente deve se conectar a outros existentes.
        
        Args:
            new_component: Componente recém-adicionado
        """
        new_points = self.connection_points.get(new_component, {})
        
        # Verificar todos os componentes existentes
        for existing_component, existing_points in self.connection_points.items():
            if existing_component == new_component:
                continue
            
            # Verificar se há pontos compatíveis para conexão
            self._create_connection_if_compatible(new_component, existing_component)
    
    def _create_connection_if_compatible(self, comp1: Component, comp2: Component):
        """
        Cria conexão entre dois componentes se forem compatíveis.
        
        Args:
            comp1: Primeiro componente
            comp2: Segundo componente
        """
        points1 = self.connection_points.get(comp1, {})
        points2 = self.connection_points.get(comp2, {})
        
        # Verificar se comp1 tem saída e comp2 tem entrada
        if 'output' in points1 and any(key.startswith('input_') for key in points2.keys()):
            self._create_connection(comp1, comp2, points1['output'], points2)
        # Verificar se comp2 tem saída e comp1 tem entrada
        elif 'output' in points2 and any(key.startswith('input_') for key in points1.keys()):
            self._create_connection(comp2, comp1, points2['output'], points1)
    
    def _create_connection(self, source: Component, target: Component, 
                          source_point: Tuple[int, int], target_points: Dict[str, Tuple[int, int]]):
        """
        Cria uma conexão entre dois componentes.
        
        Args:
            source: Componente fonte do sinal
            target: Componente destino do sinal
            source_point: Ponto de saída da fonte
            target_points: Pontos de entrada do destino
        """
        # Encontrar ponto de entrada disponível
        target_point = None
        for key, point in target_points.items():
            if key.startswith('input_'):
                target_point = point
                break
        
        if not target_point:
            return
        
        # Criar conexão
        connection = ConnectionComponent(
            start_point=source_point,
            end_point=target_point,
            signal_source=source if hasattr(source, 'get_result') else source,
            off_color=(64, 64, 64),
            on_color=(0, 255, 0),
            line_width=3,
            connection_type='straight',
            window_size=self.window_size,
            shader_manager=self.shader_manager
        )
        
        # Inicializar conexão
        connection.initialize()
        
        # Adicionar à lista de conexões
        self.connections.append(connection)
        
        # Registrar conexão nos componentes
        if source not in self.component_connections:
            self.component_connections[source] = []
        if target not in self.component_connections:
            self.component_connections[target] = []
        
        self.component_connections[source].append(connection)
        self.component_connections[target].append(connection)
        
        print(f"[ConnectionManager] Created connection: {source.__class__.__name__} -> {target.__class__.__name__}")
    
    def update(self, delta_time: float):
        """
        Atualiza todas as conexões.
        
        Args:
            delta_time: Tempo desde o último frame
        """
        for connection in self.connections:
            if connection.enabled:
                connection.update(delta_time)
    
    def render(self, renderer):
        """
        Renderiza todas as conexões.
        
        Args:
            renderer: Renderizador OpenGL
        """
        for connection in self.connections:
            if connection.visible:
                connection.render(renderer)
    
    def clear_all_connections(self):
        """
        Remove todas as conexões.
        """
        for connection in self.connections:
            connection.destroy()
        
        self.connections.clear()
        self.component_connections.clear()
        self.connection_points.clear()
        
        print("[ConnectionManager] Cleared all connections")
    
    def get_connection_count(self) -> int:
        """
        Retorna o número total de conexões.
        
        Returns:
            Número de conexões ativas
        """
        return len(self.connections)
    
    def get_component_connections(self, component: Component) -> List[ConnectionComponent]:
        """
        Retorna todas as conexões de um componente específico.
        
        Args:
            component: Componente para buscar conexões
            
        Returns:
            Lista de conexões do componente
        """
        return self.component_connections.get(component, [])
    
    def update_component_position(self, component: Component):
        """
        Atualiza as posições das conexões quando um componente se move.
        
        Args:
            component: Componente que foi movido
        """
        if component not in self.connection_points:
            return
        
        # Redefinir pontos de conexão
        self._define_connection_points(component)
        
        # Atualizar conexões existentes
        if component in self.component_connections:
            for connection in self.component_connections[component]:
                # Encontrar novos pontos
                new_start = None
                new_end = None
                
                # Determinar qual ponto pertence a este componente
                if connection.start_point in self.connection_points[component].values():
                    new_start = connection.start_point
                if connection.end_point in self.connection_points[component].values():
                    new_end = connection.end_point
                
                # Atualizar conexão se necessário
                if new_start or new_end:
                    current_start = connection.start_point
                    current_end = connection.end_point
                    
                    if new_start:
                        current_start = new_start
                    if new_end:
                        current_end = new_end
                    
                    connection.update_points(current_start, current_end) 