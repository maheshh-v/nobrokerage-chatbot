import streamlit as st
import pandas as pd
from query_parser import parse_query
from search_engine import search_properties
from summary_generator import generate_summary

st.set_page_config(page_title="NoBrokerage Property Search", layout="wide")

# Dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .stChatMessage {
        background-color: #1e2530 !important;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 15px;
    }
    [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] {
        background-color: #262c36;
        border: 1px solid #3d4451;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #e2e8f0 !important;
    }
    .stMarkdown {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    project = pd.read_csv("data/project.csv")
    address = pd.read_csv("data/ProjectAddress.csv")
    config = pd.read_csv("data/ProjectConfiguration.csv")
    variant = pd.read_csv("data/ProjectConfigurationVariant.csv")
    
    df = project.merge(address, left_on="id", right_on="projectId", how="left", suffixes=('', '_addr'))
    df = df.merge(config, left_on="id", right_on="projectId", how="left", suffixes=('', '_config'))
    df = df.merge(variant, left_on="id_config", right_on="configurationId", how="left", suffixes=('', '_variant'))
    
    return df

if "messages" not in st.session_state:
    st.session_state.messages = []

# UI
st.title("NoBrokerage Property Search")
st.caption("Type what you're looking for")

# Sidebar
with st.sidebar:
    st.header("Try these")
    st.markdown("""
    - 2BHK in Mumbai
    - 3BHK in Pune under 2 Cr
    - Properties in Chembur
    """)
    
    st.markdown("---")
    st.markdown("Built by Mahesh for NoBrokerage")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("e.g., 2BHK in Mumbai"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process query
    with st.chat_message("assistant"):
        df = load_data()
        filters = parse_query(prompt)
        
        # Check if property related
        keywords = ['bhk', 'flat', 'apartment', 'property', 'house', 'pune', 'mumbai', 'cr', 'lakh']
        is_property = any(k in prompt.lower() for k in keywords)
        
        if not is_property and not filters:
            msg = "I only search for properties. Please ask like: '2BHK in Mumbai' or '3BHK in Pune under 2 Cr'"
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            results = search_properties(df, filters)
            
            if len(results) > 0:
                # Sort by price
                results = results.sort_values('price', ascending=True)
                
                # Show summary
                summary = generate_summary(results, filters)
                st.markdown(summary)
                
                st.markdown("---")
                st.markdown(f"**{len(results)} results**")
                
                # Show cards in pairs
                for i in range(0, len(results), 2):
                    cols = st.columns(2)
                    
                    # First card
                    row = results.iloc[i]
                    with cols[0]:
                        with st.container(border=True):
                            st.markdown(f"### {row['projectName']}")
                            
                            # Location
                            city = 'Pune' if 'pune' in str(row.get('fullAddress', '')).lower() else 'Mumbai'
                            addr = str(row.get('fullAddress', 'N/A')).split(',')[0]
                            st.markdown(f"**Location:** {addr}, {city}")
                            
                            # Type
                            st.markdown(f"**Type:** {row.get('type', 'N/A')}")
                            
                            # Price
                            price = row.get('price', 0)
                            if price and str(price) != 'nan':
                                try:
                                    p = float(price)
                                    if p >= 10000000:
                                        st.markdown(f"**Price:** ₹{p/10000000:.2f} Cr")
                                    else:
                                        st.markdown(f"**Price:** ₹{p/100000:.0f} L")
                                except:
                                    pass
                            
                            # Status
                            status = row.get('status', '')
                            if status == 'READY_TO_MOVE':
                                st.markdown("**Status:** Ready to Move")
                            else:
                                st.markdown("**Status:** Under Construction")
                            
                            # Area
                            area = row.get('carpetArea', '')
                            if area and str(area) != 'nan':
                                st.markdown(f"**Area:** {area} sq.ft")
                            
                            # Amenities
                            amenities = []
                            balcony = row.get('balcony', '')
                            if balcony and str(balcony) != 'nan':
                                amenities.append(f"{int(float(balcony))} Balcony")
                            
                            furn = row.get('furnishedType', '')
                            if furn and str(furn) != 'nan' and furn != 'UNFURNISHED':
                                amenities.append(str(furn).replace('_', ' ').title())
                            
                            if row.get('parkingType') and str(row.get('parkingType')) != 'nan':
                                amenities.append("Parking")
                            
                            if amenities:
                                st.markdown(f"**Amenities:** {', '.join(amenities[:3])}")
                            
                            # Link
                            slug = row.get('slug', '')
                            if slug:
                                st.link_button("View Details", f"https://nobrokerage.com/project/{slug}", use_container_width=True)
                    
                    # Second card (if exists)
                    if i + 1 < len(results):
                        row = results.iloc[i + 1]
                        with cols[1]:
                            with st.container(border=True):
                                st.markdown(f"### {row['projectName']}")
                                
                                city = 'Pune' if 'pune' in str(row.get('fullAddress', '')).lower() else 'Mumbai'
                                addr = str(row.get('fullAddress', 'N/A')).split(',')[0]
                                st.markdown(f"**Location:** {addr}, {city}")
                                
                                st.markdown(f"**Type:** {row.get('type', 'N/A')}")
                                
                                price = row.get('price', 0)
                                if price and str(price) != 'nan':
                                    try:
                                        p = float(price)
                                        if p >= 10000000:
                                            st.markdown(f"**Price:** ₹{p/10000000:.2f} Cr")
                                        else:
                                            st.markdown(f"**Price:** ₹{p/100000:.0f} L")
                                    except:
                                        pass
                                
                                status = row.get('status', '')
                                if status == 'READY_TO_MOVE':
                                    st.markdown("**Status:** Ready to Move")
                                else:
                                    st.markdown("**Status:** Under Construction")
                                
                                area = row.get('carpetArea', '')
                                if area and str(area) != 'nan':
                                    st.markdown(f"**Area:** {area} sq.ft")
                                
                                amenities = []
                                balcony = row.get('balcony', '')
                                if balcony and str(balcony) != 'nan':
                                    amenities.append(f"{int(float(balcony))} Balcony")
                                
                                furn = row.get('furnishedType', '')
                                if furn and str(furn) != 'nan' and furn != 'UNFURNISHED':
                                    amenities.append(str(furn).replace('_', ' ').title())
                                
                                if row.get('parkingType') and str(row.get('parkingType')) != 'nan':
                                    amenities.append("Parking")
                                
                                if amenities:
                                    st.markdown(f"**Amenities:** {', '.join(amenities[:3])}")
                                
                                slug = row.get('slug', '')
                                if slug:
                                    st.link_button("View Details", f"https://nobrokerage.com/project/{slug}", use_container_width=True)
                
                st.session_state.messages.append({"role": "assistant", "content": summary})
            else:
                msg = "No properties found. Try different search terms."
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
