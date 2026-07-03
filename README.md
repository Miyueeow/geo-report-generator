# Automated Geospatial Report Generator

An end-to-end pipeline that turns a region name into a fully automated GIS report — combining spatial data analysis with AI-generated insights.

## What it does

Give it a region name (e.g. *"Lipa, Batangas, Philippines"*), and it automatically:

1. **Geocodes** the region and pulls its boundary + 3,000+ points of interest from OpenStreetMap
2. **Visualizes** the data as an interactive clustered map
3. **Analyzes** POI density, category diversity, and walkability metrics (intersection density, street network stats)
4. **Generates insights** using an LLM (Llama 3.3 via Groq) to turn raw numbers into a written urban analysis
5. **Compiles everything** into a polished, shareable PDF report

## Why I built this

As a Data Analyst and AI Automation Developer, I wanted a project that didn't just visualize data, but built a real automated pipeline — from raw data ingestion to an AI-written narrative to a finished deliverable, with zero manual steps in between.

## Tech Stack

| Layer | Tools |
|---|---|
| Geospatial data | `osmnx`, `geopandas`, OpenStreetMap |
| Visualization | `folium` (interactive clustered maps) |
| Analysis | `geopandas`, `osmnx` network stats |
| AI narrative | Groq API (Llama 3.3 70B) |
| Report generation | `reportlab` (PDF) |

## Sample Output

- Interactive map: `output/region_map.html`
- Full PDF report: `output/geo_report.pdf`

*(Add a screenshot of your map and PDF here — this is the first thing people will look at.)*

## Pipeline

```
Region name
    ↓
Phase 1: Data Ingestion (OSM boundary + POIs)
    ↓
Phase 2: Interactive Map Visualization
    ↓
Phase 3: Spatial Analysis (density, diversity, walkability)
    ↓
Phase 4: AI Narrative Generation (Groq/Llama 3.3)
    ↓
Phase 5: PDF Report Compilation
```

## How to Run

```bash
# Clone the repo
git clone <your-repo-url>
cd geo-report-generator

# Set up environment
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Add your Groq API key to a .env file
echo GROQ_API_KEY=your_key_here > .env

# Run the pipeline
python phase1_data_ingestion.py
python phase2_map_visualization.py
python phase3_analysis.py
python phase4_ai_narrative.py
python phase5_pdf_report.py
```

## Example Insight (AI-generated)

> "The urban character of Lipa, Batangas, is revealed through its geospatial data to be largely car-dependent, with parking-related points of interest accounting for over 2,000 of the region's 3,001 total POIs..."

## Future Improvements

- Integrate real population/demographic data (currently OSM-only)
- Auto-generate the map screenshot instead of manual capture
- Wrap in a Streamlit app for live, interactive report generation

---

*Built with Python, OpenStreetMap data, and Groq's Llama 3.3 API.*