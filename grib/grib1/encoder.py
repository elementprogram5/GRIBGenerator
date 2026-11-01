from __future__ import annotations
from grib.grib1.message import Grib1Message
from grib.packing import PackingStrategy
from grib.grib1.sections import (IndicatorSection, ProductDefinitionSection, GridDescriptionSection, BitmapSection, BinaryDataSection, EndSection,)

class Grib1Encoder:
    def __init__(self, packing: PackingStrategy) -> None:
        self.packing = packing
    def encode(self, message: Grib1Message) -> bytes:
        message.validate()
        if (message.bitmap is not None and len(message.bitmap.bits) != len(message.values)):
            raise ValueError("Bitmap size must match value count")
        pds = ProductDefinitionSection(product=message.product, 
                                       has_gds=True, 
                                       has_bms=message.has_bitmap).encode()
        gds =  GridDescriptionSection(message.grid).encode()
        if message.bitmap is not None:
            bms = BitmapSection(message.bitmap).encode()
        else:
            bms = b""
        bitmap_bits = (message.bitmap.bits if message.bitmap is not None else None)
        packed = self.packing.pack(message.values, bitmap_bits)
        bds = BinaryDataSection(packed).encode()
        total_length = (8 + len(pds) + len(gds) + len(bms) + len(bds) + 4)
        indicator = IndicatorSection(total_length).encode()
        end = EndSection().encode()
        encoded = indicator + pds + gds + bms + bds + end
        print("Indicator", len(indicator))
        print("PDS", len(pds))
        print("GDS", len(gds))
        print("BMS", len(bms))
        print("BDS", len(bds))
        for i, b in enumerate(bds[:32], start=1):
            print(f"{i:2d}: {b:02X}")
        print("END", len(end))
        print("TOTAL", total_length)
        print("Actual", len(encoded))
        return encoded