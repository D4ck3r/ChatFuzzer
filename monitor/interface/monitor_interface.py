from abc import ABC, abstractmethod

class MonitorInterface(ABC):
    @abstractmethod
    def check_login(self):
        pass
    @abstractmethod
    def restruct_session(self):
        pass
    @abstractmethod
    def extract_session(self):
        pass                                                                            