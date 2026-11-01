from __future__ import annotations
from grib.grib2.message import Grib2Message
from grib.packing import (PackingStrategy, PackedData, SimplePackedData)
from grib.grib2.templates import (DataRepresentationTemplate, DataRepresentationTemplate50)
from grib.grib2.sections import (
    IndicatorSection,
    IdentificationSection,
    LocalUseSection,
    GridDefinitionSection,
    ProductDefinitionSection,
    DataRepresentationSection,
    BitmapSection,
    DataSection,
    EndSection
)

class Grib2Encoder:
    def __init__(self, packing: PackingStrategy) -> None:
        self.packing = packing
    def _make_representation_template(self, packed: PackedData) -> DataRepresentationTemplate:
        if isinstance(packed, SimplePackedData):
            return DataRepresentationTemplate50(packed.reference_value, packed.binary_scale_factor, packed.decimal_scale_factor, packed.bits_per_value)
        raise TypeError(f"Unsupported packed data type: {type(packed).__name__}")
    def encode(self, message: Grib2Message) -> bytes:
        message.validate()
        bitmap_bits = (message.bitmap.bits if message.bitmap is not None else None)
        packed = self.packing.pack(message.values,bitmap_bits)
        section1 = IdentificationSection(message.identification).encode()
        if message.local_use is not None:
            section2 = LocalUseSection(message.local_use).encode()
        else:
            section2 = b""
        section3 = GridDefinitionSection(message.grid).encode()
        section4 = ProductDefinitionSection(message.product).encode()
        template = self._make_representation_template(packed)
        section5 = DataRepresentationSection(number_of_points=message.grid.point_count, template=template).encode()
        section6 = BitmapSection(message.bitmap).encode()
        section7 = DataSection(packed).encode()
        end = EndSection().encode()
        total_length = (
            16
            + len(section1)
            + len(section2)
            + len(section3)
            + len(section4)
            + len(section5)
            + len(section6)
            + len(section7)
            + len(end)
        )
        indicator = IndicatorSection(discipline=message.discipline,total_length=total_length).encode()
        encoded = (
            indicator
            + section1
            + section2
            + section3
            + section4
            + section5
            + section6
            + section7
            + end
        )
        return encoded
