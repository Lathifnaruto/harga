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

# Tambahkan animasi teks berjalan modern
st.markdown("""
<style>

/* Property Link Button Styles */
.property-link-btn {
    display: inline-block;
    background-color: var(--accent);
    color: white !important;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    text-decoration: none !important;
    font-weight: 500;
    margin-top: 0.5rem;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.property-link-btn:hover {
    background-color: var(--accent-light);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.property-link-btn:active {
    transform: translateY(0);
}
.animated-banner {
    width: 100%;
    overflow: hidden;
    background-color: rgba(79, 70, 229, 0.2);
    padding: 10px 0;
    border-radius: 10px;
    margin-bottom: 20px;
}
.animated-text {
    display: inline-block;
    white-space: nowrap;
    animation: slideText 12s linear infinite;
    font-weight: bold;
    font-size: 18px;
    color: white;
    padding-left: 100%;
}
@keyframes slideText {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}
</style>
<div class="animated-banner">
    <div class="animated-text">SELAMAT DATANG DI APLIKASI PREDIKSI HARGA RUMAH</div>
</div>
""", unsafe_allow_html=True)

# Judul
st.title("🏠 Prediksi Harga Rumah")
st.markdown("=============================================================")
st.markdown("Tugas Penambangan Data ")
st.markdown("Nama Mahasiswa : Muhammad Lathif")
st.markdown("Nama Mahasiswa : Fadmada Ananta Maharani")
st.markdown("=============================================================")
st.markdown("Masukkan detail properti untuk memprediksi harga dalam Rupiah")

# Form Input
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

# Feature Importance
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

# Prediction
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
        st.markdown(f"""
        <div class="result-box">
            <h2>🏡 {harga_rupiah}</h2>
            <p>Perkiraan berdasarkan data properti yang Anda masukkan</p>
        </div>
        """, unsafe_allow_html=True)

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
                    st.markdown(f"""
<div class="similar-property">
    <h4>{prop['title']}</h4>
    <p>📍 {prop['address']}</p>
    <p>🛏️ {int(prop['bedrooms'])} Kamar | 🚿 {int(prop['bathrooms'])} Kamar Mandi</p>
    <p>📐 Luas Tanah: {prop['land_size_m2']} m² | Luas Bangunan: {prop['building_size_m2']} m²</p>
    <p>💰 <strong>Rp {prop['price_in_rp']:,.0f}</strong></p>
    <a class="property-link-btn" href="{prop['url']}" target="_blank">🔗 Lihat Detail Properti</a>
</div>
""", unsafe_allow_html=True)
            else:
                st.info("Tidak ditemukan properti serupa dalam database kami.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencari properti serupa: {str(e)}")

        if metrics:
            st.subheader("📊 Evaluasi Model")
            st.success(f"**Akurasi Pada Score Prediksi (R² Score):** {metrics['R2'] * 100:.2f}%")

# Footer
st.markdown("""
    <div class='footer' style='text-align: center;'>
        Aplikasi Prediksi Harga Rumah | Jasasaja Rumah 123
    </div>
""", unsafe_allow_html=True)
