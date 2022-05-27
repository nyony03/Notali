from abc import ABC, abstractmethod
# abc = abstract base class


class Observer(ABC):
    @abstractmethod
    def notifier(self, num_note, note_on):
        pass
