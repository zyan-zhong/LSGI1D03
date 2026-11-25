"""Extract the exact published tables and boundaries used in Figures 1 and 2."""

from csv import writer
from io import BytesIO
import hashlib
import json
from math import isclose
from pathlib import Path
from zipfile import ZipFile

import openpyxl
import shapefile


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'data' / 'processed'


def verify_inputs():
    sources = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
    for source in sources:
        path = RAW / source['file']
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path.name}. Download it from {source['download']}.")
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        if checksum != source['sha256']:
            raise ValueError(f'SHA-256 mismatch for {path.name}. Check the upstream version.')


def sheet_rows(book, sheet, first_row):
    return book[sheet].iter_rows(min_row=first_row, values_only=True)


def write_csv(name, heading, rows):
    with (OUT / name).open('w', newline='', encoding='utf-8') as target:
        out = writer(target)
        out.writerow(heading)
        out.writerows(rows)


def write_geojson(name, value):
    (OUT / name).write_text(json.dumps(value, separators=(',', ':')), encoding='utf-8')


def prepare_north_china():
    with ZipFile(RAW / 'GroundwaterNCP_open-v2.0.zip') as archive:
        book = openpyxl.load_workbook(
            BytesIO(archive.read('YuanchengXu2718-GroundwaterNCP_open-a24aab4/sourceDataFigure.xlsx')),
            read_only=True, data_only=True,
        )
    try:
        tws = {r[0]: r[1:5] for r in sheet_rows(book, 'Fig6d', 3) if r[0]}
        wells = {r[0]: r[1:5] for r in sheet_rows(book, 'Fig3', 3) if r[0]}
        rain = {r[0]: r[1] for r in sheet_rows(book, 'Fig5a&c', 2) if isinstance(r[0], int)}
        supply = {r[0]: (r[3] + r[4], r[6]) for r in sheet_rows(book, 'Fig4', 3) if isinstance(r[0], int)}
    finally:
        book.close()

    assert len(tws) == 240 and tws.keys() == wells.keys()
    assert len(rain) == 20 and len(supply) == 19
    assert isclose(supply[2005][0], 25.3) and isclose(supply[2023][0], 12.9)
    assert isclose(rain[2021], 838.5)
    write_csv(
        'north_china_monthly.csv',
        ['month','twsa_km3','twsa_upper_km3','twsa_lower_km3','twsa_stl_km3',
         'unconfined_level_anomaly_m','level_upper_m','level_lower_m','level_stl_m','intermission'],
        ((date, *values, *wells[date], int('2017-07' <= date <= '2018-05'))
         for date, values in tws.items()),
    )
    write_csv(
        'north_china_and_hai_river_annual.csv',
        ['year','ncp_precipitation_mm','hrb_groundwater_supply_km3','hrb_yangtze_diversion_km3'],
        ((year, precip, *supply.get(year, ('', ''))) for year, precip in rain.items()),
    )


def prepare_san_joaquin():
    group = 'San Joaquin Basin of the Central Valley'
    suffix = f' ({group})'
    with ZipFile(RAW / 'Jasechko_et_al_2024_SupplementaryTables.zip') as archive:
        book = openpyxl.load_workbook(BytesIO(archive.read('Supplementary_Table_16.xlsx')),
                                      read_only=True, data_only=True)
    try:
        systems = {row[0].removesuffix(suffix): row for row in book.active.values
                   if isinstance(row[0], str) and row[0].endswith(suffix)}
    finally:
        book.close()

    assert len(systems) == 10 and sum(row[2] for row in systems.values()) == 5659
    assert systems['Chowchilla Basin'][4] == 1.02
    assert systems['Eastern San Joaquin Basin'][4:6] == (-0.05, 0.31)
    ordered = sorted(systems, key=lambda name: (-systems[name][4], name))
    codes = {name: str(index) for index, name in enumerate(ordered, 1)}
    write_csv(
        'san_joaquin_aquifer_trends.csv',
        ['map_id','aquifer_system','area_km2','monitoring_wells','median_theil_sen_depth_m_per_year',
         'fraction_deepening','fraction_deepening_above_0_5_m_per_year'],
        ((codes[name], name, row[1], row[2], *row[4:7]) for name in ordered for row in [systems[name]]),
    )

    prefix = 'jasechko_et_al_2024_aquifers'
    with ZipFile(RAW / 'Jasechko_et_al_2024_AquiferSpatialData.zip') as archive:
        builder = shapefile.Reader(
            **{ext: BytesIO(archive.read(f'{prefix}.{ext}')) for ext in ('shp', 'shx', 'dbf')},
            encoding='utf-8',
        )
        features = []
        for item in builder.iterShapeRecords():
            if item.record['Broader'] == group:
                name = item.record['Aquifer']
                features.append({
                    'type': 'Feature',
                    'properties': {'map_id': codes[name], 'aquifer_system': name},
                    'geometry': item.shape.__geo_interface__,
                })
    assert len(features) == len(codes)
    write_geojson('san_joaquin_boundaries.geojson', {'type': 'FeatureCollection', 'features': features})

    source = json.loads((RAW / 'ne_10m_coastline.geojson').read_text(encoding='utf-8'))
    selected = []
    for feature in source['features']:
        geometry = feature['geometry']
        lines = geometry['coordinates'] if geometry['type'] == 'MultiLineString' else [geometry['coordinates']]
        for line in lines:
            if any(-124 < lon < -121.7 and 35 < lat < 39 for lon, lat in line):
                selected.append(line)
    write_geojson('california_coastline.geojson', {'type': 'MultiLineString', 'coordinates': selected})


if __name__ == '__main__':
    verify_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    prepare_north_china()
    prepare_san_joaquin()
