from __future__ import annotations
from dataclasses import dataclass
from grib.grib2.templates import (GridDefinitionTemplate, ProductDefinitionTemplate)

@dataclass(slots=True)
class Bitmap:
    bits: list[bool]

@dataclass(slots=True)
class Identification:
    centre: int = 7
    subcentre: int = 0
    master_table_version: int = 2
    local_table_version: int = 0
    significance_of_reference_time: int = 1
    year: int = 2025
    month: int = 1
    day: int = 1
    hour: int = 0
    minute: int = 0
    second: int = 0
    production_status: int = 0
    type_of_processed_data: int = 1
    def validate(self) -> None:
        if not 0 <= self.centre <= 0xFFFF:
            raise ValueError("centre out of range")
        if not 0 <= self.subcentre <= 0xFFFF:
            raise ValueError("subcentre out of range")
        if not 0 <= self.master_table_version <= 0xFF:
            raise ValueError("master_table_version out of range")
        if not 0 <= self.local_table_version <= 0xFF:
            raise ValueError("local_table_version out of range")

@dataclass(slots=True)
class Grib2Message:
    discipline: int
    identification: Identification
    grid: GridDefinitionTemplate
    product: ProductDefinitionTemplate
    values: list[float]
    bitmap: Bitmap | None = None
    local_use: bytes | None = None
    @property
    def has_bitmap(self) -> bool:
        return self.bitmap is not None
    def validate(self) -> None:
        if not 0 <= self.centre <= 0xFFFF:
            raise ValueError("centre out of range")
        if not 0 <= self.subcentre <= 0xFFFF:
            raise ValueError("subcentre out of range")
        if not 0 <= self.master_table_version <= 0xFF:
            raise ValueError("master_table_version out of range")
        if not 0 <= self.local_table_version <= 0xFF:
            raise ValueError("local_table_version out of range")
        if not 0 <= self.significance_of_reference_time <= 0xFF:
            raise ValueError("significance_of_reference_time out of range")
        if not 0 <= self.year <= 0xFFFF:
            raise ValueError("year out of range")
        if not 1 <= self.month <= 12:
            raise ValueError("month out of range")
        if not 1 <= self.day <= 31:
            raise ValueError("day out of range")
        if not 0 <= self.hour <= 23:
            raise ValueError("hour out of range")
        if not 0 <= self.minute <= 59:
            raise ValueError("minute out of range")
        if not 0 <= self.second <= 59:
            raise ValueError("second out of range")
        if not 0 <= self.production_status <= 0xFF:
            raise ValueError("production_status out of range")
        if not 0 <= self.type_of_processed_data <= 0xFF:
            raise ValueError("type_of_processed_data out of range")
