
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Hard-coded trends data (expanded)
trends_data = [
    {
        "name": "Mushroom Decor",
        "velocity": 9.8,
        "category": "Home Decor",
        "status": "Rising",
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
        "category": "Home Decor",
        "status": "Rising",
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
        "category": "Food & Beverage",
        "status": "Rising",
        "description": "DIY kits for creating unique, high-quality cocktails at home.",
        "evidence": [
            "The Rise of the Home Mixologist: Best Cocktail Kits of 2025 - GQ Magazine",
            "Review: A kit for smoking your own cocktails at home - TheVerge.com",
            "Internal Search Data: High search volume for 'cocktail smoker' and 'artisan bitters'"
        ]
    },
    {
        "name": "Vintage Denim",
        "velocity": 6.9,
        "category": "Fashion",
        "status": "Stable",
        "description": "90s and early 2000s denim styles making a comeback with authentic vintage pieces.",
        "evidence": [
            "Gen Z is Obsessed with Y2K Denim - Vogue.com",
            "Vintage Levi's 501s selling for $200+ on Depop",
            "Instagram hashtag #vintagedenim reaches 2.3M posts"
        ]
    },
    {
        "name": "Sourdough Everything",
        "velocity": 6.2,
        "category": "Food & Beverage",
        "status": "Declining",
        "description": "The pandemic sourdough craze evolving into specialized products and flavors.",
        "evidence": [
            "Beyond Basic: Artisan Sourdough Flavors Take Off - Food & Wine",
            "Sourdough pizza crusts becoming restaurant standard",
            "Local bakeries report 40% increase in specialty sourdough sales"
        ]
    },
    {
        "name": "Maximalist Jewelry",
        "velocity": 8.7,
        "category": "Fashion",
        "status": "Rising",
        "description": "Bold, layered jewelry pieces that make a statement - the opposite of minimalism.",
        "evidence": [
            "Chunky Chains and Statement Earrings Rule 2025 - Harper's Bazaar",
            "TikTok jewelry hauls featuring 'more is more' philosophy viral",
            "Etsy searches for 'statement earrings' up 280%"
        ]
    },
    {
        "name": "Plant-Based Leather",
        "velocity": 7.8,
        "category": "Fashion",
        "status": "Rising",
        "description": "Innovative leather alternatives made from mushrooms, pineapple leaves, and other plants.",
        "evidence": [
            "Mushroom Leather is the Future of Fashion - Wired Magazine",
            "Major brands investing in pineapple leaf leather production",
            "Sustainability reports show 150% increase in plant-based material searches"
        ]
    },
    {
        "name": "Cottagecore Crafts",
        "velocity": 5.4,
        "category": "Home Decor",
        "status": "Declining",
        "description": "Handmade crafts inspired by rural, pastoral aesthetics - embroidery, pottery, knitting.",
        "evidence": [
            "The Cottagecore Aesthetic is Evolving - The Cut",
            "Pottery wheel sales remain elevated post-pandemic",
            "Hand-embroidered items trending on vintage marketplaces"
        ]
    }
]

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    .trend-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    .status-rising {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    .status-stable {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
    .status-declining {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'
if 'selected_trend' not in st.session_state:
    st.session_state.selected_trend = None

# App title and subtitle
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🎯 Artisan Trend Spotter")
st.subheader("Internal Curation Team Dashboard")
st.markdown('</div>', unsafe_allow_html=True)

# Create DataFrame for easier manipulation
df = pd.DataFrame(trends_data)

# Main Dashboard View
if st.session_state.current_view == 'dashboard':
    
    # Filters and controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sort_by = st.selectbox("Sort by:", ["Velocity (High to Low)", "Velocity (Low to High)", "Name (A-Z)", "Name (Z-A)"])
    
    with col2:
        category_filter = st.selectbox("Filter by Category:", ["All"] + sorted(df['category'].unique().tolist()))
    
    with col3:
        status_filter = st.selectbox("Filter by Status:", ["All"] + sorted(df['status'].unique().tolist()))
    
    with col4:
        min_velocity = st.slider("Minimum Velocity:", 0.0, 10.0, 0.0, 0.1)
    
    # Apply filters
    filtered_df = df.copy()
    
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    
    filtered_df = filtered_df[filtered_df['velocity'] >= min_velocity]
    
    # Apply sorting
    if sort_by == "Velocity (High to Low)":
        filtered_df = filtered_df.sort_values('velocity', ascending=False)
    elif sort_by == "Velocity (Low to High)":
        filtered_df = filtered_df.sort_values('velocity', ascending=True)
    elif sort_by == "Name (A-Z)":
        filtered_df = filtered_df.sort_values('name', ascending=True)
    elif sort_by == "Name (Z-A)":
        filtered_df = filtered_df.sort_values('name', ascending=False)
    
    # Dashboard metrics
    st.markdown("---")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trends", len(filtered_df))
    with col2:
        avg_velocity = filtered_df['velocity'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg Velocity", f"{avg_velocity:.1f}")
    with col3:
        rising_count = len(filtered_df[filtered_df['status'] == 'Rising'])
        st.metric("Rising Trends", rising_count)
    with col4:
        top_velocity = filtered_df['velocity'].max() if len(filtered_df) > 0 else 0
        st.metric("Top Velocity", f"{top_velocity}")
    
    # Charts
    if len(filtered_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Velocity chart
            fig_velocity = px.bar(
                filtered_df, 
                x='name', 
                y='velocity',
                color='status',
                title="Trend Velocity by Name",
                color_discrete_map={
                    'Rising': '#28a745',
                    'Stable': '#ffc107', 
                    'Declining': '#dc3545'
                }
            )
            fig_velocity.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_velocity, use_container_width=True)
        
        with col2:
            # Category distribution
            category_counts = filtered_df['category'].value_counts()
            fig_category = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Trends by Category"
            )
            fig_category.update_layout(height=400)
            st.plotly_chart(fig_category, use_container_width=True)
    
    st.markdown("---")
    
    # Display trends
    if len(filtered_df) == 0:
        st.warning("No trends match your current filters. Try adjusting the criteria.")
    else:
        for _, trend in filtered_df.iterrows():
            # Create columns for better layout
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.subheader(trend["name"])
                st.write(trend["description"])
                
                # Status badge
                status_class = f"status-{trend['status'].lower()}"
                st.markdown(f'<span class="{status_class}">{trend["status"]}</span> | Category: {trend["category"]}', unsafe_allow_html=True)
            
            with col2:
                st.metric("Trend Velocity", f"{trend['velocity']}")
            
            with col3:
                if st.button("View Details", key=f"details_{trend['name']}"):
                    st.session_state.current_view = 'detail'
                    st.session_state.selected_trend = trend.to_dict()
                    st.rerun()
            
            st.markdown("---")

# Detail View
elif st.session_state.current_view == 'detail' and st.session_state.selected_trend:
    trend = st.session_state.selected_trend
    
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.current_view = 'dashboard'
        st.session_state.selected_trend = None
        st.rerun()
    
    st.markdown("---")
    
    # Trend details
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(trend["name"])
        st.write(trend["description"])
        
        # Status and category
        status_class = f"status-{trend['status'].lower()}"
        st.markdown(f'<span class="{status_class}">{trend["status"]}</span>', unsafe_allow_html=True)
        st.write(f"**Category:** {trend['category']}")
    
    with col2:
        # Velocity gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = trend['velocity'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Trend Velocity"},
            delta = {'reference': 5.0},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgray"},
                    {'range': [5, 8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 8
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.subheader("Supporting Evidence")
    
    for i, evidence in enumerate(trend["evidence"], 1):
        st.info(f"**Source {i}:** {evidence}")
