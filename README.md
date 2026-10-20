# Vital Force farm data dashboard

Streamlit dashboard over the bundled `dados/dados_relatorio.parquet`. It filters
farm records by state and municipality, reports counts and selected operational
attributes, and places geometry centroids on a Folium map.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run home.py
```

No automated tests or CI are present. The dashboard and bundled Parquet were
not opened or executed during this audit.

## Data and privacy hold

The application exposes farm counts, state/municipality filters, operational
attributes and map locations. The repository does not document source,
consent/legal basis, minimization, update date or redistribution terms. Treat
the dataset as potentially sensitive property or business information. Do not
publish, redistribute or demonstrate it until a data owner confirms the rights
and an appropriately minimized/synthetic fixture is prepared.

The code also displays the full filtered GeoDataFrame and converts coordinates
to EPSG:4326 for map markers. No access control, aggregation threshold or
coordinate generalization is present. The existing license does not establish
rights to the bundled dataset.
