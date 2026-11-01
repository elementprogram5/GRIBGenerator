from pathlib import Path
import subprocess

from grib.grib1.encoder import Grib1Encoder
from grib.grib1.message import Grib1Message, ProductDefinition
from grib.grib1.grids import PolarStereographicGrid
from grib.packing import SimplePacking


def gradient(nx: int, ny: int):
    values = []
    for y in range(ny):
        for x in range(nx):
            values.append(float(x))
    return values

def test_encode_simple():

    nx = 181
    ny = 181

    grid = PolarStereographicGrid(
        nx=nx,
        ny=ny,
        lat1=60.0,
        lon1=0.0,
        lov=0.0,
        dx=60,
        dy=60,
    )
    values=gradient(nx, ny)
    message = Grib1Message(
        product=ProductDefinition(),
        grid=grid,
        values=values,
        bitmap=None
    )
    print(message.values)
    encoder = Grib1Encoder(SimplePacking())

    output = ( 
        Path(__file__).parent
        / "data"
        / "simple.grb"
    )

    output.parent.mkdir(exist_ok=True)

    output.write_bytes(
        encoder.encode(message)
    )
    print(output)
    result = subprocess.run(
        [
            "grib_dump",
            "-O",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    dump = result.stdout

    assert "editionNumber = 1" in dump
    #assert "packingType = grid_simple" in dump
    assert "Nx = 181" in dump
    assert "Ny = 181" in dump
    assert "numberOfValues = 32854" in dump

if __name__ == "__main__":
    test_encode_simple()