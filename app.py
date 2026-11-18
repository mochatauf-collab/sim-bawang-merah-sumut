import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="SIM Bawang Merah Sumut", page_icon="🧅", layout="wide")

@st.cache_data(ttl=120)
def load_data():
    with psycopg2.connect(st.secrets["DATABASE_URL"], connect_timeout=15) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT kode_data, kabupaten, kecamatan, tahun,
                       komoditas, produksi_ton, wilayah_sumber
                FROM dw.v_analisis_produksi
                ORDER BY kabupaten, kecamatan
            """)
            records = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(records, columns=columns)

st.title("🧅 SIM Bawang Merah Sumatera Utara")
st.caption("Dashboard Data Warehouse Produksi Bawang Merah • Data kecamatan SIMULASI untuk praktikum")

try:
    df = load_data()
except Exception:
    st.error("Gagal membaca data warehouse. Periksa DATABASE_URL, akses Neon, dan jalankan sql/01_data_warehouse.sql pada db_pusat_sumut.")
    st.stop()

if df.empty:
    st.warning("Data warehouse masih kosong. Sinkronkan Colab dan jalankan proses pemuatan warehouse terlebih dahulu.")
    st.stop()

df["produksi_ton"] = pd.to_numeric(df["produksi_ton"])
df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce").astype(int)

with st.sidebar:
    st.header("Filter Data")
    tahun = st.selectbox("Tahun", sorted(df["tahun"].unique().tolist(), reverse=True))
    choices = sorted(df.loc[df["tahun"] == tahun, "kabupaten"].unique().tolist())
    kabupaten = st.multiselect("Kabupaten", choices, default=choices)
    st.info("Nilai produksi per kecamatan adalah simulasi. Jangan gunakan sebagai statistik resmi BPS.")

filtered = df[(df["tahun"] == tahun) & (df["kabupaten"].isin(kabupaten))].copy()
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Kabupaten", filtered["kabupaten"].nunique())
col2.metric("Jumlah Kecamatan", len(filtered))
col3.metric("Total Produksi (ton)", f"{filtered['produksi_ton'].sum():,.2f}")

st.subheader("Produksi menurut Kabupaten")
by_kab = (filtered.groupby("kabupaten", as_index=False)["produksi_ton"]
          .sum().sort_values("produksi_ton", ascending=False))
st.bar_chart(by_kab.set_index("kabupaten"), y="produksi_ton")

st.subheader("Produksi menurut Kecamatan")
by_kec = filtered.sort_values("produksi_ton", ascending=False)
st.dataframe(by_kec[["kabupaten", "kecamatan", "tahun", "produksi_ton", "wilayah_sumber"]],
             use_container_width=True, hide_index=True)

st.download_button("Unduh data terfilter (CSV)",
                   data=filtered.to_csv(index=False).encode("utf-8-sig"),
                   file_name="produksi_bawang_merah_terfilter.csv",
                   mime="text/csv")

st.caption("Sumber: database pusat Neon yang telah disinkronkan melalui Google Colab. Total kabupaten mengacu pada dataset kelompok; pembagian kecamatan adalah data simulasi.")
