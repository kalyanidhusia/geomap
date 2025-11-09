#!/usr/bin/env python3
"""
plot_us_state_map.py

Generate a high-quality choropleth map of U.S. states from a user-provided data file.

Automatically downloads the U.S. shapefile from:
https://github.com/kalyanidhusia/geomap/tree/main/state_geo_files

Example:
    python plot_us_state_map.py --data data.txt --value_column Property_Tax_Burden
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import requests
import zipfile
from io import BytesIO
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib as mpl

# -------------------------------------------------------------------------
# Download shapefile automatically from GitHub if not already cached
# -------------------------------------------------------------------------
def get_us_shapefile():
    repo_zip_url = "https://github.com/kalyanidhusia/geomap/archive/refs/heads/main.zip"
    local_dir = os.path.join(os.path.expanduser("~"), ".us_state_geo")

    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)
        print("📦 Downloading U.S. shapefile data from GitHub...")
        r = requests.get(repo_zip_url)
        with zipfile.ZipFile(BytesIO(r.content)) as zip_ref:
            zip_ref.extractall(local_dir)
        print("✅ Shapefile downloaded and extracted.")

    # locate shapefile
    shp_path = None
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".shp"):
                shp_path = os.path.join(root, file)
                break
    if not shp_path:
        raise FileNotFoundError("Could not locate the shapefile in the downloaded data.")
    return shp_path

# -------------------------------------------------------------------------
# Plotting function
# -------------------------------------------------------------------------
def plot_us_map(data_path, value_column, output_file="us_state_map.png"):
    # Load data
    df = pd.read_csv(data_path, sep="\t")
    if "State" not in df.columns:
        raise ValueError("Input file must contain a 'State' column.")

    # Load shapefile (auto-download if needed)
    shp_path = get_us_shapefile()
    usa = gpd.read_file(shp_path)

    # Merge shapefile and data
    merged = usa.merge(df, left_on="NAME", right_on="State", how="left")

    # Define color map (low → high gradient)
    cmap = LinearSegmentedColormap.from_list(
        "custom_us_gradient",
        ["#85011C", "#6E082D", "#BA005A", "#462A8C", "#172378"]
    )
    vmin, vmax = df[value_column].min(), df[value_column].max()
    norm = Normalize(vmin=vmin, vmax=vmax)

    # Assign color (grey for missing)
    merged["color"] = merged[value_column].apply(
        lambda x: cmap(norm(x)) if pd.notnull(x) else "#DEDEDE"
    )

    # Plot map
    fig, ax = plt.subplots(figsize=(12, 8))
    merged.plot(color=merged["color"], edgecolor="white", linewidth=1.2, ax=ax)

    # Add colorbar
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation="vertical", shrink=0.55, aspect=25, pad=0.01)
    cbar.set_label(
        f"{value_column.replace('_', ' ')}",
        fontsize=11, fontweight="bold", fontfamily="Arial", color="black", labelpad=10
    )
    cbar.ax.tick_params(labelsize=9, colors="black")
    for tick_label in cbar.ax.get_yticklabels():
        tick_label.set_fontfamily("Arial")
        tick_label.set_fontweight("medium")

    # Add state labels
    for _, row in merged.iterrows():
        code = row["STUSPS"]
        value = row[value_column]
        if pd.notnull(value):
            text = f"{code}\n{value:.2f}"
            color = "white"
        else:
            text = code
            color = "black"
        plt.annotate(
            text=text,
            xy=(row.geometry.centroid.x, row.geometry.centroid.y),
            ha="center",
            va="center",
            fontsize=11,
            fontfamily="Arial",
            fontweight="bold" if pd.notnull(value) else "medium",
            color=color,
            linespacing=1.1
        )

    # Title & layout
    ax.set_title(f"{value_column.replace('_', ' ')} by State", fontsize=14, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()

    # Save output
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"✅ Map saved as {output_file}")
    plt.close()

# -------------------------------------------------------------------------
# Command-line interface
# -------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a U.S. state choropleth map.")
    parser.add_argument("--data", required=True, help="Path to input data file (tab-separated).")
    parser.add_argument("--value_column", required=True, help="Numeric column name to visualize.")
    parser.add_argument("--output", default="us_state_map.png", help="Output image file name.")
    args = parser.parse_args()

    plot_us_map(args.data, args.value_column, args.output)
