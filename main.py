
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import json
import datetime
import numpy as np
from io import BytesIO
import hashlib

# Database setup
def init_database():
    conn = sqlite3.connect('trends.db')
    cursor = conn.cursor()
    
    # Create trends table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            velocity REAL NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT NOT NULL,
            evidence TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create velocity history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS velocity_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trend_name TEXT NOT NULL,
            velocity REAL NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'curator'
        )
    ''')
    
    conn.commit()
    conn.close()

def get_trends_from_db():
    conn = sqlite3.connect('trends.db')
    df = pd.read_sql_query("SELECT * FROM trends ORDER BY velocity DESC", conn)
    conn.close()
    
    if not df.empty:
        df['evidence'] = df['evidence'].apply(json.loads)
    
    return df

def save_trend_to_db(trend_data):
    conn = sqlite3.connect('trends.db')
    cursor = conn.cursor()
    
    evidence_json = json.dumps(trend_data['evidence'])
    
    cursor.execute('''
        INSERT OR REPLACE INTO trends 
        (name, velocity, category, status, description, evidence, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        trend_data['name'],
        trend_data['velocity'],
        trend_data['category'],
        trend_data['status'],
        trend_data['description'],
        evidence_json,
        datetime.datetime.now()
    ))
    
    # Record velocity history
    cursor.execute('''
        INSERT INTO velocity_history (trend_name, velocity)
        VALUES (?, ?)
    ''', (trend_data['name'], trend_data['velocity']))
    
    conn.commit()
    conn.close()

def populate_initial_data():
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
    
    conn = sqlite3.connect('trends.db')
    cursor = conn.cursor()
    
    for trend in trends_data:
        cursor.execute("SELECT COUNT(*) FROM trends WHERE name = ?", (trend['name'],))
        if cursor.fetchone()[0] == 0:
            save_trend_to_db(trend)
    
    conn.close()

def get_velocity_history(trend_name):
    conn = sqlite3.connect('trends.db')
    df = pd.read_sql_query(
        "SELECT * FROM velocity_history WHERE trend_name = ? ORDER BY recorded_at",
        conn, params=(trend_name,)
    )
    conn.close()
    return df

def authenticate_user(username, password):
    conn = sqlite3.connect('trends.db')
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    return user is not None

def create_user(username, password, role='curator'):
    conn = sqlite3.connect('trends.db')
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def export_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def export_to_json(df):
    return df.to_json(orient='records', indent=2)

