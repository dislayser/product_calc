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
    print([container, figures])

    service = CalcService(container, figures)
    print(service)

if __name__ == "__main__":
    main()