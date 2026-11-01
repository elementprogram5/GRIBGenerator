from __future__ import annotations
import math
import random
from grib.grib1.message import Bitmap

def constant(nx: int, ny: int):
    return [100.0] * (nx * ny), None

def gradient(nx: int, ny: int):
    values = []
    for y in range(ny):
        for x in range(nx):
            values.append(float(x))
    return values, None

def checkerboard(nx: int, ny: int):
    values = []
    for y in range(ny):
        for x in range(nx):
            values.append(float((x + y) % 2))
    return values, None

def random_field(nx: int, ny: int, seed: int):
    rng = random.Random(seed)
    return [rng.uniform(-50, 50)
            for _ in range(nx * ny)], None

def storm(nx: int, ny: int):
    values = []
    cx = nx / 2
    cy = ny / 2
    for y in range(ny):
        for x in range(nx):
            d = math.hypot(x - cx, y - cy)
            values.append(980 + d)
    return values, None

def windy_day(nx: int, ny: int):
    values = []
    for y in range(ny):
        for x in range(nx):
            values.append(1000 + x * 0.5 + math.sin(y * 0.1) * 5)
    return values, None

def regular_day(nx: int, ny: int):
    values = []
    for y in range(ny):
        for x in range(nx):
            value = (1012 + math.sin(x * 0.05) + math.cos(y * 0.05))
            values.append(value)
    return values, None
            
def missing(nx: int, ny: int):
    values = []
    bits = []
    for i in range(nx * ny):
        values.append(float(i))
        bits.append(i % 5 != 0)
    return values, Bitmap(bits)


def bullseye(nx: int,ny: int,):
    values = []
    cx = (nx - 1) / 2
    cy = (ny - 1) / 2
    max_distance = math.hypot(cx, cy)
    for y in range(ny):
        for x in range(nx):
            distance = math.hypot(x - cx, y - cy,)
            value = (100 * (1.0 - distance / max_distance))
            values.append(value)
    return values, None

def extremes(nx: int, ny: int): 
    values = []
    for i in range(nx * ny):
        match i % 5:
            case 0:
                values.append(-999.0)
            case 1:
                values.append(0.0)
            case 2:
                values.append(9999.0)
            case 3:
                values.append(-1.0)
            case _:
                values.append(12345.0)
    return values, None
