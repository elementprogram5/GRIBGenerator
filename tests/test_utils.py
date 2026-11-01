import pytest

from grib.utils import (
    BitWriter,
    uint1,
    uint2,
    uint3,
    uint4,
    sint2,
    sint3,
    encode_millidegrees,
    latlon_index,
    ibm_float,
    _bit_width_nonneg,
)


# ----------------------------------------------------------------------
# BitWriter
# ----------------------------------------------------------------------

def test_bitwriter_single_byte():
    writer = BitWriter()
    writer.write(0b10101010, 8)
    assert writer.finish() == b"\xaa"


def test_bitwriter_multiple_writes():
    writer = BitWriter()
    writer.write(0b101, 3)
    writer.write(0b11, 2)
    writer.write(0b000, 3)
    assert writer.finish() == b"\xb8"


def test_bitwriter_crosses_byte_boundary():
    writer = BitWriter()
    writer.write(0xABC, 12)
    assert writer.finish() == b"\xab\xc0"


def test_bitwriter_padding():
    writer = BitWriter()
    writer.write(1, 1)
    assert writer.finish() == b"\x80"


def test_bitwriter_zero_bits():
    writer = BitWriter()
    writer.write(12345, 0)
    assert writer.finish() == b""


def test_bitwriter_negative_bits():
    writer = BitWriter()
    with pytest.raises(ValueError):
        writer.write(1, -1)


def test_bitwriter_negative_value():
    writer = BitWriter()
    with pytest.raises(ValueError):
        writer.write(-1, 8)


def test_bitwriter_value_too_large():
    writer = BitWriter()
    with pytest.raises(ValueError):
        writer.write(8, 3)


# ----------------------------------------------------------------------
# Bit width
# ----------------------------------------------------------------------

def test_bit_width_nonneg():
    assert _bit_width_nonneg(0) == 0
    assert _bit_width_nonneg(1) == 1
    assert _bit_width_nonneg(2) == 2
    assert _bit_width_nonneg(255) == 8
    assert _bit_width_nonneg(256) == 9


# ----------------------------------------------------------------------
# Unsigned integers
# ----------------------------------------------------------------------

def test_uint1():
    assert uint1(255) == b"\xff"


def test_uint2():
    assert uint2(65535) == b"\xff\xff"


def test_uint3():
    assert uint3(0x123456) == b"\x12\x34\x56"


def test_uint4():
    assert uint4(0x12345678) == b"\x12\x34\x56\x78"


def test_uint1_out_of_range():
    with pytest.raises(ValueError):
        uint1(256)


def test_uint2_out_of_range():
    with pytest.raises(ValueError):
        uint2(70000)


def test_uint3_out_of_range():
    with pytest.raises(ValueError):
        uint3(0x1000000)


# ----------------------------------------------------------------------
# Signed integers
# ----------------------------------------------------------------------

def test_sint2():
    assert sint2(-1) == b"\xff\xff"
    assert sint2(1) == b"\x00\x01"


def test_sint3():
    assert sint3(-1) == b"\xff\xff\xff"
    assert sint3(1) == b"\x00\x00\x01"


# ----------------------------------------------------------------------
# Miscellaneous helpers
# ----------------------------------------------------------------------

def test_encode_millidegrees():
    assert encode_millidegrees(1.234) == 1234
    assert encode_millidegrees(-1.5) == -1500


def test_latlon_index():
    assert latlon_index(0, 0, 10) == 0
    assert latlon_index(5, 2, 10) == 25
    assert latlon_index(9, 9, 10) == 99


# ----------------------------------------------------------------------
# IBM floating point
# ----------------------------------------------------------------------

def test_ibm_float_zero():
    assert ibm_float(0.0) == b"\x00\x00\x00\x00"


def test_ibm_float_positive():
    result = ibm_float(1.0)
    assert isinstance(result, bytes)
    assert len(result) == 4


def test_ibm_float_negative():
    result = ibm_float(-1.0)
    assert isinstance(result, bytes)
    assert len(result) == 4

    # Sign bit should be set.
    assert result[0] & 0x80