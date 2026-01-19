import streamlit as st
import pandas as pd

# --- TETAPAN HALAMAN ---
st.set_page_config(page_title="Sistem Maklumat Guru", page_icon="👨‍🏫", layout="wide")
st.title("📂 Carian Maklumat Guru SKTB")
st.write("Masukkan No. Kad Pengenalan (dengan atau tanpa sengkang).")

# --- SAMBUNGAN DATA ---
# Link CSV Google Sheets Cikgu
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQHsI6l64Lio14kgKWyRXkG1eS9I-8aIQ22uvsdBkheXuy-38Er2mYhqar08P7IGi_6Ll60gsTU0Eed/pub?output=csv"

@st.cache_data
def load_data():
    try:
        # Baca data CSV
        df = pd.read_csv(csv_url, dtype=str)
        # Bersihkan tajuk lajur
        df.columns = df.columns.str.strip()
        # Buat lajur carian bersih
        if 'NO KAD PENGENALAN' in df.columns:
            df['clean_ic'] = df['NO KAD PENGENALAN'].str.replace('-', '').str.replace(' ', '')
        return df
    except Exception as e:
        st.error(f"Masalah memuatkan data: {e}")
        return None

df = load_data()

# --- RUANG CARIAN ---
if df is not None:
    # Susun atur input
    col1, col2 = st.columns([3, 1])
    with col1:
        ic_input = st.text_input("No. Kad Pengenalan:", max_chars=14, placeholder="Contoh: 780119-10-5935")
    
    if st.button("Cari Maklumat"):
        if ic_input:
            input_bersih = ic_input.replace('-', '').replace(' ', '')
            
            if 'clean_ic' in df.columns:
                hasil = df[df['clean_ic'] == input_bersih]
                if not hasil.empty:
                    st.success(f"✅ Rekod Ditemui: {hasil.iloc[0]['NAMA GURU']}")
                    # Pilih maklumat untuk dipapar
                    cols = ['NAMA GURU', 'NO KAD PENGENALAN', 'JAWATAN', 'GRED']
                    valid_cols = [c for c in cols if c in hasil.columns]
                    st.table(hasil[valid_cols].T)
                else:
                    st.error("❌ Tiada rekod dijumpai.")
            else:
                st.error("Lajur 'NO KAD PENGENALAN' tiada dalam data.")
