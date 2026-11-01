# GRIBGenerator

**GRIBGenerator** is a Python project for generating synthetic meteorological data files in GRIB format. It was developed to create test files for experimenting with GRIB decoding, binary data processing, and meteorological visualization.

Rather than relying on existing GRIB generation software, this project implements the file-generation process itself, providing control over the underlying data, grid definitions, and packing methods.

## Features

- **Synthetic weather datasets:** Generate patterns such as constant fields, gradients, checkerboards, random data, bullseye patterns, and simulated storms.
- **Multiple grid types:** Generate data using different grid projections, including latitude-longitude, Mercator, polar stereographic, Lambert conformal, and Gaussian grids.
- **Data packing:** Supports multiple methods of encoding numerical values, including simple and complex packing.
- **GRIB format support:** Organized into separate GRIB1 and GRIB2 implementations. Currently only supports GRIB1. GRIB2 implementation is still a work in progress.
- **Configurable generation:** Choose the dataset, grid, packing method, and output file.

## Example

Generate a synthetic gradient dataset on a latitude-longitude grid in a GRIB1 binary:

```bash
python GribGenerator.py --grid latlon --data gradient --packing simple --output gradient_latlon.grb
```

Generate a synthetic storm dataset on a Mercator grid with complex packing in a GRIB1 binary:

```bash
python GribGenerator.py --grid mercator --data storm --packing complex --output storm_mercator.grb
```

## Project Structure

```text
GribGenerator/
├── grib/
│   ├── grib1/
│   │   ├── encoder.py
│   │   ├── grids.py
│   │   ├── message.py
│   │   └── sections.py
│   ├── grib2/
│   │   ├── encoder.py
│   │   ├── message.py
│   │   ├── sections.py
│   │   └── templates/
│   └── datasets.py
├── tests/
├── GribGenerator.py
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/GribGenerator.git
cd GribGenerator
```

The generator uses Python's standard library for core functionality. Install pytest if you want to run the test suite:

```bash
python -m pip install pytest
```

## Running Tests

The test suite uses `pytest` and requires **wgrib** to be installed for GRIB file verification tests.

### Requirements

- Python
- pytest
- wgrib
**Windows users:** Tests must be run through WSL rather than native Windows Python.

### Running on Linux

Install pytest and ensure `wgrib` is available on your system:

```bash
python -m pip install pytest
```

Then run:

```bash
python -m pytest
```

### Running on Windows

The test suite is not currently supported when running pytest directly from native Windows. Some tests depend on `wgrib`, which must be run in a Linux environment.

On Windows, use **WSL**:

1. Install and configure WSL with a Linux distribution.
2. Install Python, pytest, and wgrib inside WSL.
3. Navigate to the project directory from WSL.
4. Run the test suite:

```bash
python3 -m pytest
```

**Important:** Running `pytest` directly through Windows PowerShell or Command Prompt may cause tests to fail because of the `wgrib` dependency and environment differences.

## Purpose

This project was created to help develop and test GRIB parsers and visualization software. By generating controlled datasets with different values, grid configurations, and encoding methods, it makes it possible to test how software handles a variety of meteorological data.

The project is also an exploration of binary file formats, data encoding, and the engineering behind meteorological data exchange.

## Technologies

- Python
- Binary data processing (`struct`)
- Command-line interfaces (`argparse`)
- pytest
- wgrib — External GRIB file verification utility

## Author
**ElementProgram5**

Developed as a personal project.
