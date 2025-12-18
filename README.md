# 🎬 Dashboard Film & Kriminalitas ASEAN (2020–2024)

🔗 **Akses Dashboard Streamlit:**

👉 https://film-crime-dashboard.streamlit.app/

---

## 📌 Deskripsi Singkat

Dashboard ini merupakan aplikasi visualisasi interaktif berbasis **Streamlit** yang digunakan untuk menganalisis **jumlah produksi film berdasarkan genre** serta **hubungannya dengan tingkat kriminalitas (Crime Rate)** di negara-negara ASEAN pada periode **2020–2024**.

Aplikasi ini dirancang untuk membantu pengguna dalam:

* Mengeksplorasi distribusi genre film di setiap negara ASEAN
* Membandingkan tren jumlah film dan Crime Rate antar negara dan antar tahun
* Mengamati hubungan statistik antara produksi film dan tingkat kriminalitas
* Menyajikan statistik deskriptif secara jelas dan informatif

---

## 🎯 Tujuan Pembuatan

1. Menyajikan analisis deskriptif data film dan kriminalitas secara visual
2. Memberikan perbandingan antar negara ASEAN secara interaktif
3. Mendukung pemahaman statistik melalui grafik dan tabel yang mudah dibaca
4. Mengimplementasikan dashboard data menggunakan Streamlit

---

## 📂 Dataset yang Digunakan

Aplikasi ini menggunakan dua dataset utama:

1. **Data Produksi Film ASEAN**
   Berisi jumlah film berdasarkan genre, negara, dan tahun.

2. **Data Kriminalitas ASEAN**
   Berisi nilai **Crime Rate** per negara dan tahun.

Kedua dataset digabungkan (merge) berdasarkan atribut **Negara** dan **Tahun** untuk keperluan analisis.

---

## 🧭 Fitur Utama Dashboard

### 🔹 Filter Interaktif

* **Filter Negara**: dapat memilih satu negara, beberapa negara, atau seluruh negara ASEAN (All)
* **Filter Rentang Tahun**: memilih periode analisis menggunakan slider

Filter ini akan memengaruhi **seluruh visualisasi** pada dashboard.

---

### 🔹 Tab Visualisasi

#### 1️⃣ Distribusi Genre Film

Menampilkan perbandingan jumlah film per genre di setiap negara ASEAN dalam bentuk bar chart.

#### 2️⃣ Tren Film & Crime Rate

Menampilkan tren:

* Jumlah film per tahun
* Crime Rate per tahun
  untuk setiap negara yang dipilih.

#### 3️⃣ Scatter Plot Film vs Crime Rate

Visualisasi hubungan antara jumlah film dan Crime Rate, dilengkapi dengan **garis tren (OLS)** untuk membantu interpretasi pola hubungan.

#### 4️⃣ Korelasi

Heatmap korelasi antara genre film dan Crime Rate untuk melihat keterkaitan antar variabel.

#### 5️⃣ Statistik Deskriptif

Tabel statistik deskriptif yang mencakup:

* Mean
* Standar Deviasi
* Nilai Minimum
* Nilai Maksimum

#### 6️⃣ Visualisasi Statistik Deskriptif

Menampilkan:

* Batang sebagai **Mean**
* Error bar sebagai **rentang Min–Max**
* Label angka **Minimum dan Maksimum**

Visualisasi ini menyerupai konsep boxplot secara informasi, namun disajikan dalam bentuk bar chart agar lebih mudah dibaca.

---

## 🧠 Pendekatan Analisis

* Analisis deskriptif kuantitatif
* Visualisasi data menggunakan Plotly, Matplotlib, dan Seaborn
* Statistik dasar (mean, standar deviasi, min, max)
* Analisis korelasi dan hubungan antar variabel

---

## 🛠️ Teknologi yang Digunakan

* **Python**
* **Streamlit** (Dashboard interaktif)
* **Pandas** (Pengolahan data)
* **Plotly** (Visualisasi interaktif)
* **Matplotlib & Seaborn** (Visualisasi statistik)

---

## 📎 Cara Menjalankan Secara Lokal (Opsional)

```bash
git clone <repository-url>
cd <nama-repo>
pip install -r requirements.txt
streamlit run app.py
```

---

## 👩‍🎓 Catatan Akademik

Dashboard ini dibuat sebagai bagian dari tugas akademik untuk menunjukkan kemampuan dalam:

* Pengolahan dan integrasi data
* Analisis statistik deskriptif
* Visualisasi data interaktif
* Implementasi dashboard berbasis web

---

📌 **Link Dashboard:**
[https://film-crime-dashboard.streamlit.app/]

---

## 👥 Anggota Kelompok

1. **Nabiilah Putri Karnaia** – NIM: 122450029
2. **Amalia Melani Putri** – NIM: 122450121
3. **Fayyaza Aqila Syafitri Achjar** – NIM: 122450131

---

✍️ *Dikembangkan untuk keperluan akademik dan pembelajaran analisis data.*
