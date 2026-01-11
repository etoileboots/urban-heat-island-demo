import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Explore UHI | NYC",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def get_hourly_uhi_data():
    """
    Hourly temperature data for NYC UHI.
    Source: Gedzelman et al. (2003)
    """
    data = {
        0:  {'urban': 79, 'rural': 68, 'diff': 11},
        1:  {'urban': 78, 'rural': 67, 'diff': 11},
        2:  {'urban': 77, 'rural': 66, 'diff': 11},
        3:  {'urban': 76, 'rural': 65, 'diff': 11},
        4:  {'urban': 75, 'rural': 64, 'diff': 11},
        5:  {'urban': 74, 'rural': 63, 'diff': 11},
        6:  {'urban': 75, 'rural': 65, 'diff': 10},
        7:  {'urban': 77, 'rural': 69, 'diff': 8},
        8:  {'urban': 80, 'rural': 73, 'diff': 7},
        9:  {'urban': 83, 'rural': 77, 'diff': 6},
        10: {'urban': 85, 'rural': 80, 'diff': 5},
        11: {'urban': 87, 'rural': 82, 'diff': 5},
        12: {'urban': 89, 'rural': 84, 'diff': 5},
        13: {'urban': 90, 'rural': 85, 'diff': 5},
        14: {'urban': 91, 'rural': 86, 'diff': 5},
        15: {'urban': 91, 'rural': 85, 'diff': 6},
        16: {'urban': 90, 'rural': 84, 'diff': 6},
        17: {'urban': 89, 'rural': 82, 'diff': 7},
        18: {'urban': 87, 'rural': 79, 'diff': 8},
        19: {'urban': 85, 'rural': 76, 'diff': 9},
        20: {'urban': 83, 'rural': 73, 'diff': 10},
        21: {'urban': 82, 'rural': 71, 'diff': 11},
        22: {'urban': 81, 'rural': 70, 'diff': 11},
        23: {'urban': 80, 'rural': 69, 'diff': 11},
    }
    return data

# Albedo data from Hood College Urban Heat Studies
ALBEDO_SURFACES = {
    "Urban Surfaces": {
        "Fresh Asphalt": {"albedo": 0.04, "color": "#1a1a1a"},
        "Worn Asphalt": {"albedo": 0.12, "color": "#4a4a4a"},
        "Black Roof": {"albedo": 0.08, "color": "#2d2d2d"},
        "Red Brick": {"albedo": 0.36, "color": "#b35c44"},
        "Concrete": {"albedo": 0.55, "color": "#a8a8a8"},
    },
    "Natural Surfaces": {
        "Bare Soil": {"albedo": 0.17, "color": "#8b6914"},
        "Green Grass": {"albedo": 0.25, "color": "#4a7c23"},
        "Deciduous Trees": {"albedo": 0.17, "color": "#2d5a1d"},
        "Desert Sand": {"albedo": 0.40, "color": "#d4b896"},
        "Water": {"albedo": 0.06, "color": "#1e5f8a"},
    },
    "High-Albedo (Cool)": {
        "White Roof": {"albedo": 0.72, "color": "#e8e8e8"},
        "Fresh Snow": {"albedo": 0.85, "color": "#f5f5f5"},
    },
}

ALL_SURFACES = {}
for category, surfaces in ALBEDO_SURFACES.items():
    for name, data in surfaces.items():
        ALL_SURFACES[name] = {**data, "category": category}

