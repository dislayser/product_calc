from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class GuillotineNode:
    x: int
    y: int
    width: int
    height: int
    used: bool = False
    right: 'GuillotineNode' = None
    down: 'GuillotineNode' = None

class Container:
    def __init__(self, width: int, height: int, margin: int = 0):
        self.width = width
        self.height = height
        self.margin = margin  # Технологические отступы по краям
        self.area = width * height
        self.root = GuillotineNode(margin, margin, width - 2*margin, height - 2*margin)
    
    def __str__(self) -> str:
        return f"Container({self.width}x{self.height}, margin: {self.margin})"