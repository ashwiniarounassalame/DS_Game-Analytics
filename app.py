import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import mysql.connector
import requests
import json

print("host:", os.getenv("host"))
print("user_name:", os.getenv("user_name"))
print("password:", os.getenv("password"))
print("database:", os.getenv("database"))
print("API_KEY:", os.getenv("API_KEY"))

try:
    conn = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user_name"),
        password=os.getenv("password"),
        database=os.getenv("database")
    )
    print("Connection successful")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error Code: {err.errno}")
    print(f"SQLState: {err.sqlstate}")
    print(f"Error Message: {err.msg}")
    print(f"Error: {err}")

# Function to connect to the database
def create_db_connection():
    return mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user_name"),
        password=os.getenv("password"),
        database=os.getenv("database")
    )

# Function to fetch data from the Sportradar API
def fetch_api_data(endpoint, params=None):
    api_key = os.getenv('API_KEY')
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Competitions", "Complexes", "Competitors", "Country Analysis", "Leaderboards"])

# Home page
if page == "Home":
    st.title("Game Analytics: Tennis Data Insights")
    st.markdown("""
        Welcome to the Tennis Data Insights application powered by Sportradar API.
        Navigate through the tabs to explore and analyze sports data interactively.
    """)

# Competitions page
if page == "Competitions":
    st.title("Competitions Overview")
    st.write("Explore competition data stored in the database.")

    db_conn = create_db_connection()
    query = "SELECT * FROM competitions;"
    competitions = pd.read_sql(query, db_conn)
    db_conn.close()

    st.dataframe(competitions)

# Complexes page
if page == "Complexes":
    st.title("Complexes and Venues")
    st.write("Details about sports complexes and their venues.")
    
    db_conn = create_db_connection()
    query = """
        SELECT v.venue_name, v.city_name, v.country_name, c.complex_name
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id;
    """
    venues = pd.read_sql(query, db_conn)
    db_conn.close()

    st.dataframe(venues)

# Competitors page
if page == "Competitors":
    st.title("Competitor Rankings")
    st.write("Details about competitors and their rankings.")
    
    db_conn = create_db_connection()
    query = "SELECT * FROM competitor_rankings;"
    rankings = pd.read_sql(query, db_conn)
    db_conn.close()

    st.dataframe(rankings)

# Country Analysis page
if page == "Country Analysis":
    st.title("Country-Wise Competitor Analysis")
    db_conn = create_db_connection()
    query = """
        SELECT country, COUNT(*) as num_competitors, AVG(points) as avg_points
        FROM competitors
        GROUP BY country
        ORDER BY num_competitors DESC;
    """
    country_analysis = pd.read_sql(query, db_conn)
    db_conn.close()

    st.dataframe(country_analysis)

# Leaderboards page
if page == "Leaderboards":
    st.title("Top Competitors")
    db_conn = create_db_connection()
    query = "SELECT name, rank, points FROM competitor_rankings ORDER BY rank ASC LIMIT 5;"
    top_competitors = pd.read_sql(query, db_conn)
    db_conn.close()

    st.table(top_competitors)

st.sidebar.markdown("---")
st.sidebar.info("Data powered by Sportradar API")
