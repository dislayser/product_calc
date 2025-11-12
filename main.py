from rich.pretty import pprint as print
from rich.table import Table
from rich.console import Console
from entity.figure import Figure
from entity.container import Container
from service.industrial_calc import IndustrialCalcService

def main() -> None:
    console = Console()
    
    # Промышленные параметры (например, стандартный лист 594x841 - A1)
    container = Container(width=594, height=841, margin=5)  # 5mm технологические отступы
    
    # Изделия для производства
    figures = [
        Figure(width=40, height=40, necessary=200, margin=2),   # Отступ 2mm вокруг
        Figure(width=80, height=40, necessary=100, margin=2),
        Figure(width=60, height=60, necessary=50, margin=3),
    ]

    service = IndustrialCalcService(container, figures)
    result = service.calculate_production_plan()
    cutting_plan = service.generate_cutting_plan()
    
    console.print("\n🎯 [bold cyan]ПРОМЫШЛЕННЫЙ РАСЧЕТ РАСКРОЯ[/bold cyan]")
    console.print("=" * 70)
    
    # Информация о материалах
    table = Table(title="📋 Спецификация материалов")
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="white")
    
    table.add_row("Размер листа", f"{container.width} x {container.height} mm")
    table.add_row("Технологические отступы", f"{container.margin} mm")
    table.add_row("Полезная площадь", f"{container.area} mm²")
    table.add_row("Требуется листов", f"{result['sheets_required']} шт.")
    table.add_row("Эффективность раскроя", f"{result['efficiency']:.1%}")
    table.add_row("Отходы", f"{result['waste_area']:.0f} mm²")
    
    console.print(table)
    
    # План производства
    table = Table(title="🏭 План производства")
    table.add_column("Изделие", style="cyan")
    table.add_column("Нужно", style="white")
    table.add_column("На лист", style="green")
    table.add_column("Листов", style="yellow")
    table.add_column("Будет произведено", style="magenta")
    
    for fig_key, plan in result['production_plan'].items():
        table.add_row(
            fig_key,
            str(plan['necessary']),
            str(plan['per_sheet']),
            str(plan['sheets_needed']),
            str(plan['total_produced'])
        )
    
    console.print(table)
    
    # Координаты раскроя (для первого листа)
    console.print("\n📐 [bold]Координаты раскроя (первый лист):[/bold]")
    for placement in result['single_sheet_layout']['placements'][:10]:  # Покажем первые 10
        fig = placement['figure']
        console.print(
            f"  {fig.width}x{fig.height} "
            f"@ ({placement['x']}, {placement['y']}) "
            f"{'🔄' if placement.get('rotated') else ''}"
        )

if __name__ == "__main__":
    main()