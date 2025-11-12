from typing import List, Dict, Tuple, Optional
from entity.container import Container, GuillotineNode
from entity.figure import Figure
import math

class GuillotinePacker:
    def __init__(self, container: Container, figures: List[Figure]):
        self.container = container
        self.figures = figures
        self.placement_log = []
    
    def pack_single_container(self) -> Dict:
        """Упаковывает фигуры в один контейнер с гильотинным алгоритмом"""
        # Сортируем фигуры по убыванию площади
        sorted_figures = sorted(self.figures, key=lambda x: x.area(), reverse=True)
        
        placements = []
        remaining_figures = []
        
        for figure in sorted_figures:
            placed_count = 0
            needed = figure.necessary
            
            while placed_count < needed:
                # Пробуем разместить фигуру
                placement = self._find_best_fit(figure)
                if placement:
                    placements.append(placement)
                    placed_count += 1
                    # Обновляем дерево гильотинных узлов
                    self._split_node(placement['node'], figure)
                else:
                    # Не помещается - пробуем повернутую версию если разрешено
                    if figure.rotation:
                        rotated_figure = figure.rotated()
                        placement = self._find_best_fit(rotated_figure)
                        if placement:
                            placements.append({
                                **placement,
                                'rotated': True
                            })
                            placed_count += 1
                            self._split_node(placement['node'], rotated_figure)
                        else:
                            break
                    else:
                        break
            
            # Записываем сколько не удалось разместить
            if placed_count < needed:
                remaining_figures.append(Figure(
                    figure.width, figure.height, 
                    needed - placed_count,
                    figure.rotation, figure.margin
                ))
        
        # Собираем статистику
        figures_count = self._count_figures(placements)
        used_area = sum(placement['figure'].area() for placement in placements)
        efficiency = used_area / self.container.area
        
        return {
            'placements': placements,
            'figures_count': figures_count,
            'used_area': used_area,
            'efficiency': efficiency,
            'remaining_figures': remaining_figures
        }
    
    def _count_figures(self, placements: List[Dict]) -> Dict[str, int]:
        """Подсчитывает количество каждого типа фигур в размещениях"""
        figures_count = {}
        for placement in placements:
            fig = placement['figure']
            fig_key = f"{fig.width}x{fig.height}"
            figures_count[fig_key] = figures_count.get(fig_key, 0) + 1
        return figures_count
    
    def _find_best_fit(self, figure: Figure) -> Optional[Dict]:
        """Находит лучшую позицию для фигуры используя стратегию Best Area Fit"""
        best_node = None
        best_waste = float('inf')
        
        fig_width, fig_height = figure.size_with_margin()
        
        # Обходим все свободные узлы
        nodes_to_check = [self.container.root]
        while nodes_to_check:
            node = nodes_to_check.pop()
            
            if node.used or node.width < fig_width or node.height < fig_height:
                continue
            
            # Проверяем помещается ли фигура
            if node.width >= fig_width and node.height >= fig_height:
                waste = (node.width * node.height) - (fig_width * fig_height)
                if waste < best_waste:
                    best_waste = waste
                    best_node = node
            
            # Добавляем дочерние узлы для проверки
            if node.right:
                nodes_to_check.append(node.right)
            if node.down:
                nodes_to_check.append(node.down)
        
        if best_node:
            return {
                'figure': figure,
                'x': best_node.x,
                'y': best_node.y,
                'node': best_node,
                'rotated': False
            }
        return None
    
    def _split_node(self, node: GuillotineNode, figure: Figure):
        """Разделяет узел после размещения фигуры"""
        fig_width, fig_height = figure.size_with_margin()
        
        node.used = True
        
        # Определяем как разделять узел (вертикально или горизонтально)
        remaining_width = node.width - fig_width
        remaining_height = node.height - fig_height
        
        # Стратегия: разделяем по большей стороне
        if remaining_width >= remaining_height:
            # Вертикальное разделение
            if remaining_width > 0:
                node.right = GuillotineNode(
                    node.x + fig_width, node.y, 
                    remaining_width, node.height
                )
            if remaining_height > 0:
                node.down = GuillotineNode(
                    node.x, node.y + fig_height,
                    fig_width, remaining_height
                )
        else:
            # Горизонтальное разделение
            if remaining_height > 0:
                node.down = GuillotineNode(
                    node.x, node.y + fig_height,
                    node.width, remaining_height
                )
            if remaining_width > 0:
                node.right = GuillotineNode(
                    node.x + fig_width, node.y,
                    remaining_width, fig_height
                )