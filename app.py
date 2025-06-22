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

# Initialize history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

# ======= Dark Theme with White Text =======
st.markdown("""
<style>
:root {
    /* Color Palette - Dark Theme */
    --primary-dark: #1a1a2e;
    --secondary-dark: #16213e;
    --card-dark: #0f3460;
    --text-primary: #ffffff;  /* White text */
    --text-secondary: #e0e0e0;
    --accent: #3b82f6;
    --accent-light: #60a5fa;
    --border-dark: rgba(255, 255, 255, 0.1);
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
}

/* Main App Background */
.stApp {
    background-color: var(--primary-dark) !important;
    color: var(--text-primary) !important;
}

/* All Text Elements - White */
h1, h2, h3, h4, h5, h6,
.stMarkdown p,
.stMarkdown li,
.stMarkdown ul,
.stMarkdown ol {
    color: white !important;
}

/* Mengubah warna teks pada header dan subheader */
.stTitle h1, 
.stTitle h2, 
.stTitle h3 {
    color: white !important;
}

/* Mengubah warna teks pada form */
div[data-testid="stForm"] label,
div[data-testid="stForm"] h3 {
    color: white !important;
}

/* Mengubah warna teks pada expander */
.stExpanderHeader p {
    color: black !important;
}

/* Mengubah warna teks pada alert boxes */
.stAlert p {
    color: white !important;
}
/* Mengubah warna teks pada tombol submit menjadi putih */
div[data-testid="stForm"] button[kind="secondary"] span {
    color: white !important;
}

/* Mengubah warna ikon 🔍 menjadi putih */
div[data-testid="stForm"] button[kind="secondary"]::before {
    color: white !important;
}

/* Opsional: mengubah warna saat hover */
div[data-testid="stForm"] button[kind="secondary"]:hover span {
    color: white !important;
}

/* Main Container */
.main .block-container {
    background-color: var(--card-dark) !important;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    border: 1px solid var(--border-dark);
}

/* Buttons and Links */
.stButton button {
    background-color: var(--accent) !important;
    color: black !important;
    border: none !important;
}

.property-link-btn {
    background-color: var(--accent) !important;
    color: white !important;
    border: 2px solid var(--accent-light) !important;
    display: inline-block;
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    text-decoration: none !important;
    font-weight: 600;
    margin-top: 0.75rem;
    transition: all 0.3s ease;
    cursor: pointer;
    text-align: center;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
}

.property-link-btn:hover {
    background-color: var(--accent-light) !important;
    color: white !important;
}

/* Result Box */
.result-box {
    padding: 30px;
    background: linear-gradient(135deg, var(--card-dark), var(--secondary-dark)) !important;
    border-radius: 12px;
    text-align: center;
    border: 1px solid var(--accent);
    margin: 25px 0;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}

/* History Section */
.history-item {
    background-color: var(--secondary-dark) !important;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 4px solid var(--accent);
}
.history-item:hover {
    background-color: rgba(55, 65, 81, 0.9);
}
.history-timestamp {
    font-size: 0.85em;
    color: var(--text-secondary) !important;
    margin-bottom: 5px;
}
.history-price {
    font-weight: bold;
    font-size: 1.1em;
    color: var(--accent-light) !important;
}

/* Banner */
.animated-banner {
    width: 100%;
    overflow: hidden;
    background-color: rgba(30, 30, 30, 0.9) !important;
    padding: 10px 0;
    border-radius: 10px;
    margin-bottom: 20px;
    border: 1px solid var(--border-dark);
}
.animated-text {
    display: inline-block;
    white-space: nowrap;
    animation: slideText 12s linear infinite;
    font-weight: bold;
    font-size: 18px;
    color: var(--text-primary) !important;
    padding-left: 100%;
}
@keyframes slideText {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}

/* Footer */
.footer {
    text-align: center !important;
    color: var(--text-secondary) !important;
    padding: 1rem;
    margin-top: 2rem;
    font-size: 0.9em;
}

/* Alert Boxes */
.stAlert {
    background-color: rgba(15, 52, 96, 0.8) !important;
    border-left: 4px solid var(--accent) !important;
}
</style>

<div class="animated-banner">
    <div class="animated-text">SELAMAT DATANG DI APLIKASI PREDIKSI HARGA RUMAH</div>
</div>
""", unsafe_allow_html=True)

# Header
st.title("🏠 Prediksi Harga Rumah")
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

            # Add to history
            pred_data = {
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'harga_prediksi': harga_prediksi,
                'input_data': input_dict
            }
            st.session_state.history.append(pred_data)

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
    <a class="property-link-btn" href="{prop['url']}" target="_blank">
        <span style="margin-right: 5px;">🔍</span> Lihat Detail Properti
    </a>
</div>
""", unsafe_allow_html=True)
            else:
                st.info("Tidak ditemukan properti serupa dalam database kami.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mencari properti serupa: {str(e)}")

        if metrics:
            st.subheader("📊 Evaluasi Model")
            st.success(f"**Akurasi Pada Score Prediksi (R² Score):** {metrics['R2'] * 100:.2f}%")

# History Section
with st.expander("📜 History Prediksi", expanded=False):
    if not st.session_state.history:
        st.info("Belum ada riwayat prediksi.")
    else:
        for idx, item in enumerate(st.session_state.history[::-1]):  # Show newest first
            with st.container():
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-timestamp">⏱️ {item['timestamp']}</div>
                    <div class="history-price">💰 Rp {item['harga_prediksi']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Lihat Detail", key=f"detail_{idx}", help="Klik untuk melihat detail input"):
                    st.json(item['input_data'])

# Footer
st.markdown("""
<div class='footer'>
    Aplikasi Prediksi Harga Rumah | Jasasaja Rumah 123
</div>
""", unsafe_allow_html=True)
