"""
Phase 2: Map Visualization
Load the boundary and POI data from Phase 1, and render them as an
interactive map with clustered markers using folium.
"""

import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import os

# ---- CONFIG ----
DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"
MAP_FILENAME = "region_map.html"


def load_data():
    """
    Loads the boundary and POI GeoJSON files saved in Phase 1.
    """
    boundary_gdf = gpd.read_file(os.path.join(DATA_FOLDER, "boundary.geojson"))
    pois_gdf = gpd.read_file(os.path.join(DATA_FOLDER, "pois.geojson"))
    return boundary_gdf, pois_gdf


def build_map(boundary_gdf: gpd.GeoDataFrame, pois_gdf: gpd.GeoDataFrame) -> folium.Map:
    """
    Builds an interactive folium map with:
    - the region boundary outlined
    - POIs grouped into clusters
    """
    # Center the map on the boundary's centroid
    centroid = boundary_gdf.geometry.centroid.iloc[0]
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=13, tiles="CartoDB positron")

    # Draw the region boundary outline
    folium.GeoJson(
        boundary_gdf,
        name="Region Boundary",
        style_function=lambda x: {
            "fillColor": "transparent",
            "color": "#2c3e50",
            "weight": 3,
        },
    ).add_to(m)

    # Create a marker cluster group for POIs
    marker_cluster = MarkerCluster(name="Points of Interest").add_to(m)

    for _, row in pois_gdf.iterrows():
        geom = row.geometry
        if geom is None:
            continue

        # Some OSM features are polygons (e.g. school grounds) — use centroid for marker placement
        point = geom.centroid if geom.geom_type != "Point" else geom

        # Get a readable name and category, fallback if missing
        name = row.get("name", "Unnamed")
        amenity = row.get("amenity", "N/A")

        popup_text = f"<b>{name}</b><br>Type: {amenity}"

        folium.Marker(
            location=[point.y, point.x],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=name,
        ).add_to(marker_cluster)

    # Add layer control so users can toggle boundary/POIs on and off
    folium.LayerControl().add_to(m)

    return m


def save_map(m: folium.Map, filename: str):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    m.save(filepath)
    print(f"Map saved to: {filepath}")
    print("Open this file in your browser to view it.")


if __name__ == "__main__":
    print("Loading data from Phase 1...")
    boundary, pois = load_data()

    print(f"Loaded boundary and {len(pois)} POIs")
    print("Building map...")
    region_map = build_map(boundary, pois)

    save_map(region_map, MAP_FILENAME)