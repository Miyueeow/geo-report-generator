"""
Phase 3: Analysis Layer
Compute POI density by category, category diversity, and walkability
metrics (intersection density, road network length) using OSM data only.
"""

import geopandas as gpd
import osmnx as ox
import json
import os

# ---- CONFIG ----
DATA_FOLDER = "data"
REGION_NAME = "Lipa, Batangas, Philippines"  # keep consistent with Phase 1


def load_boundary_and_pois():
    boundary_gdf = gpd.read_file(os.path.join(DATA_FOLDER, "boundary.geojson"))
    pois_gdf = gpd.read_file(os.path.join(DATA_FOLDER, "pois.geojson"))
    return boundary_gdf, pois_gdf


def get_area_km2(boundary_gdf: gpd.GeoDataFrame) -> float:
    """
    Re-projects boundary to a metric CRS to get an accurate area in km².
    """
    # Project to a Philippines-appropriate metric CRS (UTM zone 51N)
    projected = boundary_gdf.to_crs(epsg=32651)
    area_km2 = projected.geometry.area.iloc[0] / 1_000_000  # m² to km²
    return area_km2


def compute_poi_density(pois_gdf: gpd.GeoDataFrame, area_km2: float) -> dict:
    """
    Counts POIs by category (amenity type) and computes density per km².
    """
    if "amenity" not in pois_gdf.columns:
        return {}

    counts = pois_gdf["amenity"].value_counts().to_dict()
    density = {
        category: {
            "count": count,
            "density_per_km2": round(count / area_km2, 2)
        }
        for category, count in counts.items()
    }
    return density


def compute_category_diversity(poi_density: dict) -> dict:
    """
    Simple diversity measure: how many distinct POI categories exist,
    and what the top 5 categories are by count.
    """
    total_categories = len(poi_density)
    sorted_categories = sorted(
        poi_density.items(), key=lambda x: x[1]["count"], reverse=True
    )
    top_5 = [{"category": cat, "count": data["count"]} for cat, data in sorted_categories[:5]]

    return {
        "total_distinct_categories": total_categories,
        "top_5_categories": top_5,
    }


def compute_walkability(region_name: str, boundary_gdf: gpd.GeoDataFrame) -> dict:
    """
    Pulls the road network and computes intersection density and
    total road length as walkability proxies.
    """
    print("Fetching road network... this may take a minute")
    polygon = boundary_gdf.geometry.iloc[0]
    graph = ox.graph_from_polygon(polygon, network_type="walk")

    # Basic stats from osmnx
    stats = ox.basic_stats(graph)

def compute_walkability(region_name: str, boundary_gdf: gpd.GeoDataFrame, area_km2: float) -> dict:
    """
    Pulls the road network and computes intersection density and
    total road length as walkability proxies.
    """
    print("Fetching road network... this may take a minute")
    polygon = boundary_gdf.geometry.iloc[0]
    graph = ox.graph_from_polygon(polygon, network_type="walk")

    # Basic stats from osmnx
    stats = ox.basic_stats(graph)

    intersection_count = stats.get("intersection_count", 0)
    street_length_total_km = round(stats.get("street_length_total", 0) / 1000, 2)

    walkability = {
        "intersection_count": intersection_count,
        "intersection_density_per_km2": round(intersection_count / area_km2, 2),
        "total_street_length_km": street_length_total_km,
        "street_density_km_per_km2": round(street_length_total_km / area_km2, 2),
        "circuity_avg": stats.get("circuity_avg", None),
    }
    return walkability

def save_analysis(results: dict, filename: str = "analysis_results.json"):
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Analysis saved to: {filepath}")


if __name__ == "__main__":
    print("Loading data...")
    boundary, pois = load_boundary_and_pois()

    print("Computing area...")
    area_km2 = get_area_km2(boundary)
    print(f"Region area: {area_km2:.2f} km²")

    print("Computing POI density...")
    poi_density = compute_poi_density(pois, area_km2)

    print("Computing category diversity...")
    diversity = compute_category_diversity(poi_density)

    print("Computing walkability metrics...")
    walkability = compute_walkability(REGION_NAME, boundary, area_km2)

    results = {
        "region": REGION_NAME,
        "area_km2": round(area_km2, 2),
        "total_pois": len(pois),
        "poi_density_by_category": poi_density,
        "diversity": diversity,
        "walkability": walkability,
    }

    save_analysis(results)

    print("\n--- Summary ---")
    print(f"Region: {REGION_NAME}")
    print(f"Area: {area_km2:.2f} km²")
    print(f"Total POIs: {len(pois)}")
    print(f"Distinct categories: {diversity['total_distinct_categories']}")
    print(f"Top category: {diversity['top_5_categories'][0]}")
    print(f"Intersection density: {walkability['intersection_density_per_km2']}")