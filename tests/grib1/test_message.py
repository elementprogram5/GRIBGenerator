import pytest

from grib.grib1.message import (
    Bitmap,
    ProductDefinition,
    Grib1Message,
)

from grib.grib1.grids import LatLonGrid


# ----------------------------------------------------------------------
# Bitmap
# ----------------------------------------------------------------------

def test_bitmap_creation():
    bitmap = Bitmap([True, False, True])

    assert bitmap.bits == [True, False, True]
    assert len(bitmap.bits) == 3


# ----------------------------------------------------------------------
# ProductDefinition
# ----------------------------------------------------------------------

def test_product_defaults():
    p = ProductDefinition()

    assert p.table_version == 3
    assert p.center_id == 7
    assert p.parameter_id == 11
    assert p.level_type == 100
    assert p.level_value == 500


def test_product_validate_success():
    p = ProductDefinition()

    # Should not raise.
    p.validate()


def test_product_validate_parameter():
    p = ProductDefinition(parameter_id=256)

    with pytest.raises(ValueError):
        p.validate()


def test_product_validate_level_type():
    p = ProductDefinition(level_type=300)

    with pytest.raises(ValueError):
        p.validate()


def test_product_validate_level_value():
    p = ProductDefinition(level_value=70000)

    with pytest.raises(ValueError):
        p.validate()


# ----------------------------------------------------------------------
# Grib1Message
# ----------------------------------------------------------------------

def test_grib_message_has_bitmap_false():
    grid = LatLonGrid(nx=2, ny=2)

    msg = Grib1Message(
        product=ProductDefinition(),
        grid=grid,
        values=[1.0, 2.0, 3.0, 4.0],
    )

    assert msg.has_bitmap is False


def test_grib_message_has_bitmap_true():
    grid = LatLonGrid(nx=2, ny=2)

    msg = Grib1Message(
        product=ProductDefinition(),
        grid=grid,
        values=[1.0, 2.0, 3.0, 4.0],
        bitmap=Bitmap([True, False, True, True]),
    )

    assert msg.has_bitmap is True


def test_grib_message_validate_success():
    grid = LatLonGrid(nx=2, ny=2)

    msg = Grib1Message(
        product=ProductDefinition(),
        grid=grid,
        values=[1.0, 2.0, 3.0, 4.0],
    )

    msg.validate()


def test_grib_message_wrong_number_of_values():
    grid = LatLonGrid(nx=2, ny=2)

    msg = Grib1Message(
        product=ProductDefinition(),
        grid=grid,
        values=[1.0, 2.0, 3.0],
    )

    with pytest.raises(ValueError):
        msg.validate()


def test_grib_message_invalid_product():
    grid = LatLonGrid(nx=2, ny=2)

    product = ProductDefinition(parameter_id=300)

    msg = Grib1Message(
        product=product,
        grid=grid,
        values=[1.0, 2.0, 3.0, 4.0],
    )

    with pytest.raises(ValueError):
        msg.validate()