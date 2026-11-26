# LSGI1D03 · Groundwater depletion on a dynamic Earth

Course paper and figure replication materials for *Living on a Dynamic Earth* at The Hong Kong Polytechnic University.

## Paper

[Advances and Limitations in Linking GRACE-Based Groundwater Monitoring to Water-Security Decisions Since 2008](paper/LSGI1D03_Groundwater_Final_Essay.pdf)

The essay traces satellite gravity monitoring since 2008, examines competing explanations for the North China Plain recovery, and uses California well records to show why an aquifer-wide trend can miss risks to households.

## Figures

| Figure | Question | Files |
| --- | --- | --- |
| 1. North China Plain | How do storage, well levels, water supply, and rainfall change around the groundwater recovery? | [PNG](figures/Figure_1_North_China_Plain.png) · [PDF](figures/Figure_1_North_China_Plain.pdf) · [SVG](figures/Figure_1_North_China_Plain.svg) |
| 2. San Joaquin Basin | How do groundwater-level trends differ across nearby aquifer systems in California? | [PNG](figures/Figure_2_San_Joaquin_Aquifers.png) · [PDF](figures/Figure_2_San_Joaquin_Aquifers.pdf) · [SVG](figures/Figure_2_San_Joaquin_Aquifers.svg) |

## Reproduce the figures

From the repository root, run the following with Python 3.10 or later:

```sh
python -m pip install -r requirements.txt
python scripts/download_data.py
python scripts/prepare_data.py
python scripts/plot_figures.py
```

The download script checks local inputs against their SHA-256 hashes and restores missing originals from bundled parts or the pinned upstream downloads. The preparation script extracts the source tables and boundary records. The plotting script writes the PNG, PDF, and SVG versions into `figures/`. The workflow reproduces the essay figures from author-published source data.

## Repository layout

| Path | Contents |
| --- | --- |
| [`paper/`](paper/) | Public PDF of the course paper |
| [`data/raw/`](data/raw/) | Original inputs, archive parts, and upstream links |
| [`data/processed/`](data/processed/) | Figure-ready CSV and GeoJSON |
| [`data/sources.json`](data/sources.json) | Pinned URLs, licenses, and SHA-256 hashes |
| [`scripts/`](scripts/) | Source download, data extraction, and plotting |
| [`figures/`](figures/) | Figure outputs in three formats |

[Data sources and licensing](DATA_SOURCES.md) lists the upstream datasets, exact figure tables, and processing steps.
