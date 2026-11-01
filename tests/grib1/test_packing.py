import pytest

from grib.packing import (
    SimplePacking,
    ComplexPacking,
    SimplePackedData,
    ComplexPackedData,
)


# ----------------------------------------------------------------------
# Simple Packing
# ----------------------------------------------------------------------

def test_simple_pack_returns_simplepackeddata():
    packing = SimplePacking()

    packed = packing.pack([1.0, 2.0, 3.0])

    assert isinstance(packed, SimplePackedData)


def test_simple_pack_reference_value():
    packing = SimplePacking()

    packed = packing.pack([10.0, 15.0, 20.0])

    assert packed.reference_value == 10.0


def test_simple_pack_binary_scale():
    packing = SimplePacking()

    packed = packing.pack([1.0, 2.0])

    assert packed.binary_scale_factor == 0


def test_simple_pack_bits_per_value():
    packing = SimplePacking()

    packed = packing.pack([5.0, 6.0, 7.0, 8.0])

    # values become 0,1,2,3
    assert packed.bits_per_value == 2


def test_simple_pack_generates_data():
    packing = SimplePacking()

    packed = packing.pack([0.0, 1.0, 2.0])

    assert isinstance(packed.data, bytes)
    assert len(packed.data) > 0


def test_simple_pack_bitmap():
    packing = SimplePacking()

    packed = packing.pack(
        [10.0, 20.0, 30.0],
        bitmap=[True, False, True],
    )

    assert packed.reference_value == 10.0


def test_simple_pack_empty():
    packing = SimplePacking()

    with pytest.raises(ValueError):
        packing.pack([])


# ----------------------------------------------------------------------
# Complex Packing
# ----------------------------------------------------------------------

def test_complex_constructor():
    packing = ComplexPacking(group_size=16)

    assert packing.group_size == 16


def test_complex_invalid_group_size():
    with pytest.raises(ValueError):
        ComplexPacking(group_size=0)


def test_complex_pack_returns_complexpackeddata():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(list(range(16)))

    assert isinstance(packed, ComplexPackedData)


def test_complex_reference_value():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack([10, 11, 12, 13])

    assert packed.reference_value == 10


def test_complex_number_of_second_order():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(list(range(20)))

    assert packed.number_of_second_order == 20


def test_complex_number_of_groups():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(list(range(20)))

    assert packed.number_of_first_order == 5
    assert packed.group_count == 5


def test_complex_group_widths_length():
    packing = ComplexPacking(group_size=8)

    packed = packing.pack(list(range(32)))

    assert len(packed.group_widths) == packed.number_of_first_order


def test_complex_first_order_data_exists():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(list(range(16)))

    assert isinstance(packed.first_order_data, bytes)
    assert len(packed.first_order_data) > 0


def test_complex_second_order_data_exists():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(list(range(16)))

    assert isinstance(packed.second_order_data, bytes)
    assert len(packed.second_order_data) > 0


def test_complex_secondary_bitmap_exists():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(list(range(16)))

    assert isinstance(packed.secondary_bitmap, bytes)
    assert len(packed.secondary_bitmap) > 0


def test_complex_bitmap():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(
        list(range(8)),
        bitmap=[True, False, True, True, False, True, True, True],
    )

    assert packed.number_of_second_order == 6


def test_complex_empty():
    packing = ComplexPacking()

    with pytest.raises(ValueError):
        packing.pack([])


def test_complex_decimal_scale():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(
        [1.0, 1.5, 2.0],
        decimal_scale=2,
    )

    assert packed.decimal_scale_factor == 2


def test_complex_binary_scale():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(
        [1.0, 2.0],
        binary_scale=3,
    )

    assert packed.binary_scale_factor == 3


def test_complex_spatial_differencing_flag():
    packing = ComplexPacking(group_size=4)

    packed = packing.pack(
        list(range(8)),
        spatial_differencing=True,
    )

    assert packed.spatial_differencing is True

def test_complex_gradient():
    values = [float(i) for i in range(181)]

    packing = ComplexPacking(group_size=32)
    packed = packing.pack(values)

    assert packed.number_of_second_order == 181
    assert packed.number_of_first_order == 6
    assert len(packed.group_widths) == 6