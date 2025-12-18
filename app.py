import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Film & Kriminalitas ASEAN", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data(show_spinner="Memuat data...")
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
    "Pilih Negara",
    options=country_options,
    default=["All"]
)

years = sorted(final_data["Tahun"].unique())
selected_years = st.sidebar.slider(
    "Rentang Tahun",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

if "All" in selected_countries or len(selected_countries) == 0:
    filtered = final_data[final_data["Tahun"].between(*selected_years)]
else:
    filtered = final_data[
        (final_data["Negara"].isin(selected_countries)) &
        (final_data["Tahun"].between(*selected_years))
    ]

# -------------------------------
# DASHBOARD HEADER
# -------------------------------
st.title("🎬 Dashboard Film & Kriminalitas ASEAN (2020–2024)")
st.caption("Analisis interaktif jumlah film, genre, dan keterkaitannya dengan Crime Rate.")

col1, col2, col3 = st.columns(3)
col1.metric("Negara", "All ASEAN" if "All" in selected_countries else ", ".join(selected_countries))
col2.metric("Periode", f"{selected_years[0]}–{selected_years[1]}")
col3.metric("Jumlah Data", len(filtered))

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Distribusi Genre",
    "Tren Film & Crime Rate",
    "Scatter Film vs Crime Rate",
    "Korelasi",
    "Statistik Deskriptif",
    "Visualisasi Statistik"
])

# -------------------------------
# TAB 1
# -------------------------------
with tab1:
    st.subheader("Distribusi Genre Film per Negara")
    genre_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun", "Crime Rate"]]
    genre_sum = filtered.groupby("Negara")[genre_cols].sum().reset_index()
    genre_melt = genre_sum.melt(id_vars="Negara", var_name="Genre", value_name="Jumlah")

    fig = px.bar(
        genre_melt,
        x="Genre",
        y="Jumlah",
        color="Negara",
        barmode="group",
        title="Jumlah Film per Genre per Negara"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# TAB 2
# -------------------------------
with tab2:
    st.subheader("Tren Jumlah Film dan Crime Rate")

    film_counts = filtered.groupby(["Negara", "Tahun"])[genre_cols].sum().sum(axis=1).reset_index(name="Jumlah Film")
    trend_df = pd.merge(film_counts, filtered[["Negara", "Tahun", "Crime Rate"]], on=["Negara", "Tahun"])

    fig1 = px.line(trend_df, x="Tahun", y="Jumlah Film", color="Negara", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(trend_df, x="Tahun", y="Crime Rate", color="Negara", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# TAB 3
# -------------------------------
with tab3:
    st.subheader("Hubungan Jumlah Film dan Crime Rate")

    fig3 = px.scatter(
        trend_df,
        x="Jumlah Film",
        y="Crime Rate",
        color="Negara",
        trendline="ols",
        title="Scatter Plot Jumlah Film vs Crime Rate"
    )
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# TAB 4
# -------------------------------
with tab4:
    st.subheader("Korelasi Genre dengan Crime Rate")
    corr = filtered[genre_cols + ["Crime Rate"]].corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

# -------------------------------
# TAB 5
# -------------------------------
with tab5:
    st.subheader("Statistik Deskriptif")
    num_cols = [c for c in final_data.columns if c not in ["Negara", "Tahun"]]
    stats = filtered[num_cols].agg(["mean", "std", "min", "max"]).T
    stats.columns = ["Mean", "Std", "Min", "Max"]
    st.dataframe(stats, use_container_width=True)

# -------------------------------
# TAB 6 (FINAL – TANPA RADAR CHART)
# -------------------------------
with tab6:
    st.subheader("Visualisasi Statistik Deskriptif")

    stats_vis = stats.reset_index().rename(columns={"index": "Variabel"})

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=stats_vis["Variabel"],
        y=stats_vis["Mean"],
        name="Mean",
        error_y=dict(
            type="data",
            symmetric=False,
            array=stats_vis["Max"] - stats_vis["Mean"],
            arrayminus=stats_vis["Mean"] - stats_vis["Min"]
        )
    ))

    fig.add_trace(go.Scatter(
        x=stats_vis["Variabel"],
        y=stats_vis["Max"],
        mode="text",
        text=[f"Max: {v:.2f}" for v in stats_vis["Max"]],
        textposition="top center",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=stats_vis["Variabel"],
        y=stats_vis["Min"],
        mode="text",
        text=[f"Min: {v:.2f}" for v in stats_vis["Min"]],
        textposition="bottom center",
        showlegend=False
    ))

    fig.update_layout(
        title="Mean dengan Rentang Minimum dan Maksimum",
        yaxis_title="Nilai",
        xaxis_title="Variabel"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Bar chart Mean per Genre
    fig_mean = px.bar(stats.reset_index(), x="index", y="Mean", title="Rata-rata Film per Genre")
    st.plotly_chart(fig_mean, use_container_width=True)


