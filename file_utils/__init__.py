from typing import Type

from django.conf import settings

from file_utils.aws import AwsFileService
from file_utils.base import FileServiceInterface


__all__ = ["file_service"]


class FileServiceRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, klass: Type[FileServiceInterface]):
        cls._registry.setdefault(name, klass())

    @classmethod
    def get_service(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError(f"FileService {name} not registered.")


FileServiceRegistry.register("aws", AwsFileService)


class FileService:
    def __init__(self, service=None):
        self.service = service or self._get_file_service()

    @staticmethod
    def _get_file_service():
        service_name = settings.FILE_SERVICE
        return FileServiceRegistry.get_service(service_name)

    def get_file_url(self, filename):
        self.service.get_file_url(filename)


file_service = FileService()
