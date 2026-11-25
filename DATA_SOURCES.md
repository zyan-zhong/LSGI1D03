# Data sources

## Figure 1

- Long et al. (2025), [Unprecedented large-scale aquifer recovery through human intervention](https://doi.org/10.1038/s41467-025-62719-5).
- Xu, Long, and Cui (2025), [GroundwaterNCP_open v2.0](https://doi.org/10.5281/zenodo.17799537), CC BY 4.0. The original versioned archive is bundled.

From `sourceDataFigure.xlsx`: `Fig6d` provides North China Plain TWS, JPL–CSR spread, and its published trend. `Fig3` provides unconfined groundwater-level anomalies, spatial-sampling bounds, and its published trend. `Fig4` provides Hai River basin annual supply components. The two groundwater supply columns are summed. `Fig5a&c` provides North China Plain annual precipitation.

The raw workbook contains entries for July 2017–May 2018. Those months are retained in the extracted CSV with a mission-gap flag and omitted from the satellite curves. Panel c describes the Hai River basin, while the other panels depict North China Plain series. The two envelopes have different definitions. Neither is an independent cross-validation result.

## Figure 2

- Jasechko et al. (2024), [Rapid groundwater decline and some cases of recovery in aquifers globally](https://doi.org/10.1038/s41586-023-06879-8).
- Jasechko (2023), [groundwater level data, aquifer boundaries, and supplementary tables](https://doi.org/10.5281/zenodo.10003697), CC BY 4.0. Both original archives are bundled. The downloader reassembles the aquifer boundary archive from its two exact byte parts and verifies its published copy against the pinned checksum.
- Natural Earth public-domain [1:10m coastline data](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-coastline/), pinned in the source manifest.

The script selects all ten polygons whose broader-system label is “San Joaquin Basin of the Central Valley,” joins them to Supplementary Table 16 by aquifer name, and orders them by the reported median Theil–Sen slope. The ten source well counts sum to 5,659. A positive change in depth means a falling water level. The map uses WGS 84 coordinates and an approximate latitude-corrected scale. Coastline linework is selected for the map region. The bar chart and map have the same color bands and system numbers.

The plots are new renderings made from these datasets. [CC BY 4.0 license terms](https://creativecommons.org/licenses/by/4.0/).
