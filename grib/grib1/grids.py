from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

@dataclass(slots=True)
class GridDefinition(ABC):
    nx: int
    ny: int
    def validate(self) -> None:
        if self.nx <= 0:
            raise ValueError("nx must be positive")
        if self.ny <= 0:
            raise ValueError("ny must be positive")
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    @property
    @abstractmethod
    def data_representation_type(self) -> int:
        raise NotImplementedError

@dataclass(slots=True)
class LatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    dy: float = 1.0
    scanning_mode: int = 0
    @property
    def data_representation_type(self) -> int:
        return 0


@dataclass(slots=True)
class MercatorGrid(GridDefinition):
    lat1: float = -80.0
    lon1: float = 0.0
    lat2: float = 80.0
    lon2: float = 359.0
    dx: float = 1.0
    dy: float = 1.0
    latin: float = 6.0
    scanning_mode: int = 0
    @property
    def data_representation_type(self) -> int:
        return 1


@dataclass(slots=True)
class LambertConformalGrid(GridDefinition):
    lat1: float = 20.0
    lon1: float = 220.0
    lov: float = 250.0
    dx: int = 40000
    dy: int = 40000
    latin1: float = 25.0
    latin2: float = 25.0
    scanning_mode: int = 0
    @property
    def data_representation_type(self) -> int:
        return 3


@dataclass(slots=True)
class GaussianLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    gaussian_n: int = 9.1
    scanning_mode: int = 0
    @property
    def data_representation_type(self) -> int:
        return 4

@dataclass(slots=True)
class PolarStereographicGrid(GridDefinition):
    lat1: float = 60.0
    lon1: float = 0.0
    lov: float = 0.0
    dx: int = 60000
    dy: int = 60000
    north_pole: bool = True
    scanning_mode: int = 0
    @property
    def data_representation_type(self) -> int:
        return 5
    
@dataclass(slots=True)
class AlbersEqualAreaGrid(GridDefinition):
    lat1: float = 60.0
    lon1: float = 0.0
    lov: float = 0.0
    dx: int = 60000
    dy: int = 60000
    latin1: float = 25.0
    latin2: float = 25.0
    p_center: bool = True
    scanning_mode: int = 0
    @property
    def data_representation_type(self) -> int:
        return 8

@dataclass(slots=True)
class RotatedLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    dy: float = 1.0
    scanning_mode: int = 0
    rotation_angle: float = 30.0
    @property
    def data_representation_type(self):
        return 10

@dataclass(slots=True)
class RotatedGaussianLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    gaussian_n: int = 9.1
    scanning_mode: int = 0
    rotation_angle: float = 30.0
    @property
    def data_representation_type(self) -> int:
        return 14

@dataclass(slots=True)
class StretchedLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    dy: float = 1.0
    scanning_mode: int = 0
    stretch_factor: float = 2.0
    @property
    def data_representation_type(self):
        return 20
    
@dataclass(slots=True)
class StretchedGaussianLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    gaussian_n: int = 9.1
    scanning_mode: int = 0
    stretch_factor: float = 2.0
    @property
    def data_representation_type(self) -> int:
        return 24

@dataclass(slots=True)
class StretchedRotatedLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    dy: float = 1.0
    scanning_mode: int = 0
    rotation_angle: float = 30.0
    stretch_factor: float = 2.0
    @property
    def data_representation_type(self):
        return 30

@dataclass(slots=True)
class StretchedRotatedGaussianLatLonGrid(GridDefinition):
    lat1: float = -90.0
    lon1: float = 0.0
    lat2: float = 90.0
    lon2: float = 359.0
    dx: float = 1.0
    gaussian_n: int = 9.1
    scanning_mode: int = 0
    rotation_angle: float = 30.0
    stretch_factor: float = 2.0
    @property
    def data_representation_type(self) -> int:
        return 34

@dataclass(slots=True)
class SpaceViewGrid(GridDefinition):
    lat1: float = 0.0
    lon1: float = 0.0
    dx: int = 90
    dy: int = 90
    xp: int = 50   
    yp: int = 50
    scanning_mode: int = 0
    orientationOfTheGrid: int = 0
    nr: int = 1000000
    xo: int = 0
    yo: int = 0
    @property
    def data_representation_type(self) -> int:
        return 90


@dataclass(slots=True)
class TinyGrid(LatLonGrid):
    def __init__(self) -> None:
        super().__init__(
            nx=2,
            ny=2,
            lat1=0.0,
            lon1=0.0,
            lat2=1.0,
            lon2=1.0,
            dx=1.0,
            dy=1.0,
        )

@dataclass(slots=True)
class LargeGrid(LatLonGrid):
    def __init__(self) -> None:
        super().__init__(
            nx=1440,
            ny=721,
            lat1=-90.0,
            lon1=0.0,
            lat2=90.0,
            lon2=359.75,
            dx=0.25,
            dy=0.25,
        )