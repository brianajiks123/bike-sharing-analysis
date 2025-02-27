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
    monthly_rentals = df.groupby(df['dteday'].dt.to_period("M")).agg({'cnt': 'sum'}).reset_index()
    monthly_rentals['dteday'] = monthly_rentals['dteday'].astype(str)
    return monthly_rentals

def plot_time_series(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='dteday', y='cnt', marker='o', color='b', linewidth=2, ax=ax)
    ax.set_xticklabels(df['dteday'], rotation=45)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Tren Penyewaan Sepeda per Bulan")
    ax.grid(True)
    st.pyplot(fig)

def create_season_trend(df):
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df['season_name'] = df['season_x'].map(season_mapping)
    seasonal_rentals = df.groupby('season_name').agg({'cnt': 'sum'}).reset_index()
    return seasonal_rentals

def plot_season_trend(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x='season_name', y='cnt', palette='coolwarm', hue='season_name', legend=False)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewaan")
    ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(fig)

def plot_temperature_vs_rents(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=df['temp'], y=df['cnt'], alpha=0.5, ax=ax)
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Suhu vs Penyewaan Sepeda")
    ax.grid()
    st.pyplot(fig)

def plot_correlation_heatmap(df):
    correlation_matrix = df[['cnt', 'temp', 'atemp', 'hum', 'windspeed', 'weekday', 'workingday', 'weathersit']].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Korelasi Faktor dengan Jumlah Penyewaan Sepeda")
    st.pyplot(fig)

def plot_grouped_bar_chart(df, group_col, title, labels=None):
    trend = df.groupby(group_col)['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=trend, x=group_col, y='cnt', palette='viridis', hue=group_col, legend=False, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(group_col.replace("_", " ").title())
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.grid(axis='y')
    if labels:
        ax.set_xticklabels(labels, rotation=45)
    st.pyplot(fig)

def plot_weather_impact(df):
    weather_trend = df.groupby("weathersit")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=weather_trend.index, y=weather_trend.values, palette="coolwarm", hue=weather_trend.index, legend=False)
    ax.set_xticklabels(["Clear", "Mist", "Light Snow/Rain", "Heavy Rain/Snow"])
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Rata-rata Penyewaan Sepeda")
    ax.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
    ax.grid(axis='y')
    st.pyplot(fig)

def plot_temperature_category(df):
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    labels = ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    df['temp_category'] = pd.cut(df['temp'], bins=bins, labels=labels)
    grouped_temp = df.groupby('temp_category', observed=False).agg({'cnt': 'mean'}).reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=grouped_temp, x='temp_category', y='cnt', palette='viridis', hue='temp_category')
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Pengaruh Kategori Suhu terhadap Penyewaan Sepeda")
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

# Bike Rental Trends per Month
st.markdown("<h3 style='text-align: center;'>Tren Penyewaan Sepeda per Bulan</h3>", unsafe_allow_html=True)
plot_time_series(monthly_trend)

# Average Bike Rentals per Season
st.markdown("<h3 style='text-align: center;'>Jumlah Penyewaan Sepeda Berdasarkan Musim</h3>", unsafe_allow_html=True)
plot_season_trend(season_trend)

# Temperature vs Total Rents
st.markdown("<h3 style='text-align: center;'>Suhu vs Penyewaan Sepeda</h3>", unsafe_allow_html=True)
plot_temperature_vs_rents(main_df)

# Correlation Heatmap
st.markdown("<h3 style='text-align: center;'>Korelasi Faktor dengan Jumlah Penyewaan Sepeda</h3>", unsafe_allow_html=True)
plot_correlation_heatmap(main_df)

# Manual Grouping Analysis
st.markdown("<h2 style='text-align: center;'>- Manual Grouping -</h2>", unsafe_allow_html=True)

# Average Bike Rents by Time of Day
st.markdown("<h3 style='text-align: center;'>Rata-rata Penyewaan Sepeda Berdasarkan Waktu dalam Sehari</h3>", unsafe_allow_html=True)
main_df['time_of_day'] = pd.cut(main_df['hr'], bins=[0, 6, 12, 18, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False, ordered=False)
plot_grouped_bar_chart(main_df, "time_of_day", "Rata-rata Penyewaan Sepeda Berdasarkan Waktu dalam Sehari")

st.markdown("<h3 style='text-align: center;'>Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda</h3>", unsafe_allow_html=True)
plot_weather_impact(main_df)

st.markdown("<h3 style='text-align: center;'>Pengaruh Kategori Suhu terhadap Penyewaan Sepeda</h3>", unsafe_allow_html=True)
plot_temperature_category(main_df)
