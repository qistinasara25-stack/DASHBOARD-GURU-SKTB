import streamlit as st
import pandas as pd
import ssl

# --- 1. FIX MAC (Supaya tak error merah) ---
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# --- 2. TETAPAN HALAMAN ---
st.set_page_config(page_title="Direktori Guru SKTB", page_icon="🏫", layout="wide")
st.title("📸 Galeri Guru SKTB")
st.write("Senarai guru berserta gambar profil.")

# --- 3. TARIK DATA ---
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQHsI6l64Lio14kgKWyRXkG1eS9I-8aIQ22uvsdBkheXuy-38Er2mYhqar08P7IGi_6Ll60gsTU0Eed/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(url, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_data()

# --- 4. PAPARAN KAD PROFIL (DENGAN NO. IC) ---
if df is not None:
    # Butang Refresh
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    # Susun 3 kad dalam satu baris
    cols = st.columns(3)

    for index, row in df.iterrows():
        col = cols[index % 3]
        
        with col:
            with st.container(border=True):
                # A. GAMBAR
                if 'GAMBAR' in row and pd.notna(row['GAMBAR']) and str(row['GAMBAR']).startswith('http'):
                    st.image(row['GAMBAR'], use_container_width=True)
                else:
                    st.write("👤 Tiada Foto")

                # B. MAKLUMAT (Saya dah tambah No. IC di sini)
                st.subheader(row['NAMA GURU'])
                st.write(f"**Jawatan:** {row.get('JAWATAN', '-')}")
                st.write(f"**Gred:** {row.get('GRED', '-')}")
                
                # INI BARIS BARU YANG SAYA TAMBAH:
                st.code(f"IC: {row.get('NO KAD PENGENALAN', '-')}")
