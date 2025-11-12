from typing import List, Dict
from entity.container import Container
from entity.figure import Figure
from service.guillotine_packer import GuillotinePacker
import math

class IndustrialCalcService:
    def __init__(self, container: Container, figures: List[Figure]):
        self.container = container
        self.figures = figures
    
    def calculate_production_plan(self) -> Dict:
        """Рассчитывает производственный план с гильотинной упаковкой"""
        
        # Шаг 1: Находим оптимальную упаковку для одного листа
        packer = GuillotinePacker(self.container, self.figures)
        single_sheet_result = packer.pack_single_container()
        
        # Шаг 2: Анализируем сколько каких фигур помещается на один лист
        figures_per_sheet = single_sheet_result['figures_count']
        
        # Шаг 3: Рассчитываем необходимое количество листов
        sheets_required = 0
        production_plan = {}
        
        for figure in self.figures:
            fig_key = f"{figure.width}x{figure.height}"
            per_sheet = figures_per_sheet.get(fig_key, 0)
            
            if per_sheet > 0:
                sheets_for_figure = math.ceil(figure.necessary / per_sheet)
                sheets_required = max(sheets_required, sheets_for_figure)
                
                production_plan[fig_key] = {
                    'necessary': figure.necessary,
                    'per_sheet': per_sheet,
                    'sheets_needed': sheets_for_figure,
                    'total_produced': per_sheet * sheets_required
                }
            else:
                # Если фигура не помещается на лист
                production_plan[fig_key] = {
                    'necessary': figure.necessary,
                    'per_sheet': 0,
                    'sheets_needed': float('inf'),
                    'total_produced': 0,
                    'error': 'Не помещается на лист'
                }
        
        # Если какие-то фигуры не помещаются, используем максимальное количество листов
        if sheets_required == 0:
            sheets_required = 1  # Минимум один лист
        
        # Шаг 4: Расчет эффективности и отходов
        total_material_area = self.container.area * sheets_required
        total_used_area = single_sheet_result['used_area'] * sheets_required
        efficiency = total_used_area / total_material_area if total_material_area > 0 else 0
        
        return {
            'production_plan': production_plan,
            'sheets_required': sheets_required,
            'single_sheet_layout': single_sheet_result,
            'efficiency': efficiency,
            'waste_area': total_material_area - total_used_area,
            'layout_coordinates': single_sheet_result['placements']  # Для визуализации
        }
    
    def generate_cutting_plan(self) -> Dict:
        """Генерирует план раскроя для производства"""
        production_plan = self.calculate_production_plan()
        
        cutting_plan = {
            'container_specs': {
                'width': self.container.width,
                'height': self.container.height,
                'margin': self.container.margin
            },
            'sheets_required': production_plan['sheets_required'],
            'cutting_instructions': []
        }
        
        # Создаем инструкции для каждого листа
        for placement in production_plan['single_sheet_layout']['placements']:
            fig = placement['figure']
            instruction = {
                'figure': f"{fig.width}x{fig.height}",
                'x': placement['x'],
                'y': placement['y'],
                'width': fig.width + fig.margin * 2,
                'height': fig.height + fig.margin * 2,
                'rotated': placement.get('rotated', False),
                'margin': fig.margin
            }
            cutting_plan['cutting_instructions'].append(instruction)
        
        return cutting_plan
    
    def get_detailed_report(self) -> Dict:
        """Возвращает детальный отчет о раскрое"""
        production_plan = self.calculate_production_plan()
        
        return {
            'container': {
                'width': self.container.width,
                'height': self.container.height,
                'area': self.container.area,
                'margin': self.container.margin
            },
            'figures': [
                {
                    'width': fig.width,
                    'height': fig.height,
                    'necessary': fig.necessary,
                    'margin': fig.margin,
                    'area': fig.area()
                }
                for fig in self.figures
            ],
            'production_summary': production_plan,
            'cutting_plan': self.generate_cutting_plan()
        }