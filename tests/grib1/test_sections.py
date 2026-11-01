import pytest

from grib.grib1.sections import (
    IndicatorSection,
    ProductDefinitionSection,
    GridDescriptionSection,
    BitmapSection,
    BinaryDataSection,
    EndSection,
)

from grib.grib1.message import ProductDefinition, Bitmap

from grib.grib1.grids import (
    LatLonGrid,
    MercatorGrid,
    PolarStereographicGrid,
    LambertConformalGrid,
    GaussianLatLonGrid,
)

from grib.packing import (
    SimplePackedData,
    ComplexPackedData,
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def make_product():
    return ProductDefinition(
        table_version=2,
        center_id=7,
        generating_process_id=255,
        grid_id=255,
        parameter_id=11,
        level_type=100,
        level_value=500,
        year=25,
        month=1,
        day=1,
        hour=0,
        minute=0,
        forecast_time_unit=1,
        p1=0,
        p2=0,
        time_range_indicator=0,
        number_in_average=0,
        number_missing=0,
        century=21,
        subcenter_id=0,
        decimal_scale_factor=0,
    )


# ---------------------------------------------------------------------
# Indicator Section
# ---------------------------------------------------------------------

def test_indicator_section():
    section = IndicatorSection(total_length=1234)

    encoded = section.encode()

    assert section.length == 8
    assert len(encoded) == 8
    assert encoded == (
        b"GRIB"
        + b"\x00\x04\xd2"
        + b"\x01"
    )


# ---------------------------------------------------------------------
# Product Definition Section
# ---------------------------------------------------------------------

def test_product_definition_flags():
    section = ProductDefinitionSection(
        product=make_product(),
        has_gds=True,
        has_bms=False,
    )

    assert section._flags() == 0x80


def test_product_definition_encode():
    section = ProductDefinitionSection(
        product=make_product(),
        has_gds=True,
        has_bms=False,
    )

    encoded = section.encode()

    assert section.length == 28
    assert len(encoded) == 28
    assert int.from_bytes(encoded[:3], "big") == 28


# ---------------------------------------------------------------------
# Grid Description Section
# ---------------------------------------------------------------------

@pytest.mark.parametrize(
    "grid,expected_length",
    [
        (LatLonGrid(5, 5), 32),
        (MercatorGrid(5, 5), 42),
        (PolarStereographicGrid(5, 5), 42),
        (LambertConformalGrid(5, 5), 42),
        (GaussianLatLonGrid(5, 5), 42),
    ],
)
def test_grid_description_section(grid, expected_length):
    section = GridDescriptionSection(grid)

    encoded = section.encode()

    assert section.length == expected_length
    assert len(encoded) == expected_length
    assert int.from_bytes(encoded[:3], "big") == expected_length


# ---------------------------------------------------------------------
# Bitmap Section
# ---------------------------------------------------------------------

def test_bitmap_section():
    bitmap = Bitmap(
        bits=[True, False, True, False, True]
    )

    section = BitmapSection(bitmap)

    encoded = section.encode()

    assert len(encoded) == section.length
    assert int.from_bytes(encoded[:3], "big") == section.length


# ---------------------------------------------------------------------
# Simple Binary Data Section
# ---------------------------------------------------------------------

def test_simple_binary_data_section():
    packed = SimplePackedData(
        reference_value=0.0,
        binary_scale_factor=0,
        bits_per_value=8,
        data=b"\x01\x02\x03\x04",
    )

    section = BinaryDataSection(packed)

    encoded = section.encode()

    assert len(encoded) == section.length
    assert int.from_bytes(encoded[:3], "big") == section.length


# ---------------------------------------------------------------------
# Complex Binary Data Section
# ---------------------------------------------------------------------

def test_complex_binary_data_section():
    packed = ComplexPackedData(
        binary_scale_factor=0,
        decimal_scale_factor=0,
        reference_value=0.0,
        bits_per_value=8,
        number_of_first_order=1,
        number_of_second_order=4,
        group_widths=[2],
        secondary_bitmap=b"",
        first_order_data=b"\x00",
        second_order_data=b"\x1b",
    )

    section = BinaryDataSection(packed)

    encoded = section.encode()

    assert len(encoded) == section.length
    assert int.from_bytes(encoded[:3], "big") == section.length

    # Complex packing flag
    assert encoded[3] == 0x60

    # Extended flags
    assert encoded[13] == 0x30


# ---------------------------------------------------------------------
# End Section
# ---------------------------------------------------------------------

def test_end_section():
    section = EndSection()
    assert section.length == 4
    assert section.encode() == b"7777"