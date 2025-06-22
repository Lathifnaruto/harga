import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load model dan data
model_data = joblib.load('model_regresi_rumah.sav')
model = model_data['model']
features = model_data['features']
encode_map = model_data['encode_map']

# Konfigurasi tampilan
st.set_page_config(
    page_title="Prediksi Harga Rumah",
    page_icon="🏠",
    layout="centered"
)

# CSS untuk tampilan minimalis
st.markdown("""
<style>
:root {
    --primary: #2c3e50;
    --secondary: #3498db;
    --light: #ecf0f1;
    --dark: #2c3e50;
    --success: #2ecc71;
}

/* Warna dasar */
.stApp {
    background-color: #f5f5f5;
}

/* Header */
.stTitle h1 {
    color: var(--primary) !important;
    border-bottom: 2px solid var(--secondary);
    padding-bottom: 10px;
}

/* Card input */
.css-1aumxhk {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Tombol */
.stButton>button {
    background-color: var(--secondary) !important;
    color: white !important;
    border: none;
    border-radius: 5px;
    padding: 10px 24px;
    font-weight: 500;
    transition: all 0.3s;
}

.stButton>button:hover {
    background-color: #2980b9 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Hasil prediksi */
.result-card {
    background: linear-gradient(135deg, #3498db, #2c3e50);
    color: white;
    border-radius: 10px;
    padding: 25px;
    margin: 20px 0;
    text-align: center;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

/* History item */
.history-item {
    background-color: white;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
    border-left: 4px solid var(--secondary);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# Session state untuk history
if 'history' not in st.session_state:
    st.session_state.history = []

# Header aplikasi
st.title("🏠 Prediksi Harga Rumah")
st.markdown("""
Aplikasi ini membantu Anda memperkirakan harga properti berdasarkan karakteristik rumah.
""")

# Form input
with st.form("input_form"):
    st.subheader("📋 Data Properti")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bedrooms = st.number_input("Jumlah Kamar Tidur", 0, 10, 2)
        bathrooms = st.number_input("Jumlah Kamar Mandi", 0, 10, 1)
        land_size = st.number_input("Luas Tanah (m²)", 0, 1000, 100)
        building_size = st.number_input("Luas Bangunan (m²)", 0, 1000, 80)
        
    with col2:
        floors = st.selectbox("Jumlah Lantai", [1, 2, 3])
        building_age = st.number_input("Usia Bangunan (tahun)", 0, 100, 5)
        garages = st.selectbox("Jumlah Garasi", [0, 1, 2, 3])
        furnishing = st.selectbox("Perabotan", ['unfurnished', 'furnished', 'semi furnished'])
    
    submitted = st.form_submit_button("🚀 Prediksi Harga")

import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import numpy as np

# Prediksi
if submitted:
    if land_size == 0 or building_size == 0:
        st.warning("Luas tanah dan bangunan tidak boleh nol!")
    else:
        input_dict = {
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'land_size_m2': land_size,
            'building_size_m2': building_size,
            'floors': floors,
            'building_age': building_age,
            'garages': garages,
            'property_type': 0,  # default untuk rumah
            'furnishing': encode_map['furnishing'].get(furnishing, 1),
            'property_condition': 1  # default bagus
        }
        
        data_input = pd.DataFrame([input_dict])[features]
        
        with st.spinner("Menghitung prediksi..."):
            harga_prediksi = model.predict(data_input)[0]
            harga_rupiah = f"Rp {harga_prediksi:,.0f}".replace(",", ".")
            
            # =============================================
            # NEW: BREAKDOWN ALASAN PREDIKSI
            # =============================================
            
            # 1. Dapatkan feature importance
            feature_importance = model.feature_importances_
            sorted_idx = np.argsort(feature_importance)[::-1]
            top_features = features[sorted_idx][:3]  # Ambil 3 fitur terpenting
            
            # 2. Hitung kontribusi masing-masing fitur
            contributions = {}
            mean_values = model_data['mean_values']  # Asumsi sudah disimpan saat training
            
            for feat in top_features:
                # Hitung seberapa jauh nilai input dari rata-rata
                input_val = input_dict.get(feat, 0)
                mean_val = mean_values.get(feat, 0)
                diff = input_val - mean_val
                
                # Simpan kontribusi (positif/negatif)
                contributions[feat] = {
                    'value': input_val,
                    'diff': diff,
                    'impact': 'meningkatkan' if diff > 0 else 'menurunkan'
                }
            
            # 3. Generate explanation text
            explanations = []
            for feat in top_features:
                feat_name = {
                    'land_size_m2': 'Luas Tanah',
                    'building_size_m2': 'Luas Bangunan',
                    'bedrooms': 'Jumlah Kamar Tidur',
                    'building_age': 'Usia Bangunan',
                    'furnishing': 'Kelengkapan Furnitur'
                }.get(feat, feat)
                
                explanations.append(
                    f"• **{feat_name}**: {contributions[feat]['value']} "
                    f"({contributions[feat]['impact']} harga sebesar ~{abs(contributions[feat]['diff']*100:.1f}%)"
                )
            
            # Simpan ke history
            pred_data = {
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'harga_prediksi': harga_prediksi,
                'input_data': input_dict,
                'explanation': explanations  # NEW: Simpan penjelasan
            }
            st.session_state.history.append(pred_data)
        
        # Tampilkan hasil
        st.markdown(f"""
        <div class="result-card">
            <h2>Estimasi Harga</h2>
            <h3>{harga_rupiah}</h3>
            <p>Berdasarkan karakteristik properti yang dimasukkan</p>
        </div>
        """, unsafe_allow_html=True)
        
        # =============================================
        # NEW: TAMPILKAN BREAKDOWN
        # =============================================
        st.subheader("🔍 Faktor Penentu Harga")
        
        with st.expander("Lihat Detail Analisis"):
            st.markdown("""
            **3 Faktor Terbesar yang Mempengaruhi Harga:**
            """)
            
            for exp in explanations:
                st.markdown(exp)
            
            st.markdown("""
            ---
            **Keterangan:**
            - Persentase menunjukkan seberapa besar penyimpangan dari nilai rata-rata properti
            - Faktor lain seperti lokasi tidak ditampilkan karena tidak dimasukkan dalam input
            """)

# ... [Rest of the code remains the same] ...
