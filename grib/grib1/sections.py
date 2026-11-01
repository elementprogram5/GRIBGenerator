from __future__ import annotations
from grib.utils import (BitWriter, uint1, uint2, uint3, sint2, sint3, encode_millidegrees, ibm_float) 
from grib.grib1.message import (Bitmap, ProductDefinition)
from grib.grib1.grids import (GridDefinition, LatLonGrid, MercatorGrid, PolarStereographicGrid, LambertConformalGrid, GaussianLatLonGrid, AlbersEqualAreaGrid, RotatedLatLonGrid, RotatedGaussianLatLonGrid, StretchedLatLonGrid, StretchedGaussianLatLonGrid, StretchedRotatedLatLonGrid, StretchedRotatedGaussianLatLonGrid, SpaceViewGrid)
from grib.packing import (PackedData, SimplePackedData, ComplexPackedData)
from dataclasses import dataclass
from abc import ABC
from abc import abstractmethod
import math

class Section(ABC):
    @property
    @abstractmethod
    def length(self) -> int:
        raise NotImplementedError
    @abstractmethod
    def encode(self) -> bytes:
        raise NotImplementedError

@dataclass(slots=True)
class IndicatorSection(Section):
    total_length: int
    @property
    def length(self) -> int:
        return 8
    def encode(self) -> bytes:
        return (b"GRIB" + uint3(self.total_length) + uint1(1))

@dataclass(slots=True)
class ProductDefinitionSection(Section):
    product: ProductDefinition
    has_gds: bool
    has_bms: bool
    @property
    def length(self) -> int:
        return 28
    def _flags(self) -> int:
        flags = 0
        if self.has_gds:
            flags |= 0x80
        if self.has_bms:
            flags |= 0x40
        return flags
    def encode(self) -> bytes:
        self.product.validate()
        p = self.product
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(p.table_version))
        # Octet 5
        data.extend(uint1(p.center_id))
        # Octet 6
        data.extend(uint1(p.generating_process_id))
        # Octet 7
        data.extend(uint1(p.grid_id))
        # Octet 8
        data.extend(uint1(self._flags()))
        # Octet 9
        data.extend(uint1(p.parameter_id))
        # Octet 10
        data.extend(uint1(p.level_type))
        # Octets 11-12
        data.extend(uint2(p.level_value))
        # Octets 13-17
        data.extend(uint1(p.year))
        data.extend(uint1(p.month))
        data.extend(uint1(p.day))
        data.extend(uint1(p.hour))
        data.extend(uint1(p.minute))
        # Octet 18
        data.extend(uint1(p.forecast_time_unit))
        # Octets 19-20
        data.extend(uint1(p.p1))
        data.extend(uint1(p.p2))
        # Octet 21
        data.extend(uint1(p.time_range_indicator))
        # Octets 22-23
        data.extend(uint2(p.number_in_average))
        # Octet 24
        data.extend(uint1(p.number_missing))
        # Octet 25
        data.extend(uint1(p.century))
        # Octet 26
        data.extend(uint1(p.subcenter_id))
        # Octets 27-28
        data.extend(p.decimal_scale_factor.to_bytes(2, "big", signed=True))
        return bytes(data)

@dataclass(slots=True)
class GridDescriptionSection(Section):
    grid: GridDefinition
    @property
    def length(self) -> int:
        if isinstance(self.grid, LatLonGrid):
            return 32
        if isinstance(self.grid, MercatorGrid):
            return 42
        if isinstance(self.grid, PolarStereographicGrid):
            return 42
        if isinstance(self.grid, LambertConformalGrid):
            return 42
        if isinstance(self.grid, GaussianLatLonGrid):
            return 42
        if isinstance(self.grid, AlbersEqualAreaGrid):
            return 42
        if isinstance(self.grid, RotatedLatLonGrid):
            return 42
        if isinstance(self.grid, RotatedGaussianLatLonGrid):
            return 42
        if isinstance(self.grid, StretchedLatLonGrid):
            return 42
        if isinstance(self.grid, StretchedGaussianLatLonGrid):
            return 42
        if isinstance(self.grid, StretchedRotatedLatLonGrid):
            return 52
        if isinstance(self.grid, StretchedRotatedGaussianLatLonGrid):
            return 52
        if isinstance(self.grid, SpaceViewGrid):
            return 44
        raise NotImplementedError(f"Unsupported grid type: " f"{type(self.grid).__name__}")
    def encode(self) -> bytes:
        if isinstance(self.grid, LatLonGrid):
            return self._encode_latlon()
        if isinstance(self.grid, MercatorGrid):
            return self._encode_mercator()
        if isinstance(self.grid, PolarStereographicGrid):
            return self._encode_polar_stereographic()
        if isinstance(self.grid, LambertConformalGrid):
            return self._encode_lambert_conformal()
        if isinstance(self.grid, GaussianLatLonGrid):
            return self._encode_gaussian_latlon()
        if isinstance(self.grid, AlbersEqualAreaGrid):
            return self._encode_albers_equalarea()
        if isinstance(self.grid, RotatedLatLonGrid):
            return self._encode_rotated_latlon()
        if isinstance(self.grid, RotatedGaussianLatLonGrid):
            return self._encode_rotated_gaussian_latlon()
        if isinstance(self.grid, StretchedLatLonGrid):
            return self._encode_stretched_latlon()
        if isinstance(self.grid, StretchedGaussianLatLonGrid):
            return self._encode_stretched_gaussian_latlon()
        if isinstance(self.grid, StretchedRotatedLatLonGrid):
            return self._encode_stretched_rotated_latlon()
        if isinstance(self.grid, StretchedRotatedGaussianLatLonGrid):
            return self._encode_stretched_rotated_gaussian_latlon()
        if isinstance(self.grid, SpaceViewGrid):
            return self._encode_spaceview()
        raise NotImplementedError(f"Unsupported grid type: " f"{type(self.grid).__name__}")
    def _encode_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, LatLonGrid)
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.dy)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        # Octets 29-32
        data.extend(
            b"\x00\x00\x00\x00"
        )
        return bytes(data)
    def _encode_mercator(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, MercatorGrid)
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octet 24-26
        data.extend(sint3(encode_millidegrees(grid.latin)))
        # Octet 27
        data.extend(uint1(grid.scanning_mode))
        # Octets 28-30
        data.extend(uint3(100000))
        # Octets 31-33
        data.extend(uint3(100000))
        # Octets 34-36
        data.extend(uint3(0))
        # Octets 37-42
        data.extend(b"\x00\x00\x00\x00\x00\x00")
        return bytes(data)
    def _encode_polar_stereographic(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, PolarStereographicGrid)
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
         # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(uint3(encode_millidegrees(grid.lov)))
        # Octets 21-23
        data.extend(uint3(grid.dx))
        # Octets 24-26
        data.extend(uint3(grid.dy))
        # Octet 27
        projection_flag = (0
            if grid.north_pole
            else 128)
        data.extend(uint1(projection_flag))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 42:
            data.append(0)
        return bytes(data)
    def _encode_lambert_conformal(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, LambertConformalGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
         # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(uint3(encode_millidegrees(grid.lov)))
        # Octets 21-23
        data.extend(uint3(grid.dx))
        # Octets 24-26
        data.extend(uint3(grid.dy))
        # Octet 27
        projection_flag = 0
        data.extend(uint1(projection_flag))
        # Octets 28-30
        data.extend(sint3(encode_millidegrees(grid.latin1)))
        # Octets 31-33
        data.extend(sint3(encode_millidegrees(grid.latin2)))
        #South Pole Coords 
        data.extend(uint3(0))
        data.extend(uint3(0))
        while len(data) < 42:
            data.append(0)
        return bytes(data)
    def _encode_gaussian_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid,GaussianLatLonGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.gaussian_n)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 42:
            data.append(0)
        return bytes(data)
    def _encode_albers_equalarea(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, AlbersEqualAreaGrid)
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(uint3(encode_millidegrees(grid.lov)))
        # Octets 21-23
        data.extend(uint3(grid.dx))
        # Octets 24-26
        data.extend(uint3(grid.dy))
        # Octet 27
        projection_flag = 0
        data.extend(uint1(projection_flag))
        # Octets 28-30
        data.extend(sint3(encode_millidegrees(grid.latin1)))
        # Octets 31-33
        data.extend(sint3(encode_millidegrees(grid.latin2)))
        #South Pole Coords 
        data.extend(uint3(0))
        data.extend(uint3(0))
        while len(data) < 42:
            data.append(0)
        return bytes(data)
    def _encode_rotated_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, RotatedLatLonGrid)
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.dy)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 32:
            data.append(0)
        # Octets 33-35
        data.extend(uint3(0))
        # Octets 36-38
        data.extend(uint3(0))
        # Octets 39-42
        data.extend(ibm_float(grid.rotation_angle))
        return bytes(data)
    def _encode_rotated_gaussian_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, RotatedGaussianLatLonGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.gaussian_n)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 32:
            data.append(0)
        # Octets 33-35
        data.extend(uint3(0))
        # Octets 36-38
        data.extend(uint3(0))
        # Octets 39-42
        data.extend(ibm_float(grid.rotation_angle))
        return bytes(data)
    def _encode_stretched_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, StretchedLatLonGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.dy)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 32:
            data.append(0)
        # Octets 33-35
        data.extend(uint3(0))
        # Octets 36-38
        data.extend(uint3(0))
        # Octets 39-42
        data.extend(ibm_float(grid.stretch_factor))
        return bytes(data)
    def _encode_stretched_gaussian_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, StretchedGaussianLatLonGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.gaussian_n)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 32:
            data.append(0)
        # Octets 33-35
        data.extend(uint3(0))
        # Octets 36-38
        data.extend(uint3(0))
        # Octets 39-42
        data.extend(ibm_float(grid.stretch_factor))
        return bytes(data)
    def _encode_stretched_rotated_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, StretchedRotatedLatLonGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.dy)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 32:
            data.append(0)
        # Octets 33-35
        data.extend(uint3(0))
        # Octets 36-38
        data.extend(uint3(0))
        # Octets 39-42
        data.extend(ibm_float(grid.rotation_angle))
        # Octets 43-45
        data.extend(uint3(0))
        # Octets 46-48
        data.extend(uint3(0))
        # Octets 49-52
        data.extend(ibm_float(grid.stretch_factor))
        return bytes(data)
    def _encode_stretched_rotated_gaussian_latlon(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, StretchedRotatedGaussianLatLonGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(sint3(encode_millidegrees(grid.lat2)))
        # Octets 21-23
        data.extend(uint3(encode_millidegrees(grid.lon2)))
        # Octets 24-25
        data.extend(uint2(encode_millidegrees(grid.dx)))
        # Octets 26-27
        data.extend(uint2(encode_millidegrees(grid.gaussian_n)))
        # Octet 28
        data.extend(uint1(grid.scanning_mode))
        while len(data) < 32:
            data.append(0)
        # Octets 33-35
        data.extend(uint3(0))
        # Octets 36-38
        data.extend(uint3(0))
        # Octets 39-42
        data.extend(ibm_float(grid.rotation_angle))
        # Octets 43-45
        data.extend(uint3(0))
        # Octets 46-48
        data.extend(uint3(0))
        # Octets 49-52
        data.extend(ibm_float(grid.stretch_factor))
        return bytes(data)
    def _encode_spaceview(self) -> bytes:
        grid = self.grid
        assert isinstance(grid, SpaceViewGrid)
        data = bytearray()
         # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octet 5
        data.extend(uint1(255))
        # Octet 6
        data.extend(uint1(grid.data_representation_type))
        # Octets 7-8
        data.extend(uint2(grid.nx))
        # Octets 9-10
        data.extend(uint2(grid.ny))
        # Octets 11-13
        data.extend(sint3(encode_millidegrees(grid.lat1)))
        # Octets 14-16
        data.extend(uint3(encode_millidegrees(grid.lon1)))
        # Octet 17
        data.extend(uint1(0x80))
        # Octets 18-20
        data.extend(uint3(grid.dx))
        # Octets 21-23
        data.extend(uint3(grid.dy))
        # Octets 24-26
        data.extend(uint3(grid.xo))
        # Octets 27-29
        data.extend(uint3(grid.xp))
        while len(data) < 44:
            data.append(0)
        return bytes(data)

@dataclass(slots=True)
class BitmapSection(Section):
    bitmap: Bitmap
    @property
    def length(self) -> int:
        bitmap_bytes = math.ceil(len(self.bitmap.bits) / 8)
        return 6 + bitmap_bytes
    def encode(self) -> bytes:
        data = bytearray()
        data.extend(uint3(self.length))
        unused_bits = (8 - (len(self.bitmap.bits) % 8)) % 8
        data.extend(uint1(unused_bits))
        data.extend(uint2(0))
        writer = BitWriter()
        for bit in self.bitmap.bits:
            writer.write(
                1 if bit else 0,
                1,
            )
        data.extend(writer.finish())
        return bytes(data)

@dataclass(slots=True)
class BinaryDataSection(Section):
    packed: PackedData
    @property
    def length(self) -> int:
        if isinstance(self.packed, SimplePackedData):
            return 11 + len(self.packed.data)
        if isinstance(self.packed, ComplexPackedData):
            return len(self._encode_complex())            
        raise TypeError(f"Unsupported packed data type: {type(self.packed).__name__}")
    def encode(self) -> bytes:
        if isinstance(self.packed, SimplePackedData):
            return self._encode_simple()
        if isinstance(self.packed, ComplexPackedData):
            return self._encode_complex()
        raise TypeError(f"Unsupported packed data type: {type(self.packed).__name__}")
    def _encode_simple(self) -> bytes:
        data = bytearray()
        # Octets 1-3
        data.extend(uint3(self.length))
        # Octet 4
        data.extend(uint1(0))
        # Octets 5-6
        data.extend(sint2(self.packed.binary_scale_factor))
        # Octets 7-10
        data.extend(ibm_float(self.packed.reference_value))
        # Octet 11
        data.extend(uint1(self.packed.bits_per_value))
        # Octets 12+
        data.extend(self.packed.data)
        return bytes(data)
    def _encode_complex(self) -> bytes:
        data = bytearray()
        # Octets 1-3: 
        data.extend(uint3(0))   
        # Octet 4: BDS Flags
        bds_flags = 0x60
        data.extend(uint1(bds_flags))
        # Octets 5-6: 
        data.extend(sint2(self.packed.binary_scale_factor))
        # Octets 7-10
        data.extend(ibm_float(self.packed.reference_value))
        # Octet 11
        data.extend(uint1(self.packed.bits_per_value))
        # Octets 12-13: N1 - Byte offset of First-Order values (placeholder)
        data.extend(uint2(0))
        # Octet 14: Extended Flags
        extended_flags = 0x30
        data.extend(uint1(extended_flags))
        # Octets 15-16: N2 - Byte offset of Second-Order data (placeholder)
        data.extend(uint2(0))
        # Octets 17-18
        data.extend(uint2(self.packed.number_of_first_order))
        # Octets 19-20
        data.extend(uint2(self.packed.number_of_second_order))
        # Octet 21: Reserved
        data.extend(uint1(0))
        # Octet 22 onwards: Width Array (W2j) -> 1 byte per group
        for w in self.packed.group_widths:
            data.extend(uint1(w))
        # Directly following the width array is the secondary bitmap
        data.extend(self.packed.secondary_bitmap)
        # --- Calculate and set N1 pointer ---
        # N1 points right here (1-based index equivalent to current length + 1)
        # Since Python index/length is 0-based, data length *is* the 1-based byte offset
        n1_pointer = len(data) + 1
        # Append First-Order Data
        data.extend(self.packed.first_order_data)
        # --- Calculate and set N2 pointer ---
        n2_pointer = len(data) + 1
        # Append Second-Order Data
        data.extend(self.packed.second_order_data)
        # --- Post-processing: Inject offsets and section length ---
        # Total length of this BDS section
        total_length = len(data)
        # Inject Section Length (Octets 1-3)
        data[0:3] = uint3(total_length)   
        # Inject N1 Pointer (Octets 12-13)
        data[11:13] = uint2(n1_pointer)   
        # Inject N2 Pointer (Octets 15-16)
        data[14:16] = uint2(n2_pointer)   
        return bytes(data)

@dataclass(slots=True)
class EndSection(Section):
    @property
    def length(self) -> int:
        return 4
    def encode(self) -> bytes:
        return b"7777"