# Contributing Factors Data
FACTORS = [
    {
        "title": "Albedo: The Reflectivity Factor",
        "content": """**Albedo** measures how much solar radiation a surface reflects versus absorbs, 
ranging from **0** (absorbs all) to **1** (reflects all).

You understand this intuitively: you avoid walking barefoot on blacktop because dark surfaces 
absorb more energy and get painfully hot.

Cities are full of low-albedo surfaces—asphalt, dark rooftops, brick—that absorb solar radiation 
and convert it to heat. This is the primary driver of urban heat islands.""",
        "stat_value": "0.04",
        "stat_label": "Fresh asphalt albedo (absorbs 96%)",
        "source": "Hood College Urban Heat Studies",
        "source_url": "https://www.hood.edu/sites/default/files/Coastal%20Studies/UHS/LessonPlans_ManualFiles/Surface_2%20Albedo%20%26%20Land%20Cover%20Temp%20Lab.pdf"
    },
    {
        "title": "Reduced Vegetation",
        "content": """Trees and vegetation cool cities through two mechanisms:

**Evapotranspiration** — Plants release water vapor, absorbing heat in the process.

**Shading** — Tree canopy blocks solar radiation from heating surfaces below.

Areas with substantial tree cover are **2-9°F cooler** than comparable areas without vegetation. 
NYC's tree canopy averages ~22%, but some neighborhoods have as little as 5%.""",
        "stat_value": "9°F",
        "stat_label": "Maximum cooling from tree canopy",
        "source": "Oke (1982), Q.J.R. Meteorol. Soc.",
        "source_url": "https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/qj.49710845502"
    },
    {
        "title": "Urban Canyon Effect",
        "content": """Tall buildings create **urban canyons** that trap heat:

**Reduced sky view** — Buildings block the sky, limiting nighttime heat escape.

**Multiple reflections** — Sunlight bounces between walls, absorbing more energy each time.

**Reduced airflow** — Canyon geometry blocks cooling winds.

This is why Midtown Manhattan stays hot after sunset—stored heat has nowhere to go.""",
        "stat_value": None,
        "stat_label": None,
        "source": "EPA Heat Islands",
        "source_url": "https://www.epa.gov/heatislands/what-are-heat-islands"
    },
    {
        "title": "Anthropogenic Heat",
        "content": """Cities generate heat through human activities:

**Vehicles** — Engines and exhaust release heat directly into the air.

**HVAC systems** — Air conditioners move heat from inside to outside.

**Industrial processes** — Factories and commercial kitchens emit waste heat.

In dense urban areas, anthropogenic heat adds additional warming on top of surface effects.""",
        "stat_value": None,
        "stat_label": None,
        "source": "EPA Heat Islands",
        "source_url": "https://www.epa.gov/heatislands/what-are-heat-islands"
    }
]

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
    
    /* Style the factor card container */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"] > div > div > .factor-card-marker) {
        background: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.04);
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Overview", type="secondary"):
    st.switch_page("app.py")

st.markdown('<p class="section-label">01 / Science</p>', unsafe_allow_html=True)
st.markdown('<h1 class="page-header">Understanding the Urban Heat Island Effect</h1>', unsafe_allow_html=True)
st.markdown("""
<p class="page-subtitle">
Anyone who has walked through New York City in the summer knows that it is <em>hot</em>. The phrase 
"walking in a sauna" just about covers the feeling of heat suffocating you from all sides. 
Know this feeling? Then you know of the Urban Heat Island (UHI).
</p>
""", unsafe_allow_html=True)

