import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

# Load data
@st.cache_resource
def abrir_tis():
    gdf = gpd.read_parquet('dados/dados_relatorio.parquet')
    return gdf

gdf = abrir_tis()

# Unique states
estados = gdf['estado'].unique()

# Multi-select for states
selected_estados = st.sidebar.multiselect('Selecione o(s) estado(s)', options=sorted(estados), default=[])

# Filter municipalities based on selected states
if selected_estados:
    filtered_municipios = gdf[gdf['estado'].isin(selected_estados)]['muncipio'].unique()
else:
    filtered_municipios = gdf['muncipio'].unique()  # Show all if no state is selected

# Multi-select for municipalities
selected_municipios = st.sidebar.multiselect('Selecione o(s) município(s)', options=sorted(filtered_municipios), default=[])

# Filter the data based on selections
if selected_estados and selected_municipios:
    filtered_gdf = gdf[(gdf['estado'].isin(selected_estados)) & (gdf['muncipio'].isin(selected_municipios))]
elif selected_estados:
    filtered_gdf = gdf[gdf['estado'].isin(selected_estados)]
elif selected_municipios:
    filtered_gdf = gdf[gdf['muncipio'].isin(selected_municipios)]
else:
    filtered_gdf = gdf  # Show all if no filters are selected


col1,col2,col3,col4 = st.columns(4)

with col1:
    st.header('Quantidade de fazendas')
    st.subheader(str(filtered_gdf.count().loc['fid']))

with col2:
    st.header('Volume superior a 50 L')
    gdf_50l = filtered_gdf[(filtered_gdf['vol_arm_inferior_50_l'] == 'nao')]
    st.subheader(str(gdf_50l.count().loc['fid']))

with col3:
    st.header('Destinação de resíduos')
    gdf_50l = filtered_gdf[(filtered_gdf['destinacao_oleo_queimado'] == 'sim')]
    st.subheader(str(gdf_50l.count().loc['fid']))

with col3:
    st.header('Volume estimado (l)')
    st.subheader('0')

# Create a Folium map
m = folium.Map(location=[-14, -54], zoom_start=4, control_scale=True, tiles='Esri World Imagery')

# Add Layer Control
folium.LayerControl().add_to(m)


def style_function_fazendas(x): return{
    'fillColor': 'orange',
    'color':'black',
    'weight':1,
    'fillOpacity':0.6
}

filtered_gdf = filtered_gdf.to_crs(epsg=4326)

fazendas_limpo = gpd.GeoDataFrame(filtered_gdf,columns=['geometry'])

#folium.GeoJson(fazendas_limpo,style_function=style_function_fazendas,name='Fazendas').add_to(m)

for _, row in filtered_gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        #popup=row.get("vol_arm_inferior_50_l", "No id"),
        popup=('0'),
        tooltip="Volume estimado",
        radius=5,
        color="blue",
        fill=True,
        fill_color="cyan",
        fill_opacity=0.7,
    ).add_to(m)

bounds = filtered_gdf.total_bounds
m.fit_bounds([[bounds[1],bounds[0]],[bounds[3],bounds[2]]])

# Display the map
st_Data =st_folium(m, width="100%", key="mapa")

st.write(filtered_gdf)
