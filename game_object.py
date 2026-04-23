from abc import ABC, abstractmethod

class GameObject(ABC):

    @abstractmethod
    def draw(self, win):
        pass
