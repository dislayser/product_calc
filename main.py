from rich.pretty import pprint as print
from entity.figure import Figure
from entity.container import Container
from service.calc import CalcService

def main() -> None:
    container = Container(width=11, height=8)
    figures = [
        Figure(width=2, height=3, necessary=2000),
        Figure(width=2, height=2, necessary=2000),
        Figure(width=4, height=1, necessary=500 ),
    ]

    # Создаем сервис для расчетов
    service = CalcService(container, figures)
    result = service.calculate_required_containers()
    
    print("=" * 70)
    print("РАСЧЕТ КОНТЕЙНЕРОВ ДЛЯ ИДЕНТИЧНОЙ УПАКОВКИ")
    print("=" * 70)
    
    print(f"Контейнер: {container}")
    print(f"Фигуры для размещения:")
    for fig in figures:
        print(f"  - {fig.width}x{fig.height}: {fig.necessary} шт.")
    
    print(f"ОПТИМАЛЬНАЯ СХЕМА УПАКОВКИ:")
    for fig_key, count in result['optimal_packing_scheme'].items():
        print(f"  - {fig_key}: {count} шт. в каждом контейнере")
    
    print(f"Эффективность использования площади: {result['efficiency_per_container']:.1%}")
    
    print(f"РАСЧЕТ КОЛИЧЕСТВА КОНТЕЙНЕРОВ:")
    for fig_key, analysis in result['figures_analysis'].items():
        print(f"  - {fig_key}: нужно {analysis['necessary']} шт., "
              f"в контейнере {analysis['per_container']} шт. → "
              f"требуется {analysis['containers_needed']} контейнеров")
    
    print(f"ИТОГО: требуется {result['containers_required']} контейнеров")
    
    print(f"ФАКТИЧЕСКОЕ ПРОИЗВОДСТВО:")
    for fig_key, count in result['actual_production'].items():
        print(f"  - {fig_key}: {count} шт.")
    
    print(f"Теоретический минимум контейнеров: {result['theoretical_min_containers']}")

if __name__ == "__main__":
    main()