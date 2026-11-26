"""Render the two essay figures from the included source-derived tables."""
from datetime import datetime
from pathlib import Path
import json

import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, PathPatch
from matplotlib.path import Path as MplPath
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed'
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
NAVY, TEAL, RUST = '#235278', '#147D82', '#B75136'
TEXT, MUTED, GRID = '#202832', '#53616D', '#E2E6E8'
mpl.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 9,
    'text.color': TEXT, 'axes.labelcolor': TEXT, 'axes.edgecolor': '#7D8790',
    'axes.linewidth': 0.7, 'xtick.color': MUTED, 'ytick.color': MUTED,
    'xtick.major.size': 3, 'ytick.major.size': 3,
    'svg.fonttype': 'none', 'svg.hashsalt': 'lsgi1d03-groundwater', 'pdf.fonttype': 42, 'savefig.facecolor': 'white'
})

def export(fig, name):
    for fmt in ('png', 'pdf', 'svg'):
        metadata = {'CreationDate': None} if fmt == 'pdf' else {'Date': None} if fmt == 'svg' else None
        fig.savefig(OUT / f'{name}.{fmt}', dpi=450 if fmt == 'png' else None, metadata=metadata)
    plt.close(fig)

def panel(ax, letter, title):
    ax.text(0, 1.07, letter, transform=ax.transAxes, weight='bold', fontsize=12,
            va='bottom')
    ax.text(0.085, 1.08, title, transform=ax.transAxes, weight='bold',
            fontsize=10, va='bottom')

def date_axis(ax, letter, title):
    panel(ax, letter, title)
    for key in ('top', 'right'):
        ax.spines[key].set_visible(False)
    ax.set_xlim(datetime(2004, 7, 1), datetime(2025, 1, 1))
    ax.set_xticks([datetime(y, 1, 1) for y in (2005, 2010, 2015, 2020, 2025)])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.grid(axis='y', color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)
    ax.axvline(datetime(2020, 1, 1), color='#798790', lw=0.8, ls=(0, (3, 3)), zorder=2)

