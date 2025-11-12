from dataclasses import dataclass
from typing import Dict

@dataclass
class Container:
    width: int
    height: int
    
    def __post_init__(self):
        self.area = self.width * self.height
    
    def __str__(self) -> str:
        return f"Container({self.width}x{self.height}, area: {self.area})"
    
    def __repr__(self) -> str:
        return self.__str__()