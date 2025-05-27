from abc import ABC, abstractmethod

class UseCase(ABC):
    """
    Abstract base class for use cases.
    It should be implemented by any concrete use case class.
    """
    @abstractmethod
    async def process_async(self, input: str) -> None:
        pass
