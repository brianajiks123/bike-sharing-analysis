import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Helper functions
def load_data(file_path):
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    df.sort_values(by="dteday", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def filter_data(df, start_date, end_date):
    return df[(df["dteday"] >= start_date) & (df["dteday"] <= end_date)]

def create_monthly_trend(df):
    monthly_trend = df.groupby(df['dteday'].dt.to_period("M"))["cnt"].sum().reset_index()
    monthly_trend.rename(columns={"cnt": "total_rents"}, inplace=True)
    monthly_trend["dteday"] = monthly_trend["dteday"].astype(str)
    return monthly_trend

def plot_time_series(df):
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.lineplot(x=df["dteday"], y=df["total_rents"], marker='o', linestyle='-', linewidth=2, color="b", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Rents")
    ax.set_title("Bike Rental Trens per Month")
    st.pyplot(fig)

def create_season_trend(df):
    return df.groupby("season_x")["cnt"].mean().reset_index()

def plot_temperature_vs_rents(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x=df["temp"], y=df["cnt"], alpha=0.5, ax=ax)
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Total Rents")
    ax.set_title("Temperature vs. Total Rents")
    st.pyplot(fig)

def plot_grouped_bar_chart(df, group_col, title, labels=None):
    trend = df.groupby(group_col)["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=trend.index, y=trend.values, palette="coolwarm", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(group_col.replace("_", " ").title())
    ax.set_ylabel("Average Bike Rents")
    if labels:
        ax.set_xticklabels(labels, rotation=45)
    st.pyplot(fig)

def plot_season_trend(df):
    season_trend = df.groupby("season_x")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=season_trend.index, y=season_trend.values, palette="coolwarm", hue=season_trend.index, legend=False)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    ax.set_title("Average Bike Rentals per Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Average Number of Bike Rentals")
    ax.grid(axis='y')
    st.pyplot(fig)

# Load data
all_df = load_data("merge_data.csv")

# Sidebar for date filtering
min_date, max_date = all_df["dteday"].min(), all_df["dteday"].max()
with st.sidebar:
    st.header("Name: Brian Aji Pamungkas")
    start_date, end_date = st.date_input(
        label='Dates:',
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=[min_date.to_pydatetime(), max_date.to_pydatetime()]
    )
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    st.caption(f'Copyright © Brian Aji Pamungkas {datetime.now().year}')

# Filter data
main_df = filter_data(all_df, start_date, end_date)

# Create DataFrames for visualization
monthly_trend = create_monthly_trend(main_df)
season_trend = create_season_trend(main_df)

# Dashboard Layout
st.markdown("<h1 style='text-align: center;'>🚲 Bike Sharing Dashboard 📊</h1>", unsafe_allow_html=True)

# Daily Rents
st.markdown("<h2 style='text-align: center;'>Daily Rents</h2>", unsafe_allow_html=True)
total_rents = monthly_trend["total_rents"].sum()
st.markdown(f"<h5 style='text-align: center;'>Total Rents: {total_rents}</h5>", unsafe_allow_html=True)

# Bike Rental Trens per Month
st.markdown("<h3 style='text-align: center;'>Bike Rental Trens per Month</h3>", unsafe_allow_html=True)
plot_time_series(monthly_trend)

# Average Bike Rentals per Season
st.markdown("<h3 style='text-align: center;'>Average Bike Rentals per Season</h3>", unsafe_allow_html=True)
plot_season_trend(main_df)

# Temperature vs Total Rents
st.markdown("<h3 style='text-align: center;'>Temperature vs Total Rents</h3>", unsafe_allow_html=True)
plot_temperature_vs_rents(main_df)

# Manual Grouping Analysis
st.markdown("<h2 style='text-align: center;'>- Manual Grouping -</h2>", unsafe_allow_html=True)

# Average Bike Rents by Time of Day
st.markdown("<h3 style='text-align: center;'>Average Bike Rents by Time of Day</h3>", unsafe_allow_html=True)
main_df['time_of_day'] = pd.cut(main_df['hr'], bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False, ordered=False)
plot_grouped_bar_chart(main_df, "time_of_day", "Average Bike Rents by Time of Day")

# Average Bike Rents by Weather Condition
st.markdown("<h3 style='text-align: center;'>Average Bike Rents by Weather Condition</h3>", unsafe_allow_html=True)
weather_labels = ["Clear", "Mist", "Light Snow/Rain", "Heavy Rain/Snow"]
plot_grouped_bar_chart(main_df, "weathersit", "Average Bike Rents by Weather Condition", labels=weather_labels)
