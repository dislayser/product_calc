from dataclasses import dataclass
from typing import Tuple

@dataclass
class Figure:
    width: int
    height: int
    necessary: int
    rotation: bool = True  # Можно ли вращать
    margin: int = 0  # Отступы для технологических нужд
    
    def rotated(self) -> 'Figure':
        return Figure(self.height, self.width, self.necessary, self.rotation, self.margin)
    
    def area(self) -> int:
        return (self.width + self.margin * 2) * (self.height + self.margin * 2)
    
    def size_with_margin(self) -> Tuple[int, int]:
        return (self.width + self.margin * 2, self.height + self.margin * 2)
    
    def __str__(self) -> str:
        return f"Figure({self.width}x{self.height}, need: {self.necessary}, margin: {self.margin})"