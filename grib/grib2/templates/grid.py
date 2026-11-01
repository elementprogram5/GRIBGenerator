from __future__ import annotations
from dataclasses import dataclass
from .base import GridDefinitionTemplate
from grib.utils import (uint1, uint4, sint4, encode_microdegrees)

#LatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate0(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90
    lon1: float = 0
    lat2: float = -90
    lon2: float = 359
    dx: float = 1
    dy: float = 1
    scanning_mode: int = 0
    @property
    def template_number(self) -> int:
        return 0
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
         # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(0x80))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(sint4(encode_microdegrees(self.dx)))
        # Octets 54-57
        data.extend(sint4(encode_microdegrees(self.dy)))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        return bytes(data)
    
#RotatedLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate1(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90
    lon1: float = 0
    lat2: float = -90
    lon2: float = 359
    dx: float = 1
    dy: float = 1
    south_pole_lat: float = -90.0
    south_pole_lon: float = 0.0
    rotation_angle: float = 0.0
    scanning_mode: int = 0
    @property
    def template_number(self) -> int:
        return 1
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
         # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(0x80))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(sint4(encode_microdegrees(self.dx)))
        # Octets 54-57
        data.extend(sint4(encode_microdegrees(self.dy)))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        # Octets 59-62
        data.extend(sint4(encode_microdegrees(self.south_pole_lat)))
        # Octets 63-66
        data.extend(uint4(encode_microdegrees(self.south_pole_lon)))
        # Octets 67-70
        data.extend(sint4(encode_microdegrees(self.rotation_angle)))
        return bytes(data)

#StrechedLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate2(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90
    lon1: float = 0
    lat2: float = -90
    lon2: float = 359
    dx: float = 1
    dy: float = 1
    stretching_pole_lat: float = 90.0
    stretching_pole_lon: float = 0.0
    stretching_factor: float = 1.0
    scanning_mode: int = 0
    @property
    def template_number(self) -> int:
        return 2
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
         # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(0x80))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(sint4(encode_microdegrees(self.dx)))
        # Octets 54-57
        data.extend(sint4(encode_microdegrees(self.dy)))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        # Octets 59-62
        data.extend(sint4(encode_microdegrees(self.stretching_pole_lat)))
        # Octets 63-66
        data.extend(uint4(encode_microdegrees(self.stretching_pole_lon)))
        # Octets 67-70
        data.extend(sint4(encode_microdegrees(self.stretching_factor)))
        return bytes(data)

#StrechedRotatedLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate3(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90
    lon1: float = 0
    lat2: float = -90
    lon2: float = 359
    dx: float = 1
    dy: float = 1
    south_pole_lat: float = -90.0
    south_pole_lon: float = 0.0
    rotation_angle: float = 0.0
    stretching_pole_lat: float = 90.0
    stretching_pole_lon: float = 0.0
    stretching_factor: float = 1.0
    scanning_mode: int = 0
    @property
    def template_number(self) -> int:
        return 3
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
         # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(0x80))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(sint4(encode_microdegrees(self.dx)))
        # Octets 54-57
        data.extend(sint4(encode_microdegrees(self.dy)))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        # Octets 59-62
        data.extend(sint4(encode_microdegrees(self.south_pole_lat)))
        # Octets 63-66
        data.extend(uint4(encode_microdegrees(self.south_pole_lon)))
        # Octets 67-70
        data.extend(sint4(encode_microdegrees(self.rotation_angle)))
        # Octets 71-74
        data.extend(sint4(encode_microdegrees(self.stretching_pole_lat)))
        # Octets 75-78
        data.extend(uint4(encode_microdegrees(self.stretching_pole_lon)))
        # Octets 79-82
        data.extend(sint4(encode_microdegrees(self.stretching_factor)))
        return bytes(data)

#MercatorGrid
@dataclass(slots=True)
class GridDefinitionTemplate10(GridDefinitionTemplate):
    nx : int = 360
    ny : int = 181
    lat1: float = -80.0
    lon1: float = 0.0
    lat2: float = 80.0
    lon2: float = 359.0
    latin: float = 0.0
    dx: int = 100000
    dy: int = 100000
    scanning_mode: int = 0
    orientation: float = 0.0
    @property
    def template_number(self) -> int:
        return 10
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 29-32
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 33
        data.extend(uint1(0x80))
        # Octet 34-37
        data.extend(sint4(encode_microdegrees(self.latin)))
        # Octets 38-41
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octet 46
        data.extend(uint1(self.scanning_mode))
        # Octets 47-50
        data.extend(uint4(encode_microdegrees(self.orientation)))
        # Octets 51-54
        data.extend(uint4(self.dx))
        # Octets 55-58
        data.extend(uint4(self.dy))
        return bytes(data)

