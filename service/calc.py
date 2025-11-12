from entity.container import Container
from entity.figure import Figure
from typing import List, Dict, Tuple
import math

class CalcService:
    def __init__(self, container: Container, figures: List[Figure]):
        self.container = container
        self.figures = figures

    def single_fit(self, figure: Figure, available_area: int) -> Dict:
        """Рассчитывает размещение одной фигуры в контейнере"""
        
        # Оригинальная ориентация
        fit1_w = self.container.width // figure.width
        fit1_h = self.container.height // figure.height
        total_fit1 = fit1_w * fit1_h
        area_fit1 = min(total_fit1, available_area // figure.area())
        
        # Повернутая ориентация
        fit2_w = self.container.width // figure.height
        fit2_h = self.container.height // figure.width
        total_fit2 = fit2_w * fit2_h
        area_fit2 = min(total_fit2, available_area // figure.area())
        
        # Выбираем лучшую ориентацию
        if total_fit1 >= total_fit2:
            best_fit = total_fit1
            best_orientation = 'original'
            best_width_fit = fit1_w
            best_height_fit = fit1_h
        else:
            best_fit = total_fit2
            best_orientation = 'rotated'
            best_width_fit = fit2_w
            best_height_fit = fit2_h
        
        # Ограничиваем по доступной площади
        actual_fit = min(best_fit, available_area // figure.area())
        
        return {
            'figure': figure,
            'original_fit': total_fit1,
            'rotated_fit': total_fit2,
            'best_fit': actual_fit,
            'orientation': best_orientation,
            'width_fit': best_width_fit,
            'height_fit': best_height_fit,
            'area_used': actual_fit * figure.area()
        }

    def calc(self) -> dict:
        return []
