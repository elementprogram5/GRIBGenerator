from __future__ import annotations
from dataclasses import dataclass
from grib.grib1.grids import GridDefinition

@dataclass(slots=True)
class Bitmap:
    bits: list[bool]

@dataclass(slots=True)
class ProductDefinition:
    table_version: int = 3
    center_id: int = 7
    generating_process_id: int = 255
    grid_id: int = 255
    parameter_id: int = 11
    level_type: int = 100
    level_value: int = 500
    year: int = 25
    month: int = 1
    day: int = 1
    hour: int = 0
    minute: int = 0
    forecast_time_unit: int = 1
    p1: int = 0
    p2: int = 0
    time_range_indicator: int = 0
    number_in_average: int = 0
    number_missing: int = 0
    century: int = 21
    subcenter_id: int = 0
    decimal_scale_factor: int = 0
    def validate(self) -> None:
        if not 0 <= self.parameter_id <= 255:
            raise ValueError("parameter_id out of range")
        if not 0 <= self.level_type <= 255:
            raise ValueError("level_type out of range")
        if not 0 <= self.level_value <= 65535:
            raise ValueError("level_value out of range")
    
@dataclass(slots=True)
class Grib1Message:
    product: ProductDefinition
    grid: GridDefinition
    values: list[float]
    bitmap: Bitmap | None = None
    @property
    def has_bitmap(self) -> bool:
        return self.bitmap is not None
    def validate(self) -> None:
        self.product.validate()
        self.grid.validate()
        if len(self.values) != self.grid.point_count:
            raise ValueError(
                f"Expected {self.grid.point_count} values "
                f"but got {len(self.values)}"
        )