#PolarStereographicGrid
@dataclass(slots=True)
class GridDefinitionTemplate20(GridDefinitionTemplate):
    nx: int = 181
    ny: int = 181
    lat1: float = 90.0
    lon1: float = 0.0
    lov: float = 0.0
    lad: float = 60.0 
    dx: int = 100000
    dy: int = 100000
    projection_centre: int = 0
    scanning_mode: int = 0
    resolution_flags: int = 0x80
    @property
    def template_number(self) -> int:
        return 20
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 29-32
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 33
        data.extend(uint1(self.resolution_flags))
        # Octets 34-37
        data.extend(sint4(encode_microdegrees(self.lad)))
        # Octets 38-41
        data.extend(sint4(encode_microdegrees(self.lov)))
        # Octets 42-45
        data.extend(uint4(self.dx))
        # Octets 46-49
        data.extend(uint4(self.dy))
        # Octet 50
        data.extend(uint1(self.projection_centre))
        # Octet 51
        data.extend(uint1(self.scanning_mode))
        return bytes(data)

#LambertConformalGrid
@dataclass(slots=True)
class GridDefinitionTemplate30(GridDefinitionTemplate):
    nx: int = 181
    ny: int = 181
    lat1: float = 30.0
    lon1: float = 240.0
    lov: float = 265.0
    lad: float = 60.0 
    dx: int = 40000
    dy: int = 40000
    projection_center_flag: int = 0
    scanning_mode: int = 0
    resolution_flags: int = 0x80
    latin1: float = 30.0
    latin2: float = 60.0
    south_pole_lat: float = -90.0
    south_pole_lon: float = 0.0
    @property
    def template_number(self) -> int:
        return 30
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 29-32
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 33
        data.extend(uint1(self.resolution_flags))
        # Octets 34-37
        data.extend(sint4(encode_microdegrees(self.lad)))
        # Octets 38-41
        data.extend(sint4(encode_microdegrees(self.lov)))
        # Octets 42-45
        data.extend(uint4(self.dx))
        # Octets 46-49
        data.extend(uint4(self.dy))
        # Octet 50
        data.extend(uint1(self.projection_center_flag))
        # Octet 51
        data.extend(uint1(self.scanning_mode))
        # Octet 52-55
        data.extend(sint4(encode_microdegrees(self.latin1)))
        # Octet 56-59
        data.extend(sint4(encode_microdegrees(self.latin2)))
        # Octets 60-63
        data.extend(sint4(encode_microdegrees(self.south_pole_lat)))
        # Octets 64-67
        data.extend(uint4(encode_microdegrees(self.south_pole_lon)))
        return bytes(data)

#AlbersEqualArea
@dataclass(slots=True)
class GridDefinitionTemplate31(GridDefinitionTemplate):
    nx: int = 181
    ny: int = 181
    lat1: float = 0.0
    lon1: float = 0.0
    lad : float = 0.0
    lov: float = 0.0
    dx: int = 100000
    dy: int = 100000
    projection_centre: int = 0
    scanning_mode: int = 0
    latin1: float = 20.0
    latin2: float = 50.0
    south_pole_lat: float = -90.0
    south_pole_lon: float = 0.0
    resolution_flags: int = 0x30
    @property
    def template_number(self) -> int:
        return 31
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 29-32
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 33
        data.extend(uint1(self.resolution_flags))
        # Octets 34-37
        data.extend(sint4(encode_microdegrees(self.lad)))
        # Octets 38-41
        data.extend(sint4(encode_microdegrees(self.lov)))
        # Octets 42-45
        data.extend(uint4(self.dx))
        # Octets 46-49
        data.extend(uint4(self.dy))
        # Octet 50
        data.extend(uint1(self.projection_centre))
        # Octet 51
        data.extend(uint1(self.scanning_mode))
        # Octet 52-55
        data.extend(sint4(encode_microdegrees(self.latin1)))
        # Octet 56-59
        data.extend(sint4(encode_microdegrees(self.latin2)))
        # Octets 60-63
        data.extend(sint4(encode_microdegrees(self.south_pole_lat)))
        # Octets 64-67
        data.extend(uint4(encode_microdegrees(self.south_pole_lon)))
        return bytes(data)

#GaussianLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate40(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90.0
    lon1: float = 0.0
    lat2: float = -90.0
    lon2: float = 359.0
    gaussian_n: int = 64
    scanning_mode: int = 0
    resolution_flags: int = 0x80
    @property
    def template_number(self) -> int:
        return 40
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(self.resolution_flags))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(uint4(0))
        # Octets 54-57
        data.extend(uint4(self.gaussian_n))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        return bytes(data)
    
#RotatedGaussianLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate41(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90.0
    lon1: float = 0.0
    lat2: float = -90.0
    lon2: float = 359.0
    gaussian_n: int = 64
    south_pole_lat: float = -90.0
    south_pole_lon: float = 0.0
    rotation_angle: float = 0.0
    scanning_mode: int = 0
    resolution_flags: int = 0x80
    @property
    def template_number(self) -> int:
        return 41
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(self.resolution_flags))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(uint4(0))
        # Octets 54-57
        data.extend(uint4(self.gaussian_n))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        # Octets 59-62
        data.extend(sint4(encode_microdegrees(self.south_pole_lat)))
        # Octets 63-66
        data.extend(uint4(encode_microdegrees(self.south_pole_lon)))
        # Octets 67-70
        data.extend(sint4(encode_microdegrees(self.rotation_angle)))
        return bytes(data)

#StretchedGaussianLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate42(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90.0
    lon1: float = 0.0
    lat2: float = -90.0
    lon2: float = 359.0
    gaussian_n: int = 64
    stretching_pole_lat: float = 90.0
    stretching_pole_lon: float = 0.0
    stretching_factor: float = 1.0
    scanning_mode: int = 0
    resolution_flags: int = 0x80
    @property
    def template_number(self) -> int:
        return 42
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(self.resolution_flags))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(uint4(0))
        # Octets 54-57
        data.extend(uint4(self.gaussian_n))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        # Octets 59-62
        data.extend(sint4(encode_microdegrees(self.stretching_pole_lat)))
        # Octets 63-66
        data.extend(uint4(encode_microdegrees(self.stretching_pole_lon)))
        # Octets 67-70
        data.extend(sint4(encode_microdegrees(self.stretching_factor)))
        return bytes(data)
    
#StretchedRotatedGaussianLatLonGrid
@dataclass(slots=True)
class GridDefinitionTemplate43(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
    lat1: float = 90.0
    lon1: float = 0.0
    lat2: float = -90.0
    lon2: float = 359.0
    gaussian_n: int = 64
    south_pole_lat: float = -90.0
    south_pole_lon: float = 0.0
    rotation_angle: float = 0.0
    stretching_pole_lat: float = 90.0
    stretching_pole_lon: float = 0.0
    stretching_factor: float = 1.0
    scanning_mode: int = 0
    resolution_flags: int = 0x80
    @property
    def template_number(self) -> int:
        return 43
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(uint4(0))
        # Octets 29-32
        data.extend(uint4(0))
        # Octets 33-36
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 37-40
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 41
        data.extend(uint1(self.resolution_flags))
        # Octets 42-45
        data.extend(sint4(encode_microdegrees(self.lat2)))
        # Octets 46-49
        data.extend(sint4(encode_microdegrees(self.lon2)))
        # Octets 50-53
        data.extend(uint4(0))
        # Octets 54-57
        data.extend(uint4(self.gaussian_n))
        # Octet 58
        data.extend(uint1(self.scanning_mode))
        # Octets 59-62
        data.extend(sint4(encode_microdegrees(self.south_pole_lat)))
        # Octets 63-66
        data.extend(uint4(encode_microdegrees(self.south_pole_lon)))
        # Octets 67-70
        data.extend(sint4(encode_microdegrees(self.rotation_angle)))
        # Octets 71-74
        data.extend(sint4(encode_microdegrees(self.stretching_pole_lat)))
        # Octets 75-78
        data.extend(uint4(encode_microdegrees(self.stretching_pole_lon)))
        # Octets 79-82
        data.extend(sint4(encode_microdegrees(self.stretching_factor)))
        return bytes(data)
    
@dataclass(slots=True)
class GridDefinitionTemplate90(GridDefinitionTemplate):
    nx: int = 360
    ny: int = 181
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
    def template_number(self) -> int:
        return 90
    @property
    def point_count(self) -> int:
        return self.nx * self.ny
    def encode(self) -> bytes:
        data = bytearray()
        # Octet 1
        data.extend(uint1(6))
        # Octet 2
        data.extend(uint1(0))
        # Octets 3-6
        data.extend(uint4(6367470))
        # Octet 7
        data.extend(uint1(0))
        # Octets 8-11
        data.extend(uint4(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-16
        data.extend(uint4(0))
        # Octets 17-20
        data.extend(uint4(self.nx))
        # Octets 21-24
        data.extend(uint4(self.ny))
        # Octets 25-28
        data.extend(sint4(encode_microdegrees(self.lat1)))
        # Octets 29-32
        data.extend(sint4(encode_microdegrees(self.lon1)))
        # Octet 33
        data.extend(uint1(0x80))
        # Octets 34-37
        data.extend(uint4(self.dx))
        # Octets 38-41
        data.extend(uint4(self.dy))
        # Octets 42-45
        data.extend(uint4(self.xp))
        # Octets 46-49
        data.extend(uint4(self.yp))
        # Octet 50
        data.extend(uint1(self.scanning_mode))
        # Octets 51-54
        data.extend(sint4(self.orientationOfTheGrid))
        # Octets 55-58
        data.extend(uint4(self.nr))
        # Octets 59-62
        data.extend(uint4(self.xo))
        # Octets 63-66
        data.extend(uint4(self.yo))
        return bytes(data)
