import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

# Page configuration
st.set_page_config(
    page_title="Inequality & UHI | NYC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_hvi_data():
    """Load Heat Vulnerability Index data from NYC Health EHDP."""
    import os
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hvi-nta-2020.csv')
    df = pd.read_csv(csv_path)
    borough_map = {
        'BX': 'Bronx', 'BK': 'Brooklyn', 
        'MN': 'Manhattan', 'QN': 'Queens', 'SI': 'Staten Island'
    }
    df['Borough'] = df['NTACode'].str[:2].map(borough_map)
    return df

@st.cache_data
def get_borough_data(hvi_df):
    """Aggregate NTA data to borough level."""
    borough_agg = hvi_df.groupby('Borough').agg({
        'HVI_RANK': 'mean',
        'SURFACE_TEMP': 'mean',
        'GREENSPACE': 'mean',
        'PCT_HOUSEHOLDS_AC': 'mean',
        'MEDIAN_INCOME': 'mean'
    }).round(1).reset_index()
    
    coords = {
        'Manhattan': (40.7831, -73.9712),
        'Bronx': (40.8448, -73.8648),
        'Brooklyn': (40.6782, -73.9442),
        'Queens': (40.7282, -73.7949),
        'Staten Island': (40.5795, -74.1502)
    }
    borough_agg['lat'] = borough_agg['Borough'].map(lambda x: coords[x][0])
    borough_agg['lon'] = borough_agg['Borough'].map(lambda x: coords[x][1])
    return borough_agg

@st.cache_data(ttl=3600)
def load_nyc_borough_geojson():
    """Load NYC borough boundaries."""
    urls = [
        "https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson",
        "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/new-york-city-boroughs.geojson"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                geojson = response.json()
                for feature in geojson.get('features', []):
                    props = feature.get('properties', {})
                    name = props.get('boro_name') or props.get('name') or props.get('BoroName') or ''
                    props['boro_name'] = name
                return geojson
        except:
            continue
    return None

@st.cache_data(ttl=3600)
def load_nta_geojson():
    """Load NYC NTA boundaries."""
    url = "https://data.cityofnewyork.us/api/geospatial/9nt8-h7nd?method=export&format=GeoJSON"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #fff8f0 0%, #fff0e6 50%, #ffe8d6 100%);
    }
    
    [data-testid="stSidebar"] {
        background: #fffaf5;
        border-right: 1px solid #f0e6dc;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .page-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
        max-width: 800px;
        line-height: 1.6;
    }
    
    .section-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: #f97316;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        margin-top: 2rem;
    }
    
    .section-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    
    .divider {
        height: 1px;
        background: rgba(0,0,0,0.08);
        margin: 32px 0;
    }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Overview", type="secondary"):
    st.switch_page("app.py")

