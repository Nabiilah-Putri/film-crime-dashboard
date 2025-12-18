import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
country_options = ["All"] + countries

selected_countries = st.sidebar.multiselect(
    "Pilih Negara (bisa satu, banyak, atau All)",
    options=country_options,
    default=["All"]
)

years = sorted(final_data["Tahun"].unique())
selected_years = st.sidebar.slider("Rentang Tahun", min_value=min(years), max_value=max(years),
                                   value=(min(years), max(years)))

# Logika filter negara
if "All" in selected_countries or len(selected_countries) == 0:
    filtered = final_data[final_data["Tahun"].between(selected_years[0], selected_years[1])]
else:
    filtered = final_data[
        (final_data["Negara"].isin(selected_countries)) &
        (final_data["Tahun"].between(selected_years[0], selected_years[1]))
    ]

# -------------------------------
# DASHBOARD
# -------------------------------
st.title("🎬 Dashboard Film & Kriminalitas ASEAN (2020–2024)")
st.caption("Interaktif: jelajahi jumlah film per genre, tren per tahun, dan hubungannya dengan Crime Rate.")

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Negara", ", ".join(selected_countries) if "All" not in selected_countries else "All ASEAN")
col2.metric("Periode", f"{selected_years[0]}–{selected_years[1]}")
col3.metric("Jumlah Data", len(filtered))

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Distribusi Genre", 
    "Tren Film & Crime Rate", 
    "Scatter Jumlah Film vs Crime Rate", 
    "Korelasi Heatmap", 
    "Statistik Deskriptif",
    "Visualisasi Statistik"
])

# -------------------------------
# TAB 1: Distribusi Genre (perbandingan antar negara)
# -------------------------------
with tab1:
    st.subheader("Distribusi Genre Film per Negara")
    genre_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun", "Crime Rate"]]
    genre_sum = filtered.groupby("Negara")[genre_cols].sum().reset_index()
    genre_melt = genre_sum.melt(id_vars="Negara", var_name="Genre", value_name="Jumlah")
    fig = px.bar(genre_melt, x="Genre", y="Jumlah", color="Negara", barmode="group",
                 title="Jumlah Film per Genre per Negara")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# TAB 2: Tren Film & Crime Rate (perbandingan antar negara)
# -------------------------------
with tab2:
    st.subheader("Tren Jumlah Film & Crime Rate per Negara")
    film_counts = filtered.groupby(["Negara","Tahun"])[genre_cols].sum().sum(axis=1).reset_index(name="Jumlah Film")
    crime_trend = filtered[["Negara","Tahun","Crime Rate"]]
    trend_df = pd.merge(film_counts, crime_trend, on=["Negara","Tahun"], how="inner")

    fig1 = px.line(trend_df, x="Tahun", y="Jumlah Film", color="Negara", markers=True,
                   title="Jumlah Film per Tahun per Negara")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(trend_df, x="Tahun", y="Crime Rate", color="Negara", markers=True,
                   title="Crime Rate per Tahun per Negara")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# TAB 3: Scatter Jumlah Film vs Crime Rate (perbandingan antar negara)
# -------------------------------
with tab3:
    st.subheader("Scatter Plot Jumlah Film vs Crime Rate per Negara")
    film_counts = filtered.groupby(["Negara","Tahun"])[genre_cols].sum().sum(axis=1).reset_index(name="Jumlah Film")
    scatter_df = pd.merge(film_counts, filtered[["Negara","Tahun","Crime Rate"]], on=["Negara","Tahun"], how="inner")
    fig3 = px.scatter(scatter_df, x="Jumlah Film", y="Crime Rate", color="Negara",
                      title="Jumlah Film vs Crime Rate per Negara", trendline="ols")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# TAB 4: Korelasi Heatmap (gabungan data filter)
# -------------------------------
with tab4:
    st.subheader("Korelasi Genre dengan Crime Rate (gabungan data filter)")
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

# -------------------------------
# TAB 6: Visualisasi Statistik Deskriptif (REVISI)
# -------------------------------
with tab6:
    st.subheader("Visualisasi Statistik Deskriptif")

    num_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun"]]
    stats = filtered[num_cols].agg(["mean", "std", "min", "max"]).T.reset_index()
    stats.columns = ["Variabel", "Mean", "Std", "Min", "Max"]

    # === BAR CHART MEAN ===
    fig_mean = px.bar(
        stats,
        x="Variabel",
        y="Mean",
        color="Variabel",
        text="Mean",
        title="Rata-rata (Mean) per Variabel"
    )
    fig_mean.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_mean.update_layout(showlegend=False)
    st.plotly_chart(fig_mean, use_container_width=True)

    # === ERROR BAR (MEAN ± STD) ===
    fig_std = px.bar(
        stats,
        x="Variabel",
        y="Mean",
        error_y="Std",
        color="Variabel",
        text="Std",
        title="Mean dengan Standar Deviasi"
    )
    fig_std.update_traces(texttemplate="±%{text:.2f}", textposition="outside")
    fig_std.update_layout(showlegend=False)
    st.plotly_chart(fig_std, use_container_width=True)

    # === RANGE PLOT (MIN–MAX) ===
    fig_range = px.bar(
        stats,
        x="Variabel",
        y="Max",
        base="Min",
        color="Variabel",
        text="Max",
        title="Rentang Nilai (Min–Max) per Variabel"
    )
    fig_range.update_traces(
        texttemplate="Max: %{text:.2f}",
        textposition="outside"
    )
    fig_range.update_layout(showlegend=False)
    st.plotly_chart(fig_range, use_container_width=True)
