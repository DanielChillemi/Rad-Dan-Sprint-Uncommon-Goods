
import streamlit as st

# Hard-coded trends data
trends_data = [
    {
        "name": "Mushroom Decor",
        "velocity": 9.8,
        "description": "A rising interest in fungi-inspired home goods, from lamps to textiles.",
        "evidence": [
            "The Hottest Home Trend Is Fungi-Inspired Decor - DesignDigest.com",
            "Why Everyone is Buying Mushroom Lamps for a Whimsical Vibe - ApartmentInspo.net",
            "Pinterest Trends Report shows 350% increase in searches for 'Mushroom Art'",
            "Etsy Bestsellers: Hand-carved Wooden Mushroom Figurines"
        ]
    },
    {
        "name": "Checkered Patterns",
        "velocity": 8.1,
        "description": "The classic checkerboard pattern is seeing a major resurgence in rugs, blankets, and ceramics.",
        "evidence": [
            "Checkmate: The Enduring Appeal of the Checkerboard - StyleWeekly.com",
            "TikTok #CheckeredRug hashtag surpasses 10 million views",
            "Spotted: Checkered Patterns on ceramics at the NY Now Trade Show"
        ]
    },
    {
        "name": "Craft Cocktail Kits",
        "velocity": 7.5,
        "description": "DIY kits for creating unique, high-quality cocktails at home.",
        "evidence": [
            "The Rise of the Home Mixologist: Best Cocktail Kits of 2025 - GQ Magazine",
            "Review: A kit for smoking your own cocktails at home - TheVerge.com",
            "Internal Search Data: High search volume for 'cocktail smoker' and 'artisan bitters'"
        ]
    }
]

# Initialize session state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'
if 'selected_trend' not in st.session_state:
    st.session_state.selected_trend = None

# App title and subtitle
st.title("Artisan Trend Spotter")
st.subheader("Internal Curation Team Dashboard")

# Main Dashboard View
if st.session_state.current_view == 'dashboard':
    st.write("---")
    
    for trend in trends_data:
        # Create columns for better layout
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.subheader(trend["name"])
            st.write(trend["description"])
        
        with col2:
            st.metric("Trend Velocity", f"{trend['velocity']}")
        
        with col3:
            if st.button("View Details", key=f"details_{trend['name']}"):
                st.session_state.current_view = 'detail'
                st.session_state.selected_trend = trend
                st.rerun()
        
        st.write("---")

# Detail View
elif st.session_state.current_view == 'detail' and st.session_state.selected_trend:
    trend = st.session_state.selected_trend
    
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.current_view = 'dashboard'
        st.session_state.selected_trend = None
        st.rerun()
    
    st.write("---")
    
    # Trend details
    st.header(trend["name"])
    st.write(trend["description"])
    
    st.subheader("Supporting Evidence")
    
    for evidence in trend["evidence"]:
        st.info(evidence)
