import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Mitigations & Solutions | NYC",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Data
@st.cache_data
def get_solution_effectiveness():
    """
    Cooling effectiveness of interventions.
    Sources: EPA Heat Island Mitigation; Cool Neighborhoods NYC Report
    """
    return pd.DataFrame({
        'Intervention': ['Urban Trees', 'Green Roofs', 'Cool Roofs', 'Parks & Open Space', 'Cool Pavement'],
        'Cooling Effect': ['20-45°F (surface)', '6-8°F', '5-7°F', '2-4°F', '2-4°F'],
        'Co-Benefits': ['Air quality, stormwater, carbon', 'Stormwater, insulation, habitat', 
                       'Energy savings, reduced emissions', 'Recreation, mental health', 'Reduced runoff'],
        'Implementation': ['5-15 years maturity', '1-2 years', '< 1 year', '3-5 years', '< 1 year']
    })

# CSS with green theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #f0fff4 0%, #e6ffed 50%, #dcfce7 100%);
    }
    
    [data-testid="stSidebar"] {
        background: #f5fff8;
        border-right: 1px solid #d1fae5;
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
        color: #16a34a;
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

# Navigation
if st.button("← Back to Overview", type="secondary"):
    st.switch_page("app.py")

# Header
st.markdown('<p class="section-label">03 / Solutions</p>', unsafe_allow_html=True)
st.markdown('<h1 class="page-header">Mitigation Strategies and NYC Initiatives</h1>', unsafe_allow_html=True)
st.markdown("""
<p class="page-subtitle">
Urban heat islands can be mitigated through targeted infrastructure investments. The 
<a href="https://www.epa.gov/heatislands" target="_blank">EPA</a> documents that trees, cool roofs, 
and vegetation reduce local temperatures significantly. A 
<a href="https://www.sciencedirect.com/science/article/pii/S2210670721008301" target="_blank">study of 601 European cities</a> 
found that green areas cool cities by <strong>2°F on average, and up to 5°F</strong>. NYC has committed to achieving 
<strong>net zero emissions by 2050</strong> and has implemented several preparedness actions to 
address the increasing risk of heat events.
</p>
""", unsafe_allow_html=True)

# Key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tree Canopy Goal", "30% by 2035", help="NYC Urban Forest Agenda target")
with col2:
    st.metric("Climate Target", "Net Zero 2050", help="NYC's carbon neutrality commitment")
with col3:
    st.metric("Green Area Cooling", "2-5°F avg", help="European cities study average cooling effect")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# NYC Programs
st.markdown('<p class="section-label">NYC Initiatives</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Active Cooling Programs</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **[NYC Urban Forest Agenda](https://forestforall.nyc/nyc-urban-forest-agenda/)**
    
    30% canopy cover by 2035
    
    The Forest for All NYC coalition has established an Urban Forest Agenda with three key goals: 
    achieve 30% canopy cover by 2035, support development of community-scale urban forest plans, 
    and establish a master plan for the urban forest. Trees provide critical cooling—shaded surfaces 
    are 20-45°F cooler than unshaded surfaces.
    
    ---
    
    **[Cool Neighborhoods NYC](https://www.nyc.gov/assets/orr/pdf/Cool_Neighborhoods_NYC_Report.pdf)**
    
    8 priority neighborhoods • $106M investment
    
    Comprehensive cooling in highest-vulnerability areas: trees, cool roofs, cooling centers. 
    Evapotranspiration alone or with shading can reduce peak temperatures by 2-9°F.
    """)

with col2:
    st.markdown("""
    **[NYC CoolRoofs](https://nyc-business.nyc.gov/nycbusiness/business-services/incentives/nyc-coolroofs)**
    
    Free reflective coating program
    
    NYC CoolRoofs applies reflective coating to rooftops at no cost to building owners. The program 
    serves as a workforce development opportunity, training local individuals to coat rooftops 
    while earning construction sector credentials. Part of NYC's pathway to net zero by 2050.
    """)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Equity focus
st.markdown('<p class="section-label">Equity Focus</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Prioritizing High-Vulnerability Communities</p>', unsafe_allow_html=True)

st.markdown("""
NYC uses the [Heat Vulnerability Index](https://a816-dohbesp.nyc.gov/IndicatorPublic/data-explorer/climate/?id=2411#display=summary) 
to direct cooling investments to neighborhoods with the highest heat-related health risks. 
Cool Neighborhoods NYC allocates $106 million to tackle heat vulnerability.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Target Areas**
    
    Hunts Point, Mott Haven, Highbridge, Brownsville, East New York, Bushwick, East Harlem, 
    Jamaica—selected based on HVI scores and heat-related mortality data.
    """)

with col2:
    st.markdown("""
    **Tree Equity**
    
    NYC Parks uses a [Tree Equity Score](https://www.treeequityscore.org/) to guide planting, 
    prioritizing areas with lowest canopy, highest poverty, and greatest heat exposure.
    """)

with col3:
    st.markdown("""
    **AC Access Programs**
    
    [HEAP Cooling Assistance](https://otda.ny.gov/programs/heap/) provides free air conditioners 
    to income-eligible households. Cooling centers open during heat emergencies.
    """)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Resources
st.markdown('<p class="section-label">Resources</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Programs and Applications</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Building Owners**
    - [NYC CoolRoofs](https://nyc-business.nyc.gov/nycbusiness/business-services/incentives/nyc-coolroofs) — Free roof coating
    - [Green Roof Tax Abatement](https://www.nyc.gov/site/finance/property/landlords-green-roof.page) — 10 USD per sq ft
    - [PACE Financing](https://www.nyserda.ny.gov/All-Programs/Commercial-Property-Assessed-Clean-Energy-PACE-Financing-Resources) — Clean energy loans
    """)

with col2:
    st.markdown("""
    **Residents**
    - [HEAP Cooling Assistance](https://otda.ny.gov/programs/heap/) — Free AC units
    - [Cooling Center Finder](https://finder.nyc.gov/coolingcenters/) — Locate nearby centers
    - [Con Edison Assistance](https://www.coned.com/en/accounts-billing/payment-plans-assistance) — Rate programs
    """)

with col3:
    st.markdown("""
    **Further Reading**
    - [Heat Vulnerability Index](https://a816-dohbesp.nyc.gov/IndicatorPublic/data-explorer/climate/?id=2411#display=summary) — NYC DOHMH
    - [Cool Neighborhoods NYC Report](https://www.nyc.gov/assets/orr/pdf/Cool_Neighborhoods_NYC_Report.pdf)
    - [PlaNYC](https://www.nyc.gov/content/climate/pages/planyc-getting-sustainabilty-done)
    """)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
**Sources:**
- [Cooling effects of urban green areas (2022)](https://www.sciencedirect.com/science/article/pii/S2210670721008301) — Study of 601 European cities, *Sustainable Cities and Society*
- [Cool Neighborhoods NYC Report](https://www.nyc.gov/assets/orr/pdf/Cool_Neighborhoods_NYC_Report.pdf) — NYC Mayor's Office of Resiliency
- [NYC Urban Forest Agenda](https://forestforall.nyc/nyc-urban-forest-agenda/) — Forest for All NYC
- [EPA Heat Islands](https://www.epa.gov/heatislands) — U.S. Environmental Protection Agency
- [NYC Green Roof Tax Abatement](https://www.nyc.gov/site/finance/property/landlords-green-roof.page) — NYC Department of Finance
""")

# Navigation
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Inequality & UHI", use_container_width=True):
        st.switch_page("pages/2_Inequality_and_UHI.py")
with col3:
    if st.button("Back to Overview →", use_container_width=True):
        st.switch_page("app.py")