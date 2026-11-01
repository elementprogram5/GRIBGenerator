from pathlib import Path

from grib.grib2.encoder import Grib2Encoder
from grib.grib2.message import Grib2Message, Identification

from grib.grib2.templates.grid import GridDefinitionTemplate90
from grib.grib2.templates.products import ProductDefinitionTemplate415

from grib.packing import SimplePacking
from grib import datasets


def main() -> None:

    # ---------------------------------------------------------
    # Section 3: Grid Definition Template 3.0
    # ---------------------------------------------------------
    grid = GridDefinitionTemplate90()

    # ---------------------------------------------------------
    # Create synthetic field
    # ---------------------------------------------------------
    values, bitmap = datasets.gradient(
        grid.nx,
        grid.ny,
    )

    # ---------------------------------------------------------
    # Section 4: Product Definition Template 4.0
    # ---------------------------------------------------------
    product = ProductDefinitionTemplate415(
        parameter_category=0,
        parameter_number=0,
    )

    # ---------------------------------------------------------
    # Build GRIB2 message
    # ---------------------------------------------------------
    message = Grib2Message(
        discipline=0,
        identification=Identification(),
        grid=grid,
        product=product,
        values=values,
        bitmap=bitmap,
    )

    # ---------------------------------------------------------
    # Encode
    # ---------------------------------------------------------
    encoder = Grib2Encoder(
        packing=SimplePacking()
    )

    encoded = encoder.encode(message)

    # ---------------------------------------------------------
    # Basic validation
    # ---------------------------------------------------------
    assert encoded[:4] == b"GRIB"
    assert encoded[-4:] == b"7777"

    output = Path("basic_test.grib2")
    output.write_bytes(encoded)

    print(f"Wrote {output}")
    print(f"Size: {len(encoded)} bytes")


if __name__ == "__main__":
    main()
