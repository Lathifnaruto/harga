import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load model dan data asli
model_data = joblib.load('model_regresi_rumah.sav')
df = pd.read_csv('rumah.csv')

model = model_data['model']
features = model_data['features']
encode_map = model_data['encode_map']
metrics = model_data.get('metrics', {})

# Streamlit Config
st.set_page_config(page_title="Prediksi Harga Rumah", page_icon="🏠", layout="centered")

# --- Custom CSS with Aqua Price Box ---
st.markdown("""
    <style>
    :root {
        /* Color Palette */
        --primary: rgba(30, 34, 46, 0.95);
        --secondary: rgba(40, 44, 58, 0.98);
        --text: #e2e8f0;
        --text-secondary: #94a3b8;
        --accent: #4f46e5;
        --accent-light: #6366f1;
        --card: rgba(26, 32, 44, 0.98);
        --border: rgba(74, 85, 104, 0.3);
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    .stApp {
        background: linear-gradient(rgba(30, 34, 46, 0.95), 
                    url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: var(--text);
        min-height: 100vh;
    }
    
    /* Aqua Price Box */
    .aqua-price-box {
        padding: 30px;
        background: linear-gradient(135deg, #00FFFF, #00BFFF);
        border-radius: 12px;
        text-align: center;
        border: 2px solid #00CED1;
        margin: 25px 0;
        color: #003366 !important;
        box-shadow: 0 6px 20px rgba(0, 191, 255, 0.2);
    }
    
    .aqua-price-box h2 {
        color: #003366 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .aqua-price-box p {
        color: #003366 !important;
        font-weight: 500;
    }
    
    /* Rest of your existing CSS... */
    .main .block-container {
        background-color: var(--primary);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid var(--border);
    }
    
    /* ... (keep all your other existing CSS styles) ... */
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🏠 Prediksi Harga Rumah")
st.markdown("Masukkan detail properti untuk memprediksi harga dalam Rupiah")

# --- Form Input ---
with st.form("form_rumah"):
    st.subheader("📋 Detail Properti")
    col1, col2 = st.columns(2)

    with col1:
        bedrooms = st.number_input("Jumlah Kamar Tidur", 0, 10, 2)
        bathrooms = st.number_input("Jumlah Kamar Mandi", 0, 10, 1)
        land_size = st.number_input("Luas Tanah (m²)", 0, 1000, 100)
        building_size = st.number_input("Luas Bangunan (m²)", 0, 1000, 80)
        property_type = st.selectbox("Tipe Properti", ['rumah'])

    with col2:
        floors = st.selectbox("Jumlah Lantai", [1, 2, 3])
        building_age = st.number_input("Usia Bangunan (tahun)", 0, 100, 5)
        garages = st.selectbox("Jumlah Garasi", [0, 1, 2, 3])
        furnishing = st.selectbox("Perabotan", ['unfurnished', 'furnished', 'semi furnished'])
        property_condition = st.selectbox("Kondisi Properti", ['bagus', 'bagus sekali'])

    submit = st.form_submit_button("🔍 Prediksi Harga")

# --- Feature Importance Visualization ---
st.subheader("📊 Pentingnya Fitur dalam Prediksi Harga")

feature_importance = model.feature_importances_
importance_df = pd.DataFrame({
    'Fitur': features,
    'Pengaruh': feature_importance
}).sort_values('Pengaruh', ascending=False)

st.bar_chart(importance_df.set_index('Fitur'))
st.markdown("""
**Penjelasan Pentingnya Fitur:**
- Nilai di atas menunjukkan seberapa besar pengaruh setiap fitur terhadap prediksi harga rumah
- Semakin tinggi nilainya, semakin besar pengaruh fitur tersebut dalam menentukan harga
""")
st.write("Detail Pengaruh Setiap Fitur:")
st.dataframe(importance_df.style.format({'Pengaruh': '{:.2%}'}))

# --- Prediction ---
if submit:
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
            'property_type': encode_map['property_type'].get(property_type, 0),
            'furnishing': encode_map['furnishing'].get(furnishing, 1),
            'property_condition': encode_map['property_condition'].get(property_condition, 2)
        }

        data_input = pd.DataFrame([input_dict])[features]

        with st.spinner("🔄 Memproses prediksi..."):
            harga_prediksi = model.predict(data_input)[0]
            harga_rupiah = f"Rp {harga_prediksi:,.0f}".replace(",", ".")

        st.divider()
        st.subheader("💰 Estimasi Harga Rumah")
        
        # Aqua-themed price box
        st.markdown(
            f"""
            <div class="aqua-price-box">
                <h2>🏡 {harga_rupiah}</h2>
                <p>Perkiraan berdasarkan data properti yang Anda masukkan</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Similar Properties ---
        st.subheader("🔍 Properti Serupa")
        try:
            similar_properties = df[
                (df['bedrooms'].between(bedrooms-1, bedrooms+1)) &
                (df['bathrooms'].between(bathrooms-1, bathrooms+1)) &
                (df['land_size_m2'].between(land_size*0.8, land_size*1.2)) &
                (df['building_size_m2'].between(building_size*0.8, building_size*1.2)) &
                (df['floors'] == floors)
            ]
            
            if not similar_properties.empty:
                similar_properties['price_diff'] = abs(similar_properties['price_in_rp'] - harga_prediksi)
                similar_properties = similar_properties.sort_values('price_diff').head(3)
                
                for _, prop in similar_properties.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="similar-property">
                            <h4>{prop['title']}</h4>
                            <p>📍 {prop['address']}</p>
                            <p>🛏️ {int(prop['bedrooms'])} Kamar | 🚿 {int(prop['bathrooms'])} Kamar Mandi</p>
                            <p>📐 Luas Tanah: {prop['land_size_m2']} m² | Luas Bangunan: {prop['building_size_m2']} m²</p>
                            <p>💰 <strong>Rp {prop['price_in_rp']:,.0f}</strong></p>
                            <a href="{prop['url']}" target="_blank">🔗 Lihat Detail Properti</a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Tidak ditemukan properti serupa dalam database kami.")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencari properti serupa: {str(e)}")

        if metrics:
            st.subheader("📊 Evaluasi Model")
            st.success(f"**Akurasi Pada Score Prediksi (R² Score):** {metrics['R2'] * 100:.2f}%")

# --- Footer ---
st.markdown("<div class='footer'>© 2023 Aplikasi Prediksi Harga Rumah | Jasasaja Rumah 123</div>", unsafe_allow_html=True)