# Initialize database and populate data
init_database()
populate_initial_data()

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
    .login-box {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        max-width: 400px;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'login'
if 'selected_trend' not in st.session_state:
    st.session_state.selected_trend = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Create default admin user
conn = sqlite3.connect('trends.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
if cursor.fetchone()[0] == 0:
    create_user('admin', 'password123', 'admin')
conn.close()

# Login View
if not st.session_state.authenticated:
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🎯 Artisan Trend Spotter")
    st.subheader("Please log in to continue")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", type="primary"):
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.current_view = 'dashboard'
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        with col2:
            st.info("Demo credentials:\n\nUsername: **admin**\nPassword: **password123**")
    
    with tab2:
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
        
        if st.button("Register", type="primary"):
            if reg_password != reg_password_confirm:
                st.error("Passwords don't match")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters")
            elif create_user(reg_username, reg_password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # App title and subtitle
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.current_view = 'login'
            st.rerun()
    
    with col2:
        st.title("🎯 Artisan Trend Spotter")
        st.subheader(f"Welcome back, {st.session_state.username}!")
    
    with col3:
        st.write("") # Spacer
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    if st.session_state.current_view in ['dashboard', 'analytics', 'manage']:
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
        
        with nav_col1:
            if st.button("📊 Dashboard", type="primary" if st.session_state.current_view == 'dashboard' else "secondary"):
                st.session_state.current_view = 'dashboard'
                st.rerun()
        
        with nav_col2:
            if st.button("📈 Analytics", type="primary" if st.session_state.current_view == 'analytics' else "secondary"):
                st.session_state.current_view = 'analytics'
                st.rerun()
        
        with nav_col3:
            if st.button("⚙️ Manage Trends", type="primary" if st.session_state.current_view == 'manage' else "secondary"):
                st.session_state.current_view = 'manage'
                st.rerun()
        
        with nav_col4:
            # Export functionality
            df = get_trends_from_db()
            if not df.empty:
                export_format = st.selectbox("Export:", ["None", "CSV", "JSON"])
                if export_format == "CSV":
                    csv_data = export_to_csv(df[['name', 'velocity', 'category', 'status', 'description']])
                    st.download_button(
                        "📥 Download CSV",
                        csv_data,
                        "trends_data.csv",
                        "text/csv"
                    )
                elif export_format == "JSON":
                    json_data = export_to_json(df[['name', 'velocity', 'category', 'status', 'description']])
                    st.download_button(
                        "📥 Download JSON",
                        json_data,
                        "trends_data.json",
                        "application/json"
                    )
    
    # Get data from database
    df = get_trends_from_db()
    
    # Main Dashboard View
    if st.session_state.current_view == 'dashboard':
        
        if df.empty:
            st.warning("No trends found in database.")
        else:
            # Search functionality
            search_term = st.text_input("🔍 Search trends...", placeholder="Enter keyword to search trends")
            
            # Filters and controls
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                sort_by = st.selectbox("Sort by:", ["Velocity (High to Low)", "Velocity (Low to High)", "Name (A-Z)", "Name (Z-A)", "Most Recent"])
            
            with col2:
                category_filter = st.selectbox("Filter by Category:", ["All"] + sorted(df['category'].unique().tolist()))
            
            with col3:
                status_filter = st.selectbox("Filter by Status:", ["All"] + sorted(df['status'].unique().tolist()))
            
            with col4:
                min_velocity = st.slider("Minimum Velocity:", 0.0, 10.0, 0.0, 0.1)
            
            # Apply filters
            filtered_df = df.copy()
            
            # Search filter
            if search_term:
                mask = (
                    filtered_df['name'].str.contains(search_term, case=False) |
                    filtered_df['description'].str.contains(search_term, case=False) |
                    filtered_df['category'].str.contains(search_term, case=False)
                )
                filtered_df = filtered_df[mask]
            
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
            elif sort_by == "Most Recent":
                filtered_df = filtered_df.sort_values('updated_at', ascending=False)
            
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
                        filtered_df.head(10), 
                        x='name', 
                        y='velocity',
                        color='status',
                        title="Top 10 Trends by Velocity",
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
                        st.caption(f"Last updated: {trend['updated_at']}")
                    
                    with col2:
                        st.metric("Trend Velocity", f"{trend['velocity']}")
                    
                    with col3:
                        if st.button("View Details", key=f"details_{trend['name']}"):
                            st.session_state.current_view = 'detail'
                            st.session_state.selected_trend = trend.to_dict()
                            st.rerun()
                    
                    st.markdown("---")
    
    # Analytics View
    elif st.session_state.current_view == 'analytics':
        st.header("📈 Advanced Analytics")
        
        if df.empty:
            st.warning("No data available for analytics.")
        else:
            # Trend predictions
            st.subheader("Trend Velocity Predictions")
            
            selected_trend = st.selectbox("Select trend for detailed analysis:", df['name'].tolist())
            
            if selected_trend:
                # Get velocity history
                history_df = get_velocity_history(selected_trend)
                
                if not history_df.empty:
                    # Create time series with some simulated historical data
                    dates = pd.date_range(end=datetime.datetime.now(), periods=30, freq='D')
                    current_velocity = df[df['name'] == selected_trend]['velocity'].iloc[0]
                    
                    # Simulate velocity history with some randomness
                    np.random.seed(hash(selected_trend) % 2**32)
                    base_trend = np.linspace(current_velocity * 0.7, current_velocity, 30)
                    noise = np.random.normal(0, 0.3, 30)
                    simulated_velocities = np.maximum(0, base_trend + noise)
                    
                    # Create prediction (simple linear extrapolation)
                    future_dates = pd.date_range(start=dates[-1] + pd.Timedelta(days=1), periods=14, freq='D')
                    trend_slope = (simulated_velocities[-1] - simulated_velocities[-7]) / 7
                    future_velocities = [simulated_velocities[-1] + trend_slope * i for i in range(1, 15)]
                    
                    # Plot
                    fig = go.Figure()
                    
                    # Historical data
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=simulated_velocities,
                        mode='lines+markers',
                        name='Historical Velocity',
                        line=dict(color='blue')
                    ))
                    
                    # Predictions
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=future_velocities,
                        mode='lines+markers',
                        name='Predicted Velocity',
                        line=dict(color='red', dash='dash')
                    ))
                    
                    fig.update_layout(
                        title=f'Velocity Trend Analysis: {selected_trend}',
                        xaxis_title='Date',
                        yaxis_title='Velocity',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Analytics insights
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Key Insights")
                        trend_direction = "upward" if trend_slope > 0 else "downward" if trend_slope < 0 else "stable"
                        st.write(f"• **Trend Direction**: {trend_direction.title()}")
                        st.write(f"• **Current Velocity**: {current_velocity}")
                        st.write(f"• **Predicted 2-week velocity**: {future_velocities[-1]:.1f}")
                        
                        volatility = np.std(simulated_velocities)
                        st.write(f"• **Volatility**: {'High' if volatility > 1 else 'Medium' if volatility > 0.5 else 'Low'}")
                    
                    with col2:
                        st.subheader("Competitive Analysis")
                        category_trends = df[df['category'] == df[df['name'] == selected_trend]['category'].iloc[0]]
                        rank = (category_trends['velocity'] > current_velocity).sum() + 1
                        st.write(f"• **Category Rank**: #{rank} of {len(category_trends)}")
                        
                        similar_trends = category_trends[category_trends['name'] != selected_trend].head(3)
                        st.write("• **Similar Trends**:")
                        for _, similar in similar_trends.iterrows():
                            st.write(f"  - {similar['name']} ({similar['velocity']:.1f})")
                
                else:
                    st.info("No historical data available for this trend.")
            
            # Category performance analysis
            st.markdown("---")
            st.subheader("Category Performance Analysis")
            
            category_stats = df.groupby('category').agg({
                'velocity': ['mean', 'max', 'count'],
                'status': lambda x: (x == 'Rising').sum()
            }).round(2)
            
            category_stats.columns = ['Avg Velocity', 'Max Velocity', 'Total Trends', 'Rising Trends']
            category_stats['Rising %'] = (category_stats['Rising Trends'] / category_stats['Total Trends'] * 100).round(1)
            
            st.dataframe(category_stats)
            
            # Market opportunity matrix
            fig_matrix = px.scatter(
                df,
                x='velocity',
                y=df.groupby('category')['velocity'].transform('count'),
                color='category',
                size='velocity',
                title='Market Opportunity Matrix',
                labels={'x': 'Trend Velocity', 'y': 'Category Competition Level'},
                hover_data=['name', 'status']
            )
            st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Manage Trends View
    elif st.session_state.current_view == 'manage':
        st.header("⚙️ Manage Trends")
        
        tab1, tab2 = st.tabs(["Add New Trend", "Edit Existing"])
        
        with tab1:
            st.subheader("Add New Trend")
            
            with st.form("add_trend_form"):
                new_name = st.text_input("Trend Name*")
                new_velocity = st.slider("Velocity", 0.0, 10.0, 5.0, 0.1)
                new_category = st.selectbox("Category", ["Home Decor", "Fashion", "Food & Beverage", "Technology", "Lifestyle"])
                new_status = st.selectbox("Status", ["Rising", "Stable", "Declining"])
                new_description = st.text_area("Description*")
                
                st.subheader("Evidence Sources")
                evidence_sources = []
                for i in range(4):
                    source = st.text_input(f"Evidence Source {i+1}", key=f"evidence_{i}")
                    if source:
                        evidence_sources.append(source)
                
                submitted = st.form_submit_button("Add Trend", type="primary")
                
                if submitted:
                    if new_name and new_description and evidence_sources:
                        new_trend = {
                            'name': new_name,
                            'velocity': new_velocity,
                            'category': new_category,
                            'status': new_status,
                            'description': new_description,
                            'evidence': evidence_sources
                        }
                        
                        try:
                            save_trend_to_db(new_trend)
                            st.success(f"Trend '{new_name}' added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding trend: {str(e)}")
                    else:
                        st.error("Please fill in all required fields and add at least one evidence source.")
        
        with tab2:
            st.subheader("Edit Existing Trends")
            
            if not df.empty:
                selected_trend_name = st.selectbox("Select trend to edit:", df['name'].tolist())
                
                if selected_trend_name:
                    trend_data = df[df['name'] == selected_trend_name].iloc[0]
                    
                    with st.form("edit_trend_form"):
                        edit_velocity = st.slider("Velocity", 0.0, 10.0, float(trend_data['velocity']), 0.1)
                        edit_status = st.selectbox("Status", ["Rising", "Stable", "Declining"], 
                                                 index=["Rising", "Stable", "Declining"].index(trend_data['status']))
                        edit_description = st.text_area("Description", value=trend_data['description'])
                        
                        submitted = st.form_submit_button("Update Trend", type="primary")
                        
                        if submitted:
                            updated_trend = {
                                'name': selected_trend_name,
                                'velocity': edit_velocity,
                                'category': trend_data['category'],
                                'status': edit_status,
                                'description': edit_description,
                                'evidence': trend_data['evidence']
                            }
                            
                            save_trend_to_db(updated_trend)
                            st.success(f"Trend '{selected_trend_name}' updated successfully!")
                            st.rerun()
            else:
                st.info("No trends available to edit.")
    
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
            
            if 'updated_at' in trend:
                st.caption(f"Last updated: {trend['updated_at']}")
        
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
        
        evidence_list = trend["evidence"] if isinstance(trend["evidence"], list) else json.loads(trend["evidence"])
        for i, evidence in enumerate(evidence_list, 1):
            st.info(f"**Source {i}:** {evidence}")
        
        # Historical velocity chart for this specific trend
        st.subheader("Velocity History")
        history_df = get_velocity_history(trend['name'])
        
        if not history_df.empty:
            fig_history = px.line(
                history_df,
                x='recorded_at',
                y='velocity',
                title=f"Velocity History for {trend['name']}"
            )
            st.plotly_chart(fig_history, use_container_width=True)
        else:
            st.info("No historical velocity data available for this trend.")
