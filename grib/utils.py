from __future__ import annotations
import struct

class BitWriter:
    def __init__(self) -> None:
        self._buffer = bytearray()
        self._current_byte = 0
        self._bit_count = 0 
    def write(self, value: int, bits: int) -> None:
        if bits < 0:
            raise ValueError("bits must be non-negative")
        if bits == 0:
            return
        if value < 0:
            raise ValueError("BitWriter expects unsigned values; convert signed values first")
        if value >> bits:
            raise ValueError(f"value {value} does not fit in {bits} bits")
        while bits > 0:
            free = 8 - self._bit_count 
            if bits >= free:
                shift = bits - free
                chunk = (value >> shift) & ((1 << free) - 1)
                self._current_byte = ((self._current_byte << free) | chunk) & 0xFF
                self._buffer.append(self._current_byte)
                self._current_byte = 0
                self._bit_count = 0
                bits -= free
                value &= (1 << shift) - 1  
            else:
                self._current_byte = ((self._current_byte << bits) | (value & ((1 << bits) - 1))) & 0xFF
                self._bit_count += bits
                bits = 0
    def finish(self) -> bytes:
        if self._bit_count:
            self._current_byte = (self._current_byte << (8 - self._bit_count)) & 0xFF
            self._buffer.append(self._current_byte)
            self._current_byte = 0
            self._bit_count = 0
        return bytes(self._buffer)

def _bit_width_nonneg(x: int) -> int:
    return 0 if x == 0 else x.bit_length()

def uint1(value: int) -> bytes:
    if not 0 <= value <= 0xFF:
        raise ValueError(f"uint1 out of range: {value}")
    return value.to_bytes(1, "big", signed=False)

def uint2(value: int) -> bytes:
    if not 0 <= value <= 0xFFFF:
        raise ValueError(f"uint2 out of range: {value}")
    return value.to_bytes(2, "big", signed=False)

def uint3(value: int) -> bytes:
    if not 0 <= value <= 0xFFFFFF:
        raise ValueError(f"uint3 out of range: {value}")
    return value.to_bytes(3, "big", signed=False)

def uint4(value: int) -> bytes:
    return value.to_bytes(4, "big", signed=False)

def uint8(value: int) -> bytes:
    return value.to_bytes(8, "big", signed=False)

def sint2(value: int) -> bytes:
    return value.to_bytes(2, "big", signed=True)

def sint3(value: int) -> bytes:
    return value.to_bytes(3, "big", signed=True)

def sint4(value: int) -> bytes:
    if not -0x80000000 <= value <= 0x7FFFFFFF:
        raise ValueError(f"sint4 out of range: {value}")
    return value.to_bytes(4, "big", signed=True)

def encode_microdegrees(value: float) -> int:
    return round(value * 1_000_000)

def encode_millidegrees(value: float) -> int:
    return round(value * 1000)

def latlon_index(x: int, y: int, nx: int) -> int:
    return y * nx + x 

def ieee_float(value: float) -> bytes:
    return struct.pack(">f", value)

def ibm_float(value: float) -> bytes:
    if value == 0.0:
        return b"\x00\x00\x00\x00"
    sign = 0
    if value < 0:
        sign = 1
        value = abs(value)
    exponent = 64
    while value < 0.0625:
        value *= 16.0
        exponent -= 1
    while value >= 1.0:
        value /= 16.0
        exponent += 1
    fraction = int(
        value * (1 << 24)
    )
    fraction = min(
        fraction,
        0xFFFFFF,
    )
    first = (
        (sign << 7)
        | exponent
    )
    return bytes(
        [
            first,
            (fraction >> 16) & 0xFF,
            (fraction >> 8) & 0xFF,
            fraction & 0xFF,
        ]
    )