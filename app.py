import streamlit as st
import mysql.connector
import pandas as pd

# Database Connection
@st.cache_resource
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="abcdefghijklmnopqrstuvwxyz",
            database="sportsradar",
            connection_timeout=10 
        )
        return conn  # Return the connection object if successful
    except mysql.connector.Error as e:
        st.error(f"MySQL Connection Failed: {e}")
        return None

def fetch_data(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()

# Sidebar Filters
st.sidebar.header("Filters")
year = st.sidebar.number_input("Year", min_value=2000, max_value=2025, value=2024)
week = st.sidebar.number_input("Week", min_value=1, max_value=52, value=48)
points_threshold = st.sidebar.slider("Filter by Minimum Points", 0, 5000, 0)
gender = st.sidebar.selectbox("Gender", ["men", "women", "both"])
rank_range = st.sidebar.slider("Rank Range", 1, 1000, (1, 100))
search_name = st.sidebar.text_input("Search Competitors")

# New Filters
category = st.sidebar.selectbox("Game Category", ["singles", "doubles", "mixed doubles", "all"])
complex_name = st.sidebar.text_input("Search Complex Name")

# Apply Filters Button
if st.sidebar.button("Apply Filters"):
    apply_filters = True
else:
    apply_filters = False

# Title
st.title("🎾Tennis Leaderboard & Insights")

# Fetch Summary Statistics
summary_query = """
    SELECT COUNT(DISTINCT cr.competitor_id) AS total_competitors,
           COUNT(DISTINCT c.country) AS total_countries,
           MAX(cr.points) AS highest_points
    FROM Competitors_Ranking cr
    JOIN Competitors c ON cr.competitor_id = c.competitor_id;
"""
summary = fetch_data(summary_query)

if summary and summary[0]:
    st.metric("Total Competitors", summary[0]['total_competitors'])
    st.metric("Total Countries", summary[0]['total_countries'])
    st.metric("Highest Points", summary[0]['highest_points'])
else:
    st.warning("No data available for summary statistics.")

if apply_filters:
    # Rankings Data
    st.subheader("🏅 Filtered Rankings")
    tennis_query = """
        SELECT c.name, cr.rank, cr.points, c.country
        FROM Competitors_Ranking cr
        JOIN Competitors c ON cr.competitor_id = c.competitor_id
        WHERE c.name LIKE %s AND cr.rank BETWEEN %s AND %s AND cr.points >= %s
        ORDER BY cr.points DESC, cr.rank ASC;
    """
    competitors = fetch_data(tennis_query, (f"%{search_name}%", rank_range[0], rank_range[1], points_threshold))
    if competitors:
        st.dataframe(pd.DataFrame(competitors), use_container_width=True)  # Full-width table
    else:
        st.info("No competitors found matching the criteria.")

    # Top 10 Competitors
    st.subheader("🏆 Top 10 Competitors")
    top_competitors_query = """
        SELECT c.name, cr.rank, cr.points, c.country
        FROM Competitors_Ranking cr
        JOIN Competitors c ON cr.competitor_id = c.competitor_id
        ORDER BY cr.rank ASC LIMIT 10;
    """
    top_competitors = fetch_data(top_competitors_query)
    if top_competitors:
        st.dataframe(pd.DataFrame(top_competitors), use_container_width=True)  # Full-width table
    else:
        st.info("No data for top competitors.")

    # Most Popular Venues by Countries
    st.subheader("🌍 Most Popular Venues by Countries")
    popular_venues_query = """
        SELECT v.country_name, COUNT(v.venue_id) AS total_venues
        FROM Venues v
        GROUP BY v.country_name
        ORDER BY total_venues DESC LIMIT 10;
    """
    popular_venues = fetch_data(popular_venues_query)
    if popular_venues:
        st.dataframe(pd.DataFrame(popular_venues), use_container_width=True)  # Full-width table
    else:
        st.info("No data on venue popularity.")

    # Biggest Ranking Movements
    st.subheader("📈 Biggest Ranking Movements")
    ranking_movement_query = """
        SELECT c.name, cr.rank, cr.movement
        FROM Competitors_Ranking cr
        JOIN Competitors c ON cr.competitor_id = c.competitor_id
        ORDER BY ABS(cr.movement) DESC LIMIT 10;
    """
    ranking_movement = fetch_data(ranking_movement_query)
    if ranking_movement:
        st.dataframe(pd.DataFrame(ranking_movement), use_container_width=True)  # Full-width table
    else:
        st.info("No ranking movement data available.")

    # Most Popular Categories (By Competitions)
    st.subheader("📊 Most Popular Categories (By Competitions)")
    popular_categories_query = """
        SELECT cat.category_name, COUNT(comp.competition_id) AS total_competitions
        FROM Categories cat
        JOIN Competitions comp ON cat.category_id = comp.category_id
        GROUP BY cat.category_name
        ORDER BY total_competitions DESC LIMIT 10;
    """
    popular_categories = fetch_data(popular_categories_query)
    if popular_categories:
        st.dataframe(pd.DataFrame(popular_categories), use_container_width=True)  # Full-width table
    else:
        st.info("No data on category popularity.")

    # Upcoming Competitions by Category
    st.subheader("📅 Upcoming Competitions by Category")
    upcoming_competitions_query = """
        SELECT comp.competition_name, cat.category_name, comp.type, comp.gender
        FROM Competitions comp
        JOIN Categories cat ON comp.category_id = cat.category_id
        WHERE (%s = 'all' OR cat.category_name = %s)
        ORDER BY comp.competition_name ASC;
    """
    upcoming_competitions = fetch_data(upcoming_competitions_query, (category, category))
    if upcoming_competitions:
        st.dataframe(pd.DataFrame(upcoming_competitions), use_container_width=True)  # Full-width table
    else:
        st.info("No upcoming competitions available.")

    # Number of Competitions by Gender
    st.subheader("👨‍🦰👩 Number of Competitions by Gender")
    competitions_by_gender_query = """
        SELECT gender, COUNT(competition_id) AS total_competitions
        FROM Competitions
        GROUP BY gender
        ORDER BY total_competitions DESC;
    """
    competitions_by_gender = fetch_data(competitions_by_gender_query)
    if competitions_by_gender:
        st.dataframe(pd.DataFrame(competitions_by_gender), use_container_width=True)  # Full-width table
    else:
        st.info("No data available for competitions by gender.")