st.markdown("""
The UHI effect occurs when cities experience significantly higher temperatures than surrounding 
rural areas. A [2024 Climate Central study](https://www.climatecentral.org/climate-matters/urban-heat-islands-2024) 
found that New Yorkers feel this effect more than anywhere else in the U.S.—NYC averages **9.7°F 
warmer** than it would be without city-related conditions.
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if 'factor_slide' not in st.session_state:
    st.session_state.factor_slide = 0
if 'selected_surface' not in st.session_state:
    st.session_state.selected_surface = 'Fresh Asphalt'

st.markdown('<p class="section-label">Contributing Factors</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">What Creates Urban Heat Islands?</p>', unsafe_allow_html=True)
st.markdown("Urban heat islands form through multiple compounding factors. Navigate below to explore each.")

current = st.session_state.factor_slide
total = len(FACTORS)

# Navigation row
nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

with nav_col1:
    if st.button("← Previous", disabled=(current == 0), use_container_width=True, key="prev_factor"):
        st.session_state.factor_slide = max(0, current - 1)
        st.rerun()

with nav_col2:
    progress_html = "".join([
        f'<div style="flex: 1; height: 6px; background: {"#f97316" if i == current else "#e5e5e5"}; border-radius: 3px; margin: 0 2px;"></div>'
        for i in range(total)
    ])
    st.markdown(f'<div style="display: flex; align-items: center; padding: 12px 0;">{progress_html}</div>', unsafe_allow_html=True)

with nav_col3:
    if st.button("Next →", disabled=(current == total - 1), use_container_width=True, key="next_factor"):
        st.session_state.factor_slide = min(total - 1, current + 1)
        st.rerun()

# Factor card - using expander styling trick for unified block
factor = FACTORS[current]

# The entire factor in one styled container
factor_container = st.container(border=True)

with factor_container:
    # Header with title and counter
    header_col1, header_col2 = st.columns([5, 1])
    with header_col1:
        st.markdown(f"### {factor['title']}")
    with header_col2:
        st.markdown(f"""
        <div style="background: #fff8f0; color: #f97316; padding: 6px 12px; 
                    border-radius: 20px; font-size: 0.85rem; font-weight: 600; 
                    text-align: center; margin-top: 4px;">
            {current + 1} / {total}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Content
    st.markdown(factor['content'])
    
    st.markdown("---")
    
    # Stats row (only show if stat exists)
    if factor['stat_value']:
        stat_col, source_col = st.columns(2)
        with stat_col:
            st.metric(label=factor['stat_label'], value=factor['stat_value'])
        with source_col:
            st.markdown(f"**Source:** [{factor['source']}]({factor['source_url']})")
    else:
        st.markdown(f"**Source:** [{factor['source']}]({factor['source_url']})")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-label">Interactive</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Albedo Explorer: See How Surfaces Reflect Light</p>', unsafe_allow_html=True)

st.markdown("""
Select a surface material to see its albedo value and how much solar energy it absorbs versus reflects.
Data from [Hood College Urban Heat Studies](https://www.hood.edu/sites/default/files/Coastal%20Studies/UHS/LessonPlans_ManualFiles/Surface_2%20Albedo%20%26%20Land%20Cover%20Temp%20Lab.pdf).
""")

viz_col1, viz_col2 = st.columns([1, 1])

with viz_col1:
    category = st.selectbox("Surface Category", options=list(ALBEDO_SURFACES.keys()), key="albedo_category")
    surface_options = list(ALBEDO_SURFACES[category].keys())
    selected_surface = st.selectbox("Select Surface", options=surface_options, key="albedo_surface")
    
    surface_data = ALL_SURFACES[selected_surface]
    albedo = surface_data['albedo']
    absorbed = 1 - albedo
    
    st.markdown("##### Quick Reference")
    ref_data = []
    for cat, surfaces in ALBEDO_SURFACES.items():
        for name, data in surfaces.items():
            ref_data.append({
                "Surface": name,
                "Albedo": f"{data['albedo']:.0%}",
                "Heat Absorbed": f"{(1-data['albedo']):.0%}"
            })
    ref_df = pd.DataFrame(ref_data).sort_values("Albedo")
    st.dataframe(ref_df, use_container_width=True, hide_index=True, height=300)

with viz_col2:
    st.markdown(f"### {selected_surface}")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=albedo * 100,
        number={'suffix': '%', 'font': {'size': 48, 'family': 'DM Sans'}},
        title={'text': 'Reflectivity', 'font': {'size': 16, 'family': 'DM Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'ticksuffix': '%', 'tickfont': {'family': 'DM Sans'}},
            'bar': {'color': '#f97316'},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': '#ddd',
            'steps': [
                {'range': [0, 20], 'color': '#fee2e2'},
                {'range': [20, 40], 'color': '#fef3c7'},
                {'range': [40, 60], 'color': '#fef9c3'},
                {'range': [60, 80], 'color': '#d1fae5'},
                {'range': [80, 100], 'color': '#a7f3d0'}
            ],
        }
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    energy_col1, energy_col2 = st.columns(2)
    
    with energy_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%); 
                    border-radius: 12px; padding: 20px; text-align: center; color: white;">
            <div style="font-size: 2.2rem; font-weight: 700;">{absorbed*100:.0f}%</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">ABSORBED</div>
            <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 4px;">Converts to heat</div>
        </div>
        """, unsafe_allow_html=True)
    
    with energy_col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    border-radius: 12px; padding: 20px; text-align: center; color: white;">
            <div style="font-size: 2.2rem; font-weight: 700;">{albedo*100:.0f}%</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">REFLECTED</div>
            <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 4px;">Returns to space</div>
        </div>
        """, unsafe_allow_html=True)

st.info("""
**💡 The Urban Heat Island Connection**

Cities replace high-albedo natural surfaces (grass at 25%, trees at 17%) with low-albedo materials 
(asphalt at 4%, dark roofs at 8%). **Fresh asphalt absorbs 96% of sunlight** while grass reflects 
about 25%. This difference—across millions of square feet—is why cities are **6-10°F hotter** 
than surrounding areas.
""")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Next: Inequality & UHI →", use_container_width=True):
        st.switch_page("pages/2_Inequality_and_UHI.py")