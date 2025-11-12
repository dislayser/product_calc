from dataclasses import dataclass

@dataclass
class Figure:
    width: int
    height: int
    necessary: int|None = None
    
    def rotated(self) -> 'Figure':
        return Figure(self.height, self.width, self.necessary)
    
    def area(self) -> int:
        return self.width * self.height
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
