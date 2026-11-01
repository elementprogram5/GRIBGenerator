from __future__ import annotations
import argparse
from pathlib import Path
from grib.grib1.encoder import Grib1Encoder
from grib.grib1.message import (Grib1Message, ProductDefinition)
from grib.packing import (SimplePacking, ComplexPacking)
from grib.grib1.grids import (LatLonGrid, MercatorGrid, PolarStereographicGrid, LambertConformalGrid, GaussianLatLonGrid, AlbersEqualAreaGrid, RotatedLatLonGrid, RotatedGaussianLatLonGrid, StretchedLatLonGrid, StretchedGaussianLatLonGrid, StretchedRotatedLatLonGrid, StretchedRotatedGaussianLatLonGrid, SpaceViewGrid, TinyGrid, LargeGrid)
from grib import datasets

GRID_TYPES = {
    "latlon": lambda: LatLonGrid(360, 181),
    "mercator": lambda: MercatorGrid(360, 181),
    "polar_stereographic": lambda: PolarStereographicGrid(181, 181),
    "lambert_conformal": lambda: LambertConformalGrid(181, 181),
    "gaussian_latlon": lambda: GaussianLatLonGrid(360, 181),
    "albers_equalarea": lambda: AlbersEqualAreaGrid(360, 181),
    "rotated_latlon": lambda: RotatedLatLonGrid(360, 181),
    "rotated_gaussian_latlon": lambda: RotatedGaussianLatLonGrid(360, 181),
    "stretched_latlon": lambda: StretchedLatLonGrid(360, 181),
    "stretched_gaussian_latlon": lambda: StretchedGaussianLatLonGrid(360, 181),
    "stretched_rotated_latlon": lambda: StretchedRotatedLatLonGrid(360, 181),
    "stretched_rotated_gaussian_latlon": lambda: StretchedRotatedGaussianLatLonGrid(360, 181),
    "spaceview": lambda: SpaceViewGrid(100, 100),
    "tiny": TinyGrid,
    "large": LargeGrid
}

DATASETS = {
    "constant": datasets.constant,
    "gradient": datasets.gradient,
    "checkerboard": datasets.checkerboard,
    "random": datasets.random_field,
    "bullseye": datasets.bullseye,
    "storm": datasets.storm,
    "windy_day": datasets.windy_day,
    "regular_day": datasets.regular_day,
    "extremes": datasets.extremes,
    "missing": datasets.missing,
}

PACKINGS = {
    "simple": SimplePacking,
    "complex": ComplexPacking,
}

def write_reference(values: list[float], bitmap,output: str | Path) -> None:
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        for i, value in enumerate(values):
            if bitmap is not None and not bitmap.bits[i]:
                file.write("nan\n")
            else:
                file.write(f"{value:.17g}\n")
    print(f"Reference values: {output_path}")

def generate(grid_name :str, data_name: str, packing_name: str, output: str | Path, seed: int | None,reference_output: str | Path | None = None) -> None:
    grid = GRID_TYPES[grid_name]()
    if data_name == "random":
        values, bitmap = DATASETS[data_name](grid.nx, grid.ny, seed or 0)
    else:
        values, bitmap = DATASETS[data_name](grid.nx, grid.ny)
        print(reference_output)
    if reference_output is not None:
        write_reference(values, bitmap, reference_output)
    message = Grib1Message(product=ProductDefinition(), grid=grid, values=values,bitmap=bitmap)
    encoder = Grib1Encoder(PACKINGS[packing_name]())
    data = encoder.encode(message)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    print(f"Generated: {output_path}")

def generate_all(output_dir: str | Path, seed: int | None ) -> None:
    output_dir = Path(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    for grid_name in GRID_TYPES:
        for dataset_name in DATASETS:
            for packing_name in PACKINGS:
                filename = (f"{dataset_name}_" f"{grid_name}_" f"{packing_name}.grb")
                generate(grid_name=grid_name, 
                        data_name=dataset_name, 
                        packing_name=packing_name, 
                        output=output_dir / filename, 
                        seed=seed)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="GribGenerator", 
                                     description="Generate synthetic GRIB1 files for parser and visualization testing.")
    parser.add_argument("--grid", choices=sorted(GRID_TYPES.keys()))
    parser.add_argument("--data", choices=sorted(DATASETS.keys()))
    parser.add_argument("--packing", choices=sorted(PACKINGS.keys()))
    parser.add_argument("--output", help="Output GRIB file path")
    parser.add_argument("--seed", type=int, default=0, help="Random seed")
    parser.add_argument("--reference-output", help="Optional output path for original reference values")
    parser.add_argument("--generate-all", action="store_true", help="Generate all combinations")
    parser.add_argument("--output-dir", default="generated", help="Output directory")
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.generate_all:
        generate_all(output_dir=args.output_dir, seed=args.seed)
        return
    missing = []
    if args.grid is None:
        missing.append("--grid")
    if args.data is None:
        missing.append("--data")
    if args.packing is None:
        missing.append("--packing")
    if args.output is None:
        missing.append("--output")
    if missing:
        parser.error(f"Missing required arguments: {', '.join(missing)}")
    generate(grid_name=args.grid,
        data_name=args.data,
        packing_name=args.packing,
        output=args.output,
        seed=args.seed,
        reference_output=args.reference_output) 
    
if __name__ == "__main__":
    main()