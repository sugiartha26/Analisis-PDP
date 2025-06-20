import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analisis Konsultasi & Aduan PDP", layout="wide")
st.title("📊 Aplikasi Analisis Konsultasi & Aduan PDP")

# === Upload File ===
uploaded_file = st.file_uploader("Unggah file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # === Filter Section ===
    st.sidebar.header("🔎 Filter Data")
    jenis_layanan = st.sidebar.multiselect("Pilih Jenis Layanan", options=df["Jenis Layanan"].unique(), default=df["Jenis Layanan"].unique())
    kanal = st.sidebar.multiselect("Pilih Kanal", options=df["Kanal"].unique(), default=df["Kanal"].unique())
    kategori_topik = st.sidebar.multiselect("Pilih Kategori Topik", options=df["Kategori Topik"].unique(), default=df["Kategori Topik"].unique())

    df_filtered = df[
        df["Jenis Layanan"].isin(jenis_layanan) &
        df["Kanal"].isin(kanal) &
        df["Kategori Topik"].isin(kategori_topik)
    ]

    st.subheader("📌 Data Tersaring")
    st.dataframe(df_filtered)

    # === Analisis Deskriptif ===
    st.subheader("📈 Analisis Deskriptif")
    st.write("Jumlah Baris dan Kolom:", df_filtered.shape)
    st.write("Statistik Deskriptif Kolom 'Jumlah':")
    st.write(df_filtered["Jumlah"].describe())

    st.write("Jumlah per Jenis Layanan:")
    st.bar_chart(df_filtered.groupby("Jenis Layanan")["Jumlah"].sum())

    st.write("Jumlah per Kanal:")
    st.bar_chart(df_filtered.groupby("Kanal")["Jumlah"].sum())

    st.write("Topik Teratas:")
    st.dataframe(df_filtered.groupby("Kategori Topik")["Jumlah"].sum().sort_values(ascending=False).reset_index())

    # === Missing Value ===
    st.subheader("🧩 Missing Value")
    missing = df_filtered.isnull().sum()
    if missing.sum() == 0:
        st.success("✅ Tidak ada missing value.")
    else:
        st.warning("⚠️ Terdapat missing value:")
        st.write(missing[missing > 0])

    # === Duplikasi ===
    st.subheader("📋 Duplikasi Data")
    duplicates = df_filtered.duplicated().sum()
    st.write(f"Jumlah data duplikat: {duplicates}")

    # === Outlier ===
    st.subheader("🚨 Outlier")
    Q1 = df_filtered["Jumlah"].quantile(0.25)
    Q3 = df_filtered["Jumlah"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df_filtered[(df_filtered["Jumlah"] < lower_bound) | (df_filtered["Jumlah"] > upper_bound)]
    st.write(f"Jumlah outlier: {len(outliers)}")
    if not outliers.empty:
        st.dataframe(outliers)

    # === Visualisasi ===
    st.subheader("📊 Visualisasi Distribusi")

    fig1, ax1 = plt.subplots()
    ax1.boxplot(df_filtered["Jumlah"], vert=False)
    ax1.set_title("Boxplot Jumlah Konsultasi dan Aduan")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.hist(df_filtered["Jumlah"], bins=15, edgecolor='black')
    ax2.set_title("Histogram Jumlah Konsultasi dan Aduan")
    st.pyplot(fig2)

    # === Insight ===
    st.subheader("💡 Insight dari Data")

    topik_teratas = df_filtered.groupby("Kategori Topik")["Jumlah"].sum().sort_values(ascending=False).head(3)
    kanal_terbanyak = df_filtered.groupby("Kanal")["Jumlah"].sum().sort_values(ascending=False).head(1)
    layanan_terbanyak = df_filtered.groupby("Jenis Layanan")["Jumlah"].sum().sort_values(ascending=False).head(1)

    st.markdown(f"""
    - 🔝 **Topik paling sering muncul**: {', '.join(topik_teratas.index)} dengan jumlah tertinggi {topik_teratas.iloc[0]}.
    - 📬 **Kanal paling sering digunakan**: {kanal_terbanyak.index[0]} ({kanal_terbanyak.iloc[0]} aduan/konsultasi).
    - 🧾 **Jenis layanan paling umum**: {layanan_terbanyak.index[0]}.
    - 📌 Terdeteksi **{len(outliers)} data outlier**, menunjukkan ketimpangan distribusi antar topik.
    """)
