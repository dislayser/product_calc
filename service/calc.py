from typing import List, Dict, Tuple
from entity.container import Container
from entity.figure import Figure
from dataclasses import dataclass
import math

@dataclass
class Placement:
    figure: Figure
    count: int
    orientation: str
    width_fit: int
    height_fit: int

class CalcService:
    def __init__(self, container: Container, figures: List[Figure]):
        self.container = container
        self.figures = figures
    
    def find_optimal_container_packing(self) -> Dict:
        """
        Находит оптимальное размещение фигур в одном контейнере
        Возвращает схему упаковки и количество каждого типа фигур
        """
        best_scheme = None
        best_efficiency = 0
        best_total_figures = 0
        
        # Генерируем различные комбинации размещения
        schemes = self._generate_packing_schemes()
        
        for scheme in schemes:
            efficiency = self._calculate_scheme_efficiency(scheme)
            total_figures = sum(scheme.values())
            
            # Выбираем схему с лучшей эффективностью и максимальным количеством фигур
            if efficiency > best_efficiency or (efficiency == best_efficiency and total_figures > best_total_figures):
                best_efficiency = efficiency
                best_total_figures = total_figures
                best_scheme = scheme
        
        return {
            'packing_scheme': best_scheme,
            'figures_per_container': best_scheme,
            'efficiency': best_efficiency,
            'total_figures_per_container': best_total_figures
        }
    
    def _generate_packing_schemes(self) -> List[Dict[str, int]]:
        """Генерирует возможные схемы упаковки фигур в контейнер"""
        schemes = []
        
        # Пробуем разные комбинации фигур
        for fig1 in self.figures:
            # Схема с одной фигурой
            scheme_single = self._create_scheme_with_figure(fig1)
            if scheme_single:
                schemes.append(scheme_single)
            
            # Схемы с комбинациями фигур
            for fig2 in self.figures:
                if fig1 != fig2:
                    scheme_double = self._create_scheme_with_two_figures(fig1, fig2)
                    if scheme_double:
                        schemes.append(scheme_double)
        
        return schemes
    
    def _create_scheme_with_figure(self, figure: Figure) -> Dict[str, int]:
        """Создает схему упаковки с одной фигурой"""
        # Пробуем обе ориентации
        count_original = self._calculate_max_fit(figure.width, figure.height)
        count_rotated = self._calculate_max_fit(figure.height, figure.width)
        
        count = max(count_original, count_rotated)
        
        if count > 0:
            return {f"{figure.width}x{figure.height}": count}
        return None
    
    def _create_scheme_with_two_figures(self, fig1: Figure, fig2: Figure) -> Dict[str, int]:
        """Создает схему упаковки с двумя типами фигур"""
        scheme = {}
        
        # Пробуем разные комбинации размещения
        for orientation1 in ['original', 'rotated']:
            for orientation2 in ['original', 'rotated']:
                width1 = fig1.width if orientation1 == 'original' else fig1.height
                height1 = fig1.height if orientation1 == 'original' else fig1.width
                
                width2 = fig2.width if orientation2 == 'original' else fig2.height
                height2 = fig2.height if orientation2 == 'original' else fig2.width
                
                # Пробуем разместить оба типа фигур
                count1, count2 = self._calculate_combined_fit(width1, height1, width2, height2)
                
                if count1 > 0 or count2 > 0:
                    key1 = f"{fig1.width}x{fig1.height}"
                    key2 = f"{fig2.width}x{fig2.height}"
                    
                    current_scheme = {}
                    if count1 > 0:
                        current_scheme[key1] = count1
                    if count2 > 0:
                        current_scheme[key2] = count2
                    
                    # Выбираем схему с максимальным использованием площади
                    current_area = count1 * fig1.area() + count2 * fig2.area()
                    existing_area = sum(scheme.get(k, 0) * Figure(*map(int, k.split('x')), 0).area() 
                                      for k in scheme.keys())
                    
                    if current_area > existing_area:
                        scheme = current_scheme
        
        return scheme if scheme else None
    
    def _calculate_max_fit(self, width: int, height: int) -> int:
        """Рассчитывает максимальное количество фигур, помещающихся в контейнер"""
        return (self.container.width // width) * (self.container.height // height)
    
    def _calculate_combined_fit(self, width1: int, height1: int, width2: int, height2: int) -> Tuple[int, int]:
        """
        Упрощенный расчет комбинированного размещения
        В реальной реализации здесь должен быть более сложный алгоритм
        """
        # Пробуем разместить сначала первый тип, затем второй в оставшемся месте
        count1 = self._calculate_max_fit(width1, height1)
        remaining_area = self.container.area - count1 * width1 * height1
        
        if remaining_area > 0:
            count2 = min(self._calculate_max_fit(width2, height2), 
                        remaining_area // (width2 * height2))
        else:
            count2 = 0
        
        return count1, count2
    
    def _calculate_scheme_efficiency(self, scheme: Dict[str, int]) -> float:
        """Рассчитывает эффективность использования площади для схемы"""
        total_area_used = 0
        for fig_key, count in scheme.items():
            w, h = map(int, fig_key.split('x'))
            total_area_used += count * w * h
        
        return total_area_used / self.container.area
    
    def calculate_required_containers(self) -> Dict:
        """Рассчитывает необходимое количество контейнеров"""
        # Находим оптимальную схему упаковки
        optimal_packing = self.find_optimal_container_packing()
        packing_scheme = optimal_packing['packing_scheme']
        
        # Рассчитываем необходимое количество контейнеров для каждой фигуры
        containers_needed = 0
        figures_placement = {}
        
        for figure in self.figures:
            fig_key = f"{figure.width}x{figure.height}"
            figures_per_container = packing_scheme.get(fig_key, 0)
            
            if figures_per_container > 0:
                containers_for_figure = math.ceil(figure.necessary / figures_per_container)
                containers_needed = max(containers_needed, containers_for_figure)
                
                figures_placement[fig_key] = {
                    'necessary': figure.necessary,
                    'per_container': figures_per_container,
                    'containers_needed': containers_for_figure
                }
        
        # Рассчитываем фактическое количество произведенных фигур
        actual_produced = {}
        for fig_key, info in figures_placement.items():
            actual_produced[fig_key] = packing_scheme.get(fig_key, 0) * containers_needed
        
        return {
            'optimal_packing_scheme': packing_scheme,
            'containers_required': containers_needed,
            'efficiency_per_container': optimal_packing['efficiency'],
            'figures_analysis': figures_placement,
            'actual_production': actual_produced,
            'theoretical_min_containers': math.ceil(
                sum(fig.area() * fig.necessary for fig in self.figures) / self.container.area
            )
        }