import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Film & Kriminalitas ASEAN", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_final_data():
    df = pd.read_excel("final_data_film.xlsx")
    crime = pd.read_csv("data_kriminalitas.csv")
    crime["Negara"] = crime["Negara"].str.strip()
    crime["Negara"] = crime["Negara"].replace({
        "Philipina": "Philippines",
        "Myannar": "Myanmar",
        "Brunei": "Brunei Darussalam"
    })
    crime["Crime Rate"] = crime["Crime Rate"].str.replace(",", ".").astype(float)
    final_data = pd.merge(df, crime, on=["Negara", "Tahun"], how="inner")
    return final_data

final_data = load_final_data()

# -------------------------------
# SIDEBAR FILTER
# -------------------------------
st.sidebar.header("Filter")
countries = sorted(final_data["Negara"].unique())
years = sorted(final_data["Tahun"].unique())

selected_country = st.sidebar.selectbox("Pilih Negara", countries)
selected_years = st.sidebar.slider("Rentang Tahun", min_value=min(years), max_value=max(years),
                                   value=(min(years), max(years)))

filtered = final_data[(final_data["Negara"] == selected_country) &
                      (final_data["Tahun"].between(selected_years[0], selected_years[1]))]

# -------------------------------
# DASHBOARD
# -------------------------------
st.title("🎬 Dashboard Film & Kriminalitas ASEAN (2020–2024)")
st.caption("Interaktif: jelajahi jumlah film per genre, tren per tahun, dan hubungannya dengan Crime Rate.")

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Negara", selected_country)
col2.metric("Periode", f"{selected_years[0]}–{selected_years[1]}")
col3.metric("Jumlah Data", len(filtered))

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Distribusi Genre", 
    "Tren Film & Crime Rate", 
    "Scatter Jumlah Film vs Crime Rate", 
    "Korelasi Heatmap", 
    "Statistik Deskriptif"
])

# -------------------------------
# TAB 1: Distribusi Genre
# -------------------------------
with tab1:
    st.subheader("Distribusi Genre Film")
    genre_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun", "Crime Rate"]]
    genre_sum = filtered[genre_cols].sum().reset_index()
    genre_sum.columns = ["Genre", "Jumlah"]
    fig = px.bar(genre_sum, x="Genre", y="Jumlah", title="Jumlah Film per Genre")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# TAB 2: Tren Film & Crime Rate
# -------------------------------
with tab2:
    st.subheader("Tren Jumlah Film & Crime Rate")
    film_counts = filtered.groupby("Tahun")[genre_cols].sum().sum(axis=1).reset_index(name="Jumlah Film")
    crime_trend = filtered[["Tahun", "Crime Rate"]].dropna()
    trend_df = pd.merge(film_counts, crime_trend, on="Tahun", how="outer").sort_values("Tahun")

    fig1 = px.bar(trend_df, x="Tahun", y="Jumlah Film", title="Jumlah Film per Tahun")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(trend_df, x="Tahun", y="Crime Rate", markers=True, title="Crime Rate per Tahun")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# TAB 3: Scatter Jumlah Film vs Crime Rate
# -------------------------------
with tab3:
    st.subheader("Scatter Plot Jumlah Film vs Crime Rate")
    film_counts = filtered.groupby("Tahun")[genre_cols].sum().sum(axis=1).reset_index(name="Jumlah Film")
    scatter_df = pd.merge(film_counts, filtered[["Tahun", "Crime Rate"]], on="Tahun", how="inner")
    fig3 = px.scatter(scatter_df, x="Jumlah Film", y="Crime Rate", color="Tahun",
                      trendline="ols", title="Jumlah Film vs Crime Rate")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# TAB 4: Korelasi Heatmap
# -------------------------------
with tab4:
    st.subheader("Korelasi Genre dengan Crime Rate")
    corr = filtered[genre_cols + ["Crime Rate"]].corr()
    fig4, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig4)

# -------------------------------
# TAB 5: Statistik Deskriptif
# -------------------------------
with tab5:
    st.subheader("Statistik Deskriptif")
    num_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun"]]
    stats = filtered[num_cols].agg(["mean", "std", "min", "max", "median"]).T
    stats = stats.rename(columns={
        "mean": "Mean", "std": "Std", "min": "Min", "max": "Max", "median": "Median"
    })
    st.dataframe(stats, use_container_width=True)

    st.subheader("Distribusi Crime Rate")
    fig5, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(filtered["Crime Rate"], bins=10, kde=True, color="skyblue", ax=ax[0])
    ax[0].set_title("Distribusi Crime Rate")
    sns.boxplot(x=filtered["Crime Rate"], color="lightgreen", ax=ax[1])
    ax[1].set_title("Boxplot Crime Rate")
    st.pyplot(fig5)