st.markdown('<p class="section-label">02 / Equity</p>', unsafe_allow_html=True)
st.markdown('<h1 class="page-header">Environmental Justice and Heat Exposure</h1>', unsafe_allow_html=True)
st.markdown("""
<p class="page-subtitle">
In the 1930s, the Home Owners' Loan Corporation (HOLC) graded neighborhoods from A ("Best") to 
D ("Hazardous") based on perceived investment risk. Areas with Black and immigrant residents 
received the lowest grades—a practice known as "redlining." These designations shaped decades 
of investment decisions.
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">Geographic Distribution</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Heat Vulnerability Across NYC</p>', unsafe_allow_html=True)

st.markdown("""
The [Heat Vulnerability Index (HVI)](https://a816-dohbesp.nyc.gov/IndicatorPublic/data-explorer/climate/?id=2411#display=summary), 
developed by NYC DOHMH, combines surface temperature, poverty levels, AC access, green space, 
and age demographics. Neighborhoods scoring 4-5 are concentrated in the **South Bronx**, 
**Central Brooklyn**, and **Northern Manhattan**.
""")

hvi_data = load_hvi_data()
borough_data = get_borough_data(hvi_data)

# Controls
ctrl_col1, ctrl_col2 = st.columns(2)

with ctrl_col1:
    view_level = st.radio("View by:", ["Borough", "Neighborhood (NTA)"], horizontal=True)

with ctrl_col2:
    metric_options = {
        "Heat Vulnerability Index": ("HVI_RANK", "HVI (1-5)", "YlOrRd", 1, 5),
        "Surface Temperature": ("SURFACE_TEMP", "Surface Temp (°F)", "YlOrRd", 80, 92),
        "Green Space": ("GREENSPACE", "Green Space (%)", "Greens", 0, 70),
        "Air Conditioning Access": ("PCT_HOUSEHOLDS_AC", "Households w/ AC (%)", "Blues", 75, 100)
    }
    map_metric = st.selectbox("Select metric:", list(metric_options.keys()))

col_name, display_name, colormap, min_val, max_val = metric_options[map_metric]

# Color function
def get_color(value, min_v, max_v, colormap_name):
    if value is None:
        return '#cccccc'
    normalized = (value - min_v) / (max_v - min_v) if max_v > min_v else 0.5
    normalized = max(0, min(1, normalized))
    
    color_scales = {
        "YlOrRd": ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026'],
        "Greens": ['#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c'],
        "Blues": ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c']
    }
    colors = color_scales.get(colormap_name, color_scales["YlOrRd"])
    idx = min(int(normalized * len(colors)), len(colors) - 1)
    return colors[idx]

# Borough name mapping
name_mapping = {
    'Manhattan': 'Manhattan', 'New York': 'Manhattan',
    'Bronx': 'Bronx', 'The Bronx': 'Bronx',
    'Brooklyn': 'Brooklyn', 'Kings': 'Brooklyn',
    'Queens': 'Queens', 'Staten Island': 'Staten Island', 'Richmond': 'Staten Island'
}

# Create map
m = folium.Map(location=[40.7128, -73.95], zoom_start=10, tiles='cartodbpositron')

if view_level == "Borough":
    borough_geojson = load_nyc_borough_geojson()
    if borough_geojson and 'features' in borough_geojson:
        data_lookup = borough_data.set_index('Borough')[col_name].to_dict()
        
        for feature in borough_geojson['features']:
            boro_name = feature['properties'].get('boro_name', '')
            normalized_name = name_mapping.get(boro_name, name_mapping.get(boro_name.title(), boro_name))
            value = data_lookup.get(normalized_name)
            if value is not None:
                feature['properties']['metric_value'] = f"{value:.1f}" if col_name in ['HVI_RANK', 'SURFACE_TEMP'] else f"{value:.1f}%"
            else:
                feature['properties']['metric_value'] = "N/A"
        
        def style_function(feature):
            boro_name = feature['properties'].get('boro_name', '')
            normalized_name = name_mapping.get(boro_name, name_mapping.get(boro_name.title(), boro_name))
            value = data_lookup.get(normalized_name)
            return {'fillColor': get_color(value, min_val, max_val, colormap), 'color': '#555', 'weight': 2, 'fillOpacity': 0.7}
        
        folium.GeoJson(
            borough_geojson,
            style_function=style_function,
            highlight_function=lambda x: {'weight': 3, 'color': '#333', 'fillOpacity': 0.9},
            tooltip=folium.GeoJsonTooltip(
                fields=['boro_name', 'metric_value'],
                aliases=['Borough:', f'{display_name}:'],
                style="font-size: 13px; padding: 8px;"
            )
        ).add_to(m)
else:
    nta_geojson = load_nta_geojson()
    if nta_geojson and 'features' in nta_geojson:
        data_lookup = hvi_data.set_index('NTACode')[col_name].to_dict()
        name_lookup = hvi_data.set_index('NTACode')['GEONAME'].to_dict()
        
        first_props = nta_geojson['features'][0]['properties']
        nta_key = next((k for k in ['nta2020', 'ntacode', 'NTACode'] if k in first_props), None)
        
        if nta_key:
            for feature in nta_geojson['features']:
                nta_code = feature['properties'].get(nta_key, '')
                value = data_lookup.get(nta_code)
                nta_name = feature['properties'].get('ntaname', name_lookup.get(nta_code, nta_code))
                feature['properties']['nta_name'] = nta_name
                if value is not None:
                    feature['properties']['metric_value'] = f"{value:.1f}" if col_name in ['HVI_RANK', 'SURFACE_TEMP'] else f"{value:.1f}%"
                else:
                    feature['properties']['metric_value'] = "N/A"
            
            def style_function_nta(feature):
                nta_code = feature['properties'].get(nta_key, '')
                value = data_lookup.get(nta_code)
                return {'fillColor': get_color(value, min_val, max_val, colormap), 'color': '#888', 'weight': 0.5, 'fillOpacity': 0.7}
            
            folium.GeoJson(
                nta_geojson,
                style_function=style_function_nta,
                highlight_function=lambda x: {'weight': 2, 'color': '#333', 'fillOpacity': 0.9},
                tooltip=folium.GeoJsonTooltip(
                    fields=['nta_name', 'metric_value'],
                    aliases=['Neighborhood:', f'{display_name}:'],
                    style="font-size: 12px; padding: 6px;"
                )
            ).add_to(m)

# Legend
color_scales = {
    "YlOrRd": ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026'],
    "Greens": ['#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c'],
    "Blues": ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c']
}
colors = color_scales.get(colormap, color_scales["YlOrRd"])

st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center; margin: 16px 0; gap: 8px;">
    <span style="font-size: 0.85rem; color: #666;">Low</span>
    {"".join([f'<div style="width: 30px; height: 20px; background: {c}; border: 1px solid #ccc;"></div>' for c in colors])}
    <span style="font-size: 0.85rem; color: #666;">High</span>
    <span style="font-size: 0.85rem; color: #333; margin-left: 16px; font-weight: 600;">{display_name}</span>
</div>
""", unsafe_allow_html=True)

st_folium(m, width=None, height=450, use_container_width=True)

# Borough averages
st.markdown(f"**Borough Averages — {display_name}**")
cols = st.columns(5)
ascending = col_name in ['GREENSPACE', 'PCT_HOUSEHOLDS_AC']
sorted_borough = borough_data.sort_values(col_name, ascending=ascending)
for i, (_, row) in enumerate(sorted_borough.iterrows()):
    value = row[col_name]
    formatted = f"{value:.1f}" if col_name in ['HVI_RANK', 'SURFACE_TEMP'] else f"{value:.1f}%"
    with cols[i]:
        st.metric(row['Borough'], formatted)

if view_level == "Neighborhood (NTA)":
    st.markdown("---")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f"**Highest {display_name}**")
        top_5 = hvi_data.nlargest(5, col_name)[['GEONAME', 'Borough', col_name]]
        for _, row in top_5.iterrows():
            val = f"{row[col_name]:.1f}" if col_name in ['HVI_RANK', 'SURFACE_TEMP'] else f"{row[col_name]:.1f}%"
            st.caption(f"{row['GEONAME']} ({row['Borough']}): **{val}**")
    
    with col_right:
        st.markdown(f"**Lowest {display_name}**")
        bottom_5 = hvi_data.nsmallest(5, col_name)[['GEONAME', 'Borough', col_name]]
        for _, row in bottom_5.iterrows():
            val = f"{row[col_name]:.1f}" if col_name in ['HVI_RANK', 'SURFACE_TEMP'] else f"{row[col_name]:.1f}%"
            st.caption(f"{row['GEONAME']} ({row['Borough']}): **{val}**")

