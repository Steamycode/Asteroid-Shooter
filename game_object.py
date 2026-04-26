from abc import ABC, abstractmethod

class GameObject(ABC):

    @abstractmethod
    def draw(self, win):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def check_off_screen(self):
        pass
