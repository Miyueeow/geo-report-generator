"""
Phase 4: AI Narrative Layer
Loads the structured analysis from Phase 3 and uses Groq to generate
written insights/narrative summarizing the geospatial findings.
"""

import json
import os
from dotenv import load_dotenv
from groq import Groq

# ---- CONFIG ----

# ---- CONFIG ----
DATA_FOLDER = "data"
ANALYSIS_FILE = "analysis_results.json"
OUTPUT_FILE = "narrative.txt"

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def load_analysis() -> dict:
    filepath = os.path.join(DATA_FOLDER, ANALYSIS_FILE)
    with open(filepath, "r") as f:
        return json.load(f)


def build_prompt(analysis: dict) -> str:
    """
    Builds a prompt that gives Groq the structured data and asks
    for a written narrative report.
    """
    prompt = f"""
You are an urban data analyst writing a short report for a city planning audience.

Here is structured geospatial analysis data for the region: {analysis['region']}

- Area: {analysis['area_km2']} km²
- Total points of interest: {analysis['total_pois']}
- Distinct POI categories: {analysis['diversity']['total_distinct_categories']}
- Top 5 POI categories: {json.dumps(analysis['diversity']['top_5_categories'])}
- Intersection density: {analysis['walkability']['intersection_density_per_km2']} per km²
- Total street length: {analysis['walkability']['total_street_length_km']} km
- Street density: {analysis['walkability']['street_density_km_per_km2']} km per km²
- Circuity (street directness, 1.0 = perfectly straight): {analysis['walkability']['circuity_avg']}

Write a concise, professional narrative report (3-4 short paragraphs) that:
1. Summarizes what this data reveals about the area's urban character (e.g. car-dependent vs walkable, commercial vs residential mix)
2. Highlights the most interesting or notable finding
3. Notes any potential implications or considerations for urban planning
4. Avoids generic filler language — be specific and reference the actual numbers

Do not use markdown formatting. Write in plain prose paragraphs.
"""
    return prompt


def generate_narrative(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def save_narrative(text: str):
    filepath = os.path.join(DATA_FOLDER, OUTPUT_FILE)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Narrative saved to: {filepath}")


if __name__ == "__main__":
    print("Loading analysis data...")
    analysis = load_analysis()

    print("Building prompt...")
    prompt = build_prompt(analysis)

    print("Generating narrative with Groq (Llama 3.3)... (this may take a few seconds)")
    narrative = generate_narrative(prompt)

    save_narrative(narrative)

    print("\n--- Generated Narrative ---\n")
    print(narrative)