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

# --- Custom CSS untuk Background Transparan dengan Gambar Rumah Mewah ---
# --- Custom CSS for Dark Theme ---
st.markdown("""
    <style>
    :root {
        /* Color Palette */
        --primary: rgba(30, 34, 46, 0.95);       /* Dark slate blue */
        --secondary: rgba(40, 44, 58, 0.98);     /* Slightly lighter dark */
        --text: #e2e8f0;                        /* Soft white for text */
        --text-secondary: #94a3b8;               /* Lighter gray for secondary text */
        --accent: #4f46e5;                       /* Vibrant indigo for accents */
        --accent-light: #6366f1;                 /* Lighter accent */
        --card: rgba(26, 32, 44, 0.98);         /* Dark card background */
        --border: rgba(74, 85, 104, 0.3);        /* Subtle border color */
        --success: #10b981;                      /* Green for success messages */
        --warning: #f59e0b;                      /* Amber for warnings */
        --error: #ef4444;                        /* Red for errors */
    }
    
    /* Base App Styling */
    .stApp {
        background: linear-gradient(rgba(30, 34, 46, 0.95), 
                    url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: var(--text);
        min-height: 100vh;
    }
    
    /* Main Container */
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
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text) !important;
        font-weight: 600 !important;
    }
    
    p {
        color: var(--text-secondary);
    }
    
    /* Result Box */
    .result-box {
        padding: 25px;
        background: linear-gradient(135deg, var(--card), var(--secondary));
        backdrop-filter: blur(4px);
        border-radius: 12px;
        text-align: center;
        border: 1px solid var(--accent-light);
        margin: 20px 0;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .result-box h2 {
        color: white !important;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Form Elements */
    .stTextInput input, 
    .stNumberInput input, 
    .stSelectbox select {
        background-color: var(--secondary) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    
    label {
        color: var(--text) !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--accent) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-light) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }
    
    /* Similar Property Cards */
    .similar-property {
        background: var(--card);
        padding: 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid var(--accent);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .similar-property:hover {
        transform: translateY(-3px);
    }
    
    .similar-property h4 {
        color: var(--text) !important;
        margin-bottom: 0.5rem;
    }
    
    .similar-property a {
        color: var(--accent-light) !important;
        text-decoration: none;
        font-weight: 500;
    }
    
    /* Notifications */
    .stAlert {
        border-radius: 8px !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border-left: 4px solid var(--warning) !important;
    }
    
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid var(--success) !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid var(--error) !important;
    }
    
    /* Footer */
    .footer {
        background-color: rgba(26, 32, 44, 0.9);
        text-align: center;
        font-size: 0.85em;
        color: var(--text-secondary) !important;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 2rem;
        border-top: 1px solid var(--border);
    }

    /* Aqua-themed result box */
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
    
    /* Data Tables */
    .dataframe {
        background-color: var(--card) !important;
        color: var(--text) !important;
    }
    
    /* Divider */
    .stDivider>div>div>div {
        background-color: var(--accent) !important;
        height: 2px !important;
    }
    
    /* Spinner */
    .stSpinner>div>div {
        border-color: var(--accent) transparent transparent transparent !important;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        
        .result-box {
            padding: 1rem;
        }
    }
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

# Dapatkan importance scores dari model
feature_importance = model.feature_importances_
importance_df = pd.DataFrame({
    'Fitur': features,
    'Pengaruh': feature_importance
}).sort_values('Pengaruh', ascending=False)

# Tampilkan dalam bentuk bar chart
st.bar_chart(importance_df.set_index('Fitur'))

# Tampilkan penjelasan
st.markdown("""
**Penjelasan Pentingnya Fitur:**
- Nilai di atas menunjukkan seberapa besar pengaruh setiap fitur terhadap prediksi harga rumah
- Semakin tinggi nilainya, semakin besar pengaruh fitur tersebut dalam menentukan harga
""")

# Tampilkan tabel detail
st.write("Detail Pengaruh Setiap Fitur:")
st.dataframe(importance_df.style.format({'Pengaruh': '{:.2%}'}))

# --- Prediction ---
if submit:
    if land_size == 0 or building_size == 0:
        st.warning("Luas tanah dan bangunan tidak boleh nol!")
    else:
        # ... (previous prediction code remains the same until the result box)

        st.divider()
        st.subheader("💰 Estimasi Harga Rumah")
        
        # Box hasil prediksi dengan desain aqua
        st.markdown(
            f"""
            <div class="result-box" style="
                background: linear-gradient(135deg, #00FFFF, #00BFFF);
                border: 2px solid #00CED1;
                color: #003366 !important;
            ">
                <h2 style="
                    color: #003366 !important;
                    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
                    font-size: 2.2rem;
                    margin-bottom: 0.5rem;
                ">🏡 {harga_rupiah}</h2>
                <p style="color: #003366; font-weight: 500;">Perkiraan berdasarkan data properti yang Anda masukkan</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Cari Properti Serupa ---
        st.subheader("🔍 Properti Serupa")
        
        try:
            # Cari properti dengan kriteria yang mirip
            similar_properties = df[
                (df['bedrooms'].between(bedrooms-1, bedrooms+1)) &
                (df['bathrooms'].between(bathrooms-1, bathrooms+1)) &
                (df['land_size_m2'].between(land_size*0.8, land_size*1.2)) &
                (df['building_size_m2'].between(building_size*0.8, building_size*1.2)) &
                (df['floors'] == floors)
            ]
            
            if not similar_properties.empty:
                # Ambil 3 properti terdekat
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

        # --- Evaluasi Model ---
        if metrics:
            st.subheader("📊 Evaluasi Model")
            st.success(f"**Akurasi Pada Score Prediksi (R² Score):** {metrics['R2'] * 100:.2f}%")

# --- Footer ---
st.markdown("<div class='footer'>© 2023 Aplikasi Prediksi Harga Rumah | Jasasaja Rumah 123</div>", unsafe_allow_html=True)
