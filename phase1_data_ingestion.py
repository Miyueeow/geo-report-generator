"""
Phase 1: Data Ingestion
Geocode a region name into a boundary, then pull points of interest (POIs)
within that boundary using OpenStreetMap data via osmnx.
"""

import osmnx as ox
import geopandas as gpd

# ---- CONFIG ----
REGION_NAME = "Lipa, Batangas, Philippines"  # Change this to any city/region you want
OUTPUT_FOLDER = "data"

# osmnx settings (recommended defaults)
ox.settings.log_console = True
ox.settings.use_cache = True


def get_region_boundary(region_name: str) -> gpd.GeoDataFrame:
    """
    Converts a region name into a geographic boundary polygon.
    Tries a couple of query variations if the first one fails.
    """
    candidates = [
        region_name,
        region_name.replace(" City", ""),
        region_name.split(",")[0] + ", Batangas, Philippines",
    ]

    for query in candidates:
        try:
            print(f"Trying: {query}")
            boundary_gdf = ox.geocode_to_gdf(query)
            print(f"Success with: {query}")
            return boundary_gdf
        except TypeError:
            print(f"No polygon found for: {query}, trying next option...")
            continue

    raise ValueError(
        f"Could not find a valid boundary polygon for '{region_name}'. "
        "Try a different region name or check it on openstreetmap.org first."
    )


def get_pois(boundary_gdf: gpd.GeoDataFrame, tags: dict) -> gpd.GeoDataFrame:
    """
    Pulls points of interest within the given boundary polygon.
    `tags` follows OSM tagging schema, e.g. {"amenity": True}
    pulls ALL amenities (restaurants, schools, hospitals, etc.)
    """
    polygon = boundary_gdf.geometry.iloc[0]
    print("Fetching POIs... this may take a minute depending on region size")
    pois_gdf = ox.features_from_polygon(polygon, tags)
    return pois_gdf


def save_data(gdf: gpd.GeoDataFrame, filename: str):
    """
    Saves a GeoDataFrame to a GeoJSON file in the data folder.
    """
    import os
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    gdf.to_file(filepath, driver="GeoJSON")
    print(f"Saved: {filepath}")


if __name__ == "__main__":
    # Step 1: Get the region boundary
    boundary = get_region_boundary(REGION_NAME)
    save_data(boundary, "boundary.geojson")

    # Step 2: Get points of interest
    # We'll pull amenities (restaurants, schools, hospitals, banks, etc.)
    poi_tags = {"amenity": True}
    pois = get_pois(boundary, poi_tags)
    save_data(pois, "pois.geojson")

    print("\n--- Summary ---")
    print(f"Region: {REGION_NAME}")
    print(f"Boundary area (approx, in degrees²): {boundary.geometry.area.iloc[0]:.6f}")
    print(f"Total POIs found: {len(pois)}")