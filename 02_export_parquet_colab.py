# Jalankan di notebook Google Colab setelah: !pip install psycopg2-binary duckdb pandas pyarrow
# dan setelah variabel db_pusat (connection string Neon pusat) tersedia.
import pandas as pd
import psycopg2
import duckdb

with psycopg2.connect(db_pusat) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT kabupaten, kecamatan, tahun, komoditas, produksi_ton
            FROM dw.v_analisis_produksi
        """)
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description]

df = pd.DataFrame(rows, columns=columns)
df["produksi_ton"] = df["produksi_ton"].astype(float)
con = duckdb.connect()
con.register("produksi", df)
con.execute("COPY (SELECT * FROM produksi) TO 'produksi_bawang_merah_2025.parquet' (FORMAT PARQUET)")
ringkasan = con.execute("""
    SELECT kabupaten, tahun, COUNT(*) AS jumlah_kecamatan,
           SUM(produksi_ton) AS total_produksi_ton
    FROM read_parquet('produksi_bawang_merah_2025.parquet')
    GROUP BY kabupaten, tahun
    ORDER BY total_produksi_ton DESC
""").df()
print(ringkasan)
# Opsional untuk mengunduh file di Colab:
# from google.colab import files
# files.download('produksi_bawang_merah_2025.parquet')
