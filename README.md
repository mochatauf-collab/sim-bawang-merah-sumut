# SIM Bawang Merah Sumut — Dashboard

## Alur
Colab -> Neon db_pusat_sumut (`public.produksi_bawang_merah_pusat`) -> warehouse `dw` -> Streamlit dashboard.

## Persiapan Neon
Jalankan `sql/01_data_warehouse.sql` di SQL Editor pada database `db_pusat_sumut` SETELAH 20 data masuk ke tabel pusat. Untuk memperbarui warehouse setelah Colab sinkronisasi ulang, jalankan kembali SQL tersebut.

## Publikasi dengan GitHub + Streamlit Community Cloud
1. Buat repo GitHub. Upload `app.py`, `requirements.txt`, `.gitignore`, folder `sql`, dan `scripts`.
2. Di share.streamlit.io, pilih Create app, GitHub repo, branch `main`, entrypoint `app.py`.
3. Masukkan secret di Advanced settings (JANGAN unggah ke GitHub):
   DATABASE_URL = "postgresql://USER:PASSWORD@HOST/db_pusat_sumut?sslmode=require"
4. Deploy. Pastikan user database memiliki hak SELECT pada view warehouse.

## Analitik kolumnar / big-data pipeline (demonstrasi)
Jalankan `scripts/02_export_parquet_colab.py` di Google Colab setelah instalasi `duckdb` dan `pyarrow`. Data diekspor ke Parquet lalu diagregasi dengan DuckDB. Ini demonstrasi teknik analitik yang dapat diskalakan, bukan dataset big data (hanya 20 baris).

## Peringatan
Angka produksi per kecamatan adalah SIMULASI. Jangan tampilkan sebagai statistik BPS tingkat kecamatan.
