from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Container:
    width: int
    height: int

    def area(self) -> int:
        return self.width * self.height
