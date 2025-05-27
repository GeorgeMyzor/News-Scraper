from abc import ABC, abstractmethod

class UseCase(ABC):
    @abstractmethod
    async def process_async(self, input: str) -> None:
        pass
