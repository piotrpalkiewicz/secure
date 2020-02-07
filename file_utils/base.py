from abc import ABCMeta, abstractmethod


class FileServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_file_url(self, filename: str) -> str:
        pass
