from __future__ import annotations
from abc import ABC, abstractmethod

class GridDefinitionTemplate(ABC):
    @property
    @abstractmethod
    def template_number(self) -> int:
        raise NotImplementedError
    @property
    @abstractmethod
    def point_count(self) -> int:
        raise NotImplementedError
    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError
    def validate(self) -> None:
        if self.point_count <= 0:
            raise ValueError("Grid point count must be positive")


class ProductDefinitionTemplate(ABC):
    @property
    @abstractmethod
    def template_number(self) -> int:
        raise NotImplementedError
    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError
    def validate(self) -> None:
        pass

class DataRepresentationTemplate(ABC):
    @property
    @abstractmethod
    def template_number(self) -> int:
        raise NotImplementedError
    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError
