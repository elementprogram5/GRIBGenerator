from dataclasses import dataclass
from abc import ABC, abstractmethod
import math
from grib.utils import (BitWriter, uint1, uint2, uint4, uint8) 
from grib.grib2.templates import (GridDefinitionTemplate, ProductDefinitionTemplate, DataRepresentationTemplate)
from grib.grib2.message import (Bitmap, Identification)
from grib.packing import PackedData

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
    discipline: int
    total_length: int
    @property
    def length(self) -> int:
        return 16
    def encode(self) -> bytes:
        data = bytearray()
        # Octets 1-4
        data.extend(b"GRIB")
        # Octets 5-6
        data.extend(b"\x00\x00")
        # Octet 7
        data.extend(uint1(self.discipline))
        # Octet 8
        data.extend(uint1(2))
        # Octets 9-16
        data.extend(uint8(self.total_length))
        return bytes(data)

@dataclass(slots=True)
class IdentificationSection(Section):
    identification: Identification
    @property
    def length(self) -> int:
        return 21
    def encode(self) -> bytes:
        i = self.identification
        i.validate()
        data = bytearray()
        # Octets 1-4
        data.extend(uint4(self.length))
        # Octet 5
        data.extend(uint1(1))
        # Octets 6-7
        data.extend(uint2(i.centre))
        # Octets 8-9
        data.extend(uint2(i.subcentre))
        # Octet 10
        data.extend(uint1(i.master_table_version))
        # Octet 11
        data.extend(uint1(i.local_table_version))
        # Octet 12
        data.extend(uint1(i.significance_of_reference_time))
        # Octets 13-14
        data.extend(uint2(i.year))
        # Octet 15
        data.extend(uint1(i.month))
        # Octet 16
        data.extend(uint1(i.day))
        # Octet 17
        data.extend(uint1(i.hour))
        # Octet 18
        data.extend(uint1(i.minute))
        # Octet 19
        data.extend(uint1(i.second))
        # Octet 20
        data.extend(uint1(i.production_status))
        # Octet 21
        data.extend(uint1(i.type_of_processed_data))
        return bytes(data)

@dataclass(slots=True)
class LocalUseSection(Section):
    data: bytes
    @property
    def length(self) -> int:
        return 5 + len(self.data)
    def encode(self) -> bytes:
        out = bytearray()
        # Octets 1-4
        out.extend(uint4(self.length))
        # Octet 5
        out.extend(uint1(2))
        # local use
        out.extend(self.data)
        return bytes(out)

@dataclass(slots=True)
class GridDefinitionSection(Section):
    grid_template: GridDefinitionTemplate
    source_of_grid_definition: int = 0
    number_of_points: int | None = None
    @property
    def length(self) -> int:
        return 14 + len(self.grid_template.encode())
    def encode(self) -> bytes:
        template = self.grid_template
        template.validate()
        template_data = template.encode()
        if self.number_of_points is None:
            points = template.point_count
        else:
            points = self.number_of_points
        data = bytearray()
        # Octets 1-4
        data.extend(uint4(self.length))
        # Octet 5
        data.extend(uint1(3))
        # Octet 6
        data.extend(uint1(self.source_of_grid_definition))
        # Octets 7-10
        data.extend(uint4(points))
        # Octet 11
        data.extend(uint1(0))
        # Octet 12
        data.extend(uint1(0))
        # Octets 13-14
        data.extend(uint2(template.template_number))
        # Template data
        data.extend(template_data)
        return bytes(data)

@dataclass(slots=True)
class ProductDefinitionSection(Section):
    template: ProductDefinitionTemplate
    @property
    def length(self) -> int:
        return 9 + len(self.template.encode())
    def encode(self) -> bytes:
        data = bytearray()
        # Octets 1-4
        data.extend(uint4(self.length))
        # Octet 5
        data.extend(uint1(4))
        # Octets 6-7
        data.extend(uint2(0))
        # Octets 8-9
        data.extend(uint2(self.template.template_number))
        # Template data
        data.extend(self.template.encode())
        return bytes(data)

@dataclass(slots=True)
class DataRepresentationSection(Section):
    number_of_points: int
    template: DataRepresentationTemplate
    @property
    def length(self) -> int:
        return 11 + len(self.template.encode())
    def encode(self) -> bytes:
        data = bytearray()
        # Octets 1-4
        data.extend(uint4(self.length))
        # Octet 5
        data.extend(uint1(5))
        # Octets 6-9
        data.extend(uint4(self.number_of_points))
        # Octets 10-11
        data.extend(uint2(self.template.template_number))
        # Template data
        data.extend(self.template.encode())
        return bytes(data)

@dataclass(slots=True)
class BitmapSection(Section):
    bitmap: Bitmap | None = None
    @property
    def length(self) -> int:
        if self.bitmap is None:
            return 6
        bitmap_bytes = math.ceil(len(self.bitmap.bits) / 8)
        return 6 + bitmap_bytes
    def encode(self) -> bytes:
        data = bytearray()
        # Octets 1-4
        data.extend(uint4(self.length))
        # Octet 5
        data.extend(uint1(6))
        # Octet 6
        if self.bitmap is None:
            data.extend(uint1(255))
            return bytes(data)
        data.extend(uint1(0))
        writer = BitWriter()
        for bit in self.bitmap.bits:
            writer.write(1 if bit else 0, 1)
        # Bitmap
        data.extend(writer.finish())
        return bytes(data)

@dataclass(slots=True)
class DataSection(Section):
    packed: PackedData
    @property
    def length(self) -> int:
        return 5 + len(self.packed.data)
    def encode(self) -> bytes:
        data = bytearray()
        # Octets 1-4
        data.extend(uint4(self.length))
        # Octet 5
        data.extend(uint1(7))
        # Octets 6+
        data.extend(self.packed.data)
        return bytes(data)

@dataclass(slots=True)
class EndSection:
    @property
    def length(self) -> int:
        return 4
    def encode(self) -> bytes:
        return b"7777"