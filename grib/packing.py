from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from grib.utils import BitWriter, _bit_width_nonneg

@dataclass(slots=True)
class PackedData(ABC):
    reference_value: float
    binary_scale_factor: int

@dataclass(slots=True)
class SimplePackedData(PackedData):
    decimal_scale_factor: int = 0
    bits_per_value: int = 0
    data: bytes = b""

@dataclass(slots=True)
class ComplexPackedData(PackedData):
    reference_value: float
    binary_scale_factor: int
    decimal_scale_factor: int
    bits_per_value: int                  
    number_of_first_order: int           
    number_of_second_order: int          
    group_widths: list[int]             
    secondary_bitmap: bytes             
    first_order_data: bytes             
    second_order_data: bytes             
    spatial_differencing: bool = False
    @property
    def group_count(self) -> int:
        return self.number_of_first_order

class PackingStrategy(ABC):
    @abstractmethod
    def pack(self, values: list[float], bitmap: list[bool] | None = None) -> PackedData:
        raise NotImplementedError
    
class SimplePacking(PackingStrategy):
    def pack(self, values: list[float], bitmap: list[bool] | None = None) -> SimplePackedData:
        if bitmap is not None:
            values = [value
                for value, present in zip(values, bitmap)
                if present]
        if not values:
            raise ValueError("cannot pack empty value list")
        reference_value = min(values)
        scaled_values = [int(round(v - reference_value))
            for v in values]
        maximum = max(scaled_values)
        bits_per_value = max(1, maximum.bit_length())
        writer = BitWriter()
        for value in scaled_values:
            writer.write(value, bits_per_value)
        return SimplePackedData(reference_value=reference_value, 
            binary_scale_factor=0, 
            bits_per_value=bits_per_value, 
            data=writer.finish()
        )

class ComplexPacking(PackingStrategy):
    def __init__(self, group_size: int = 32):
        if group_size <= 0:
            raise ValueError("group_size must be positive")
        self.group_size = group_size
    def pack(self, values: list[float], 
             bitmap: list[bool] | None = None,
             decimal_scale: int = 0,
             binary_scale: int = 0,
             spatial_differencing: bool = False) -> ComplexPackedData:
        if bitmap is not None:
            values = [value for value, present in zip(values, bitmap) if present]
        if not values:
            raise ValueError("Cannot pack empty value list")
        P2 = len(values)
        reference_value = min(values)
        scale_factor = (10 ** decimal_scale) / (2 ** binary_scale)
        ints = [int(round((v - reference_value) * scale_factor)) for v in values]
        # Chunk into groups
        groups = [ints[i:i + self.group_size] for i in range(0, len(ints), self.group_size)]
        P1 = len(groups)  
        first_order_values: list[int] = []
        group_widths: list[int] = []
        residuals_by_group: list[list[int]] = []
        for g in groups:
            fo = min(g)
            first_order_values.append(fo)
            residuals = [x - fo for x in g]
            residuals_by_group.append(residuals)
            w2 = max((_bit_width_nonneg(r) for r in residuals), default=0)
            group_widths.append(w2)
        max_first = max(first_order_values) if first_order_values else 0
        W1 = max(1, _bit_width_nonneg(max_first)) 
        sec_writer = BitWriter()
        for g_idx, residuals in enumerate(residuals_by_group):
            for i in range(len(residuals)):
                # 1 at the start of a group (where a new first-order value applies)
                sec_writer.write(1 if i == 0 else 0, 1)
        secondary_bitmap = sec_writer.finish()
        first_writer = BitWriter()
        for fo in first_order_values:
            first_writer.write(fo, W1)
        first_order_bytes = first_writer.finish()
        second_writer = BitWriter()
        for w, residuals in zip(group_widths, residuals_by_group):
            if w == 0:
                continue
            for r in residuals:
                second_writer.write(r, w)
        second_order_bytes = second_writer.finish()
        return ComplexPackedData(
            reference_value=reference_value,
            binary_scale_factor=binary_scale,
            decimal_scale_factor=decimal_scale,
            bits_per_value=W1,                
            number_of_first_order=P1,         
            number_of_second_order=P2,        
            group_widths=group_widths,        
            secondary_bitmap=secondary_bitmap,
            first_order_data=first_order_bytes,
            second_order_data=second_order_bytes,
            spatial_differencing=spatial_differencing
        )