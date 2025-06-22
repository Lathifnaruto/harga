import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load model and original data
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

# ======= Custom Theme =======
st.markdown("""
<style>
:root {
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --text: #ffffff;
    --background: #0f172a;
    --card: #1e293b;
    --border: #334155;
}

/* Main app styling */
.stApp {
    background-color: var(--background);
    color: var(--text);
}

/* Button styling */
.stButton>button {
    background-color: var(--primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin-top: 15px !important;
}

.stButton>button:hover {
    background-color: var(--primary-hover) !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, #1e3a8a, #1e40af);
    color: white;
    border-radius: 12px;
    padding: 25px;
    margin: 20px 0;
    text-align: center;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    border: 1px solid var(--border);
}

/* Header styling */
.stTitle h1 {
    color: white !important;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 10px;
}

/* Form styling */
.css-1aumxhk {
    background-color: var(--card);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border: 1px solid var(--border);
}
</style>
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

    # Prediction button with custom styling
    submit = st.form_submit_button(
        "🔍 PREDIKSI HARGA",
        type="primary",
        help="Klik untuk memproses prediksi harga rumah"
    )

# Feature Importance
st.subheader("📊 Pentingnya Fitur dalam Prediksi Harga")
feature_importance = model.feature_importances_
importance_df = pd.DataFrame({
    'Fitur': features,
    'Pengaruh': feature_importance
}).sort_values('Pengaruh', ascending=False)
st.bar_chart(importance_df.set_index('Fitur'))

# Prediction Logic
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
        <div class="result-card">
            <h2>🏡 {harga_rupiah}</h2>
            <p>Perkiraan berdasarkan data properti yang Anda masukkan</p>
        </div>
        """, unsafe_allow_html=True)

        # Similar properties and history sections remain the same...
        # ... [rest of your existing code]

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 40px; color: #94a3b8; font-size: 0.9em;'>
    Aplikasi Prediksi Harga Rumah | © 2023
</div>
""", unsafe_allow_html=True)
