import streamlit as st
import pandas as pd
import ssl

# --- 1. MAGIC FIX UNTUK MAC (Kekalkan ini supaya tak error) ---
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# --- 2. TETAPAN HALAMAN ---
# layout="wide" supaya jadual nampak besar dan luas
st.set_page_config(page_title="Direktori Guru SKTB", page_icon="🏫", layout="wide")

st.title("🏫 Senarai Maklumat Guru SKTB")
st.write("Berikut adalah senarai penuh guru. Anda boleh klik tajuk lajur untuk susun (sort).")

# --- 3. TARIK DATA ---
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQHsI6l64Lio14kgKWyRXkG1eS9I-8aIQ22uvsdBkheXuy-38Er2mYhqar08P7IGi_6Ll60gsTU0Eed/pub?output=csv"

@st.cache_data
def load_data():
    try:
        # Baca data
        df = pd.read_csv(url, dtype=str)
        
        # Bersihkan tajuk lajur
        df.columns = df.columns.str.strip()
        
        # Pilih lajur penting sahaja untuk dipaparkan (Buang lajur 'BIL' jika tak perlu)
        # Berdasarkan gambar cikgu, ini lajur yang ada:
        lajur_pilihan = ['NAMA GURU', 'JAWATAN', 'GRED', 'NO KAD PENGENALAN']
        
        # Tapis supaya hanya ambil lajur yang wujud (elak error jika nama ubah)
        lajur_ada = [c for c in lajur_pilihan if c in df.columns]
        
        return df[lajur_ada]
    except Exception as e:
        st.error(f"Gagal memuatkan data: {e}")
        return None

df = load_data()

# --- 4. PAPARAN JADUAL ---
if df is not None:
    # st.dataframe lebih canggih dari st.table
    # Cikgu boleh scroll, boleh besarkan column, dan boleh sort.
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.success(f"Jumlah Guru: {len(df)} orang")
