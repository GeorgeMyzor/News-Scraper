from abc import ABC, abstractmethod

class UseCase(ABC):
    @abstractmethod
    def process(self, input: str) -> None:
        pass