st.caption("""
**Data Source:** [NYC DOHMH Environment & Health Data Portal](https://github.com/nychealth/EHDP-data) — 
Heat Vulnerability Index 2020
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">Research Findings</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Temperature Disparities Today</p>', unsafe_allow_html=True)

st.markdown("""
[Hoffman, Shandas, and Pendleton (2020)](https://www.mdpi.com/2225-1154/8/1/12) analyzed 108 U.S. 
cities and found that **94% of formerly redlined neighborhoods are now measurably hotter** than 
surrounding areas, with an average difference of 4.7°F. 

In NYC, [NYSERDA (2024)](https://www.nyserda.ny.gov/Featured-Stories/Protecting-New-Yorkers-from-Extreme-Heat) 
reports a gap of nearly **6°F between D-graded and A-graded neighborhoods**. Decades of reduced 
investment resulted in fewer trees, more impervious surfaces, and less green infrastructure.
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">Comparative Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">HOLC Grade A vs. Grade D Today</p>', unsafe_allow_html=True)

st.caption("*NYC data from NYSERDA; national averages from Hoffman et al. (2020)*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Grade A — 'Best' Rated")
    st.metric("Temperature vs. NYC Average", "-4.2°F", help="NYSERDA 2024")
    st.metric("Tree Canopy Coverage", "~30%")
    st.metric("Green Space Access", "Higher")

with col2:
    st.markdown("#### Grade D — 'Hazardous' Rated")
    st.metric("Temperature vs. NYC Average", "+1.6°F", help="NYSERDA 2024")
    st.metric("Tree Canopy Coverage", "~10%")
    st.metric("Green Space Access", "Lower")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">Health Impact</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Heat-Related Health Disparities</p>', unsafe_allow_html=True)

st.markdown("""
Heat-related mortality is concentrated in specific populations and neighborhoods. The 
[NYC Panel on Climate Change 4th Assessment (2024)](https://climateassessment.nyc/wp-content/uploads/2024/04/NPCC4_HealthInterimR2.pdf) reports that 
**Black New Yorkers die from heat stress at twice the rate of white New Yorkers**. This is a direct result of historical redlining practices and increasing heat vulnerability.  
""")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">At-Risk Groups</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Populations Most Vulnerable to Extreme Heat</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **Older Adults**
    
    Adults are most vulnerable to heat-related deaths. Reduced thermoregulation and chronic 
    conditions increase risk. 
    """)

with col2:
    st.markdown("""
    **Low-Income Households**
    
    Cost barriers limit AC use. Many choose between cooling and other necessities like food 
    or medication.
    """)

with col3:
    st.markdown("""
    **Chronic Conditions**
    
    Heat exacerbates cardiovascular disease, respiratory illness, diabetes, and mental health 
    conditions.
    """)

with col4:
    st.markdown("""
    **Outdoor Workers**
    
    Construction, delivery, and sanitation workers face prolonged exposure with limited ability 
    to seek relief.
    """)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
**Sources:**
- [Hoffman, Shandas & Pendleton (2020)](https://www.mdpi.com/2225-1154/8/1/12) — "The Effects of Historical Housing Policies on Resident Exposure to Intra-Urban Heat," *Climate* 8(1)
- [NYSERDA (2024)](https://www.nyserda.ny.gov/Featured-Stories/Protecting-New-Yorkers-from-Extreme-Heat) — "Protecting New Yorkers from Extreme Heat"
- [NYC Panel on Climate Change 4th Assessment](https://climateassessment.nyc/wp-content/uploads/2024/04/NPCC4_HealthInterimR2.pdf) — NPCC4, 2024
- [NYC Gov](https://a816-dohbesp.nyc.gov/IndicatorPublic/data-features/heat-report/) — "2025 NYC Heat-Related Mortality Report"
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Explore UHI Effect", use_container_width=True):
        st.switch_page("pages/1_Explore_UHI.py")
with col3:
    if st.button("Mitigations & Solutions →", use_container_width=True):
        st.switch_page("pages/3_Mitigations_and_Solutions.py")