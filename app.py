import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Dashboard Film & Kriminalitas ASEAN", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_final_data():
    df = pd.read_excel("final_data_film.xlsx")
    crime = pd.read_csv("data_kriminalitas.csv")
    # cleaning crime sesuai preprocessing
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
st.caption("Interaktif: jelajahi jumlah film per genre dan hubungannya dengan Crime Rate.")

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Negara", selected_country)
col2.metric("Periode", f"{selected_years[0]}–{selected_years[1]}")
col3.metric("Jumlah Data", len(filtered))

# Tabs
tab1, tab2, tab3 = st.tabs(["Distribusi Genre", "Tren Crime Rate", "Korelasi"])

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
# TAB 2: Tren Crime Rate
# -------------------------------
with tab2:
    st.subheader("Tren Crime Rate per Tahun")
    fig2 = px.line(filtered, x="Tahun", y="Crime Rate", markers=True,
                   title=f"Crime Rate {selected_country}")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# TAB 3: Korelasi
# -------------------------------
with tab3:
    st.subheader("Korelasi Genre dengan Crime Rate")
    genre_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun", "Crime Rate"]]
    corr = filtered[genre_cols + ["Crime Rate"]].corr()
    fig3, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig3)