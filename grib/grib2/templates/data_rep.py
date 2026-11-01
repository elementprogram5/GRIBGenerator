from __future__ import annotations
from dataclasses import dataclass
from .base import DataRepresentationTemplate
from grib.utils import (uint1, sint2, ieee_float)
@dataclass(slots=True)

class DataRepresentationTemplate0(DataRepresentationTemplate):
    reference_value: float
    binary_scale_factor: int
    decimal_scale_factor: int
    bits_per_value: int
    @property
    def template_number(self) -> int:
        return 0
    def encode(self) -> bytes:
        data = bytearray()
        # Octets 1-4
        data.extend(ieee_float(self.reference_value))
        # Octets 5-6
        data.extend(sint2(self.binary_scale_factor))
        # Octets 7-8
        data.extend(sint2(self.decimal_scale_factor))
        # Octet 9
        data.extend(uint1(self.bits_per_value))
        # Octet 10
        data.extend(uint1(0))
        return bytes(data)