def north_china():
    monthly = pd.read_csv(DATA/'north_china_monthly.csv', parse_dates=['month'])
    annual = pd.read_csv(DATA/'north_china_and_hai_river_annual.csv')
    months = monthly['month'].to_numpy()
    dates = pd.to_datetime(annual['year'].astype(str), format='%Y').to_numpy()
    observed = monthly['intermission'].eq(0).to_numpy()
    fig, ax = plt.subplots(2, 2, figsize=(7.24, 4.92))
    fig.subplots_adjust(left=.105, right=.979, top=.9, bottom=.095, wspace=.38, hspace=.56)

    a, b, c, d = ax.flat
    date_axis(a, 'a', 'Regional water storage')
    a.axvspan(datetime(2017, 7, 1), datetime(2018, 6, 1), color='#DCE1E5', lw=0)
    a.axhline(0, color='#A0ABB2', lw=.75)
    a.fill_between(months, monthly['twsa_lower_km3'], monthly['twsa_upper_km3'],
                   where=observed, color='#CCDDE9', lw=0)
    a.plot(months, monthly['twsa_km3'].where(observed), color=NAVY, lw=.8, alpha=.7)
    a.plot(months, monthly['twsa_stl_km3'].where(observed), color=NAVY, lw=1.9)
    a.set_ylabel('TWS anomaly (km³)')
    a.yaxis.set_major_locator(MultipleLocator(20))
    a.annotate('Mission gap', (datetime(2017, 12, 10), 30),
               xytext=(datetime(2015, 6, 1), 38), color=MUTED, fontsize=7.9,
               ha='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=.55))

    date_axis(b, 'b', 'Unconfined aquifer wells')
    b.axhline(0, color='#A0ABB2', lw=.75)
    b.fill_between(months, monthly['level_lower_m'], monthly['level_upper_m'],
                   color='#D0E6E5', lw=0)
    b.plot(months, monthly['unconfined_level_anomaly_m'], color=TEAL, lw=.75, alpha=.62)
    b.plot(months, monthly['level_stl_m'], color='#136A74', lw=1.9)
    b.set_ylabel('Water-level anomaly (m)')
    b.set_ylim(-3, 3.35)
    b.yaxis.set_major_locator(MultipleLocator(1.5))
    b.text(.03, .92, 'Higher = shallower', transform=b.transAxes, fontsize=7.8,
           color=MUTED, va='top')

    date_axis(c, 'c', 'Annual supply by source')
    c.plot(dates, annual['hrb_groundwater_supply_km3'], color=NAVY, lw=1.55,
           marker='o', markersize=2.4, label='Groundwater (both types)')
    c.plot(dates, annual['hrb_yangtze_diversion_km3'], color=RUST, lw=1.45,
           marker='s', markersize=2.5, label='Yangtze diversion')
    c.set_ylim(-1, 38)
    c.yaxis.set_major_locator(MultipleLocator(10))
    c.set_ylabel('Hai River basin (km³ yr⁻¹)')
    c.legend(frameon=False, fontsize=7.3, loc='upper left', labelspacing=.25,
             handlelength=1.65, borderaxespad=.25)

    date_axis(d, 'd', 'Annual precipitation')
    highlights = [TEAL if yr == 2021 else '#BACBD3' for yr in annual['year']]
    d.bar(mdates.date2num(dates), annual['ncp_precipitation_mm'], width=250, color=highlights, zorder=2.5)
    d.set_ylim(0, 1010)
    d.yaxis.set_major_locator(MultipleLocator(250))
    d.set_ylabel('Precipitation (mm yr⁻¹)')
    d.annotate('2021  ·  838.5 mm', (datetime(2021, 1, 1), 838.5),
               xytext=(datetime(2024, 2, 1), 955), color='#136A74',
               fontsize=8.1, ha='right', va='center',
               arrowprops=dict(arrowstyle='-', color=TEAL, lw=.65))
    export(fig, 'Figure_1_North_China_Plain')

CATEGORIES = [
    (-np.inf, 0.0, '#2C777E', 'Shallowing (<0)'),
    (0.0, 0.10, '#E5D5BC', '0 to <0.10'),
    (0.10, 0.50, '#D58B50', '0.10 to <0.50'),
    (0.50, np.inf, '#A64431', '≥0.50'),
]

def palette(value):
    return next(color for lo, hi, color, _ in CATEGORIES if lo <= value < hi)

def polygon_path(geometry):
    coords = geometry['coordinates']
    polygon_list = [coords] if geometry['type'] == 'Polygon' else coords
    vertices, commands = [], []
    for part in polygon_list:
        for ring in part:
            vertices.extend(ring)
            commands.extend([MplPath.MOVETO] + [MplPath.LINETO] * (len(ring)-2) + [MplPath.CLOSEPOLY])
    return MplPath(vertices, commands)

# Placement of numbered labels near the shapes, with leader lines for small areas.
LABELS = {
    1: (-120.29, 37.04), 2: (-119.99, 36.91), 3: (-120.60, 37.28),
    4: (-120.74, 37.51), 5: (-121.23, 38.36), 6: (-120.82, 37.71),
    7: (-120.87, 37.03), 8: (-121.78, 37.93), 9: (-121.50, 37.73),
    10: (-121.13, 38.02)
}

def california():
    table = pd.read_csv(DATA/'san_joaquin_aquifer_trends.csv')
    assert len(table) == 10 and table['monitoring_wells'].sum() == 5659
    table = table.set_index('map_id')
    features = json.loads((DATA/'san_joaquin_boundaries.geojson').read_text())['features']
    coast = json.loads((DATA/'california_coastline.geojson').read_text())['coordinates']
    fig = plt.figure(figsize=(7.24, 4.22))
    ax = fig.add_axes([.07, .18, .42, .69])
    bars = fig.add_axes([.703, .18, .245, .69])
    for x, letter, title in ((.07, 'a', 'Mapped aquifer systems'),
                             (.506, 'b', 'Groundwater-level trends')):
        fig.text(x, .925, letter, weight='bold', fontsize=12, va='bottom')
        fig.text(x+.031, .929, title, weight='bold', fontsize=10, va='bottom')
    for line in coast:
        xy = np.array(line)
        ax.plot(xy[:,0], xy[:,1], lw=.55, color='#879CAA', zorder=1)
    for feature in features:
        key = int(feature['properties']['map_id'])
        row = table.loc[key]
        color = palette(row['median_theil_sen_depth_m_per_year'])
        ax.add_patch(PathPatch(polygon_path(feature['geometry']), facecolor=color,
                               edgecolor='#65594F', linewidth=.5, zorder=2))
    for k, (x, y) in LABELS.items():
        ax.text(x, y, str(k), ha='center', va='center', fontsize=7.5, zorder=4,
                bbox=dict(boxstyle='circle,pad=.18', facecolor='white', edgecolor='#677581', lw=.45))
    ax.set_xlim(-123.04, -119.63)
    ax.set_ylim(36.62, 38.66)
    ax.set_aspect(1 / np.cos(np.deg2rad(37.7)), adjustable='box', anchor='N')
    ax.set_xticks([-122.5,-121.5,-120.5], ['122.5° W','121.5° W','120.5° W'])
    ax.set_yticks([37.0,38.0], ['37° N','38° N'])
    ax.tick_params(labelsize=7.7)
    ax.grid(color='#DFE4E7', linewidth=.55)
    ax.set_axisbelow(True)
    ax.text(-122.96,38.53,'California, USA', fontsize=8.0, color=MUTED, va='center')
    ax.text(-122.77,37.21,'Pacific\nOcean',color='#688496', fontsize=7.6, linespacing=1.0)
    x0,y0 = -122.9,36.77
    delta = 50/(111.32*np.cos(np.deg2rad(y0)))
    ax.plot([x0,x0+delta],[y0,y0],color=MUTED,lw=.9)
    ax.text(x0+delta/2,y0+.036,'50 km',color=MUTED,fontsize=7,ha='center',va='bottom')

    slopes = table['median_theil_sen_depth_m_per_year'].to_numpy()
    order = np.arange(len(table))
    names = [f'{i}   {name.removesuffix(" Basin")}' for i, name in zip(table.index,table['aquifer_system'])]
    bars.barh(order, slopes, color=[palette(s) for s in slopes], edgecolor='#665A4D',
              linewidth=.5, height=.57, zorder=3)
    bars.axvline(0, color='#6E7983', lw=.75, zorder=2)
    bars.set_ylim(len(table)-.42, -.66)
    bars.set_xlim(-.15, 1.17)
    bars.set_yticks(order, names)
    bars.set_xticks([0,.5,1],['0','0.5','1.0'])
    bars.tick_params(axis='y', length=0, pad=4, labelsize=8.0)
    bars.grid(axis='x', color=GRID, lw=.65)
    bars.set_axisbelow(True)
    bars.set_xlabel('Median depth trend (m yr⁻¹)', labelpad=4, fontsize=8.5)
    for spine in ('top','right','left'):
        bars.spines[spine].set_visible(False)
    for idx, slope in enumerate(slopes):
        label = f'{slope:.2f}'.replace('-', '−')
        bars.text(slope + .035 if slope >= 0 else .028, idx, label,
                  va='center', ha='left', fontsize=7.4, color=TEXT)
    eastern = table.loc[table['aquifer_system'].eq('Eastern San Joaquin Basin')].iloc[0]
    row = list(table.index).index(eastern.name)
    percentage = eastern['fraction_deepening']
    bars.text(.41, row, f'{percentage:.0%} had falling levels',
              ha='left', va='center', fontsize=7.6, color=TEXT)
    fig.legend([Patch(facecolor=color,edgecolor='#665A4D',linewidth=.5) for _,_,color,_ in CATEGORIES],
               [name for _,_,_,name in CATEGORIES], frameon=False,
               loc='lower center', bbox_to_anchor=(.445, .035), ncol=4, fontsize=8.0,
               handlelength=1.25, columnspacing=1.35)
    export(fig,'Figure_2_San_Joaquin_Aquifers')

if __name__ == '__main__':
    north_china()
    california()
