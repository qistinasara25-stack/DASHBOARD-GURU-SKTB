import streamlit as st
import pandas as pd
import ssl

# --- 1. FIX MAC ---
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# --- 2. TETAPAN ---
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

# --- 4. PAPARAN KAD PROFIL (MENGGUNAKAN GRID) ---
if df is not None:
    # Kita buat butang Refresh
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    # Kita susun 3 kad dalam satu baris (row)
    # Cikgu boleh tukar nombor 3 tu jadi 4 kalau nak lagi padat
    cols = st.columns(3)

    for index, row in df.iterrows():
        # Pilih column ikut giliran (0, 1, 2, ulang balik)
        col = cols[index % 3]
        
        with col:
            # Buat kotak (container) cantik untuk setiap guru
            with st.container(border=True):
                # 1. PAPAR GAMBAR
                # Pastikan nama column dalam Excel ialah 'GAMBAR'
                if 'GAMBAR' in row and pd.notna(row['GAMBAR']) and str(row['GAMBAR']).startswith('http'):
                    st.image(row['GAMBAR'], use_container_width=True)
                else:
                    # Kalau tak ada gambar, letak icon orang lidi
                    st.write("👤 Tiada Foto")

                # 2. PAPAR MAKLUMAT
                st.subheader(row['NAMA GURU'])
                st.caption(f"**Jawatan:** {row.get('JAWATAN', '-')}")
                st.text(f"Gred: {row.get('GRED', '-')}")
                # st.text(f"IC: {row.get('NO KAD PENGENALAN', '-')}") # Boleh 'uncomment' kalau nak tunjuk IC
