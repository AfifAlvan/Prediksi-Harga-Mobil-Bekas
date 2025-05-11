import streamlit as st
import pandas as pd
import joblib

# Load model dan encoder
model = joblib.load("model_harga_mobil.pkl")
le_merek = joblib.load("le_merek.pkl")
le_model = joblib.load("le_model.pkl")

# Load dataset referensi untuk mapping Merek ke Tipe
df = pd.read_csv("data_mobil_new.csv")
merek_tipe_map = df.groupby('Merek')['Model'].unique().to_dict()
# --- Sidebar Navigasi ---
st.sidebar.title("🚗 Navigasi")
halaman = st.sidebar.radio("Pilih Halaman", ["Home", "Prediksi Harga"])

# Logo / Gambar di Sidebar (opsional)
# st.sidebar.image("https://apollo.olx.co.id/v1/files/679cbde4642c9-ID/image;s=850x0", width=120)

# --- HOME PAGE ---
if halaman == "Home":
    st.title("🛠️ Aplikasi Prediksi Harga Mobil Bekas")
    st.image("mobil.jpg", width=700)

# Menambahkan deskripsi yang lebih menarik di Streamlit
    st.markdown("""
        <p style='font-size: 20px;'>🔍 Di halaman Prediksi Harga kamu bisa:</p>
        <ul style='font-size: 18px;'>
            <li>Mengetahui harga mobil berdasarkan <strong>merek, tipe, dan tahun</strong></li>
            <li>Menyesuaikan input sesuai data historis</li>
        </ul>
        <h3 style='text-align: center; font-size: 22px;'>💡 Bagaimana cara kerjanya?</h3>
        <p style='font-size: 18px;'>
            1. <strong>Pengolahan Data Cerdas dengan AI</strong>: Kami menggunakan data harga mobil bekas selama 20 tahun terakhir untuk menghitung depresiasi harga secara akurat, membantu kamu mengetahui tren harga mobil dari tahun ke tahun.<br><br>
            2. <strong>Model Generative AI untuk Prediksi Harga</strong>: Aplikasi ini memprediksi harga mobil bekas berdasarkan merek, tipe, dan tahun mobil, dengan teknologi AI yang canggih.<br><br>
            3. <strong>Deployment Sederhana & Cepat</strong>: Sistem mudah diakses dan memberikan prediksi harga secara real-time dan tepat.
        </p>
    """, unsafe_allow_html=True)

    

# --- PREDIKSI PAGE ---
elif halaman == "Prediksi Harga":
    st.title("🔮 Prediksi Harga Mobil Bekas")

    # Pilihan Merek
    merek = st.selectbox("Pilih Merek Mobil", sorted(merek_tipe_map.keys()))

    # Pilihan Tipe berdasarkan Merek
    
    tipe_list = sorted(merek_tipe_map.get(merek, []))
    tipe = st.selectbox("Pilih Tipe Mobil", tipe_list)

    # Input Tahun
    tahun = st.number_input("Tahun Mobil", min_value=1990, max_value=2025, value=2015)

    # Tombol Prediksi
    if st.button("Prediksi Harga"):
        if merek not in le_merek.classes_ or tipe not in le_model.classes_:
            st.error("Merek atau Tipe belum dikenali oleh model. Coba gunakan data dari pelatihan.")
        else:
            merek_encoded = le_merek.transform([merek])[0]
            tipe_encoded = le_model.transform([tipe])[0]
            input_data = pd.DataFrame([[merek_encoded, tipe_encoded, tahun]],
                                      columns=['Merek_encoded', 'Model_encoded', 'Tahun'])
            prediksi = model.predict(input_data)[0]
            st.markdown(f"""
            <h2 style='color: #4CAF50; text-align: center; font-size: 40px;'>
                Harga prediksi mobil bekas {merek} {tipe} tahun {tahun} adalah:
            </h2>
            <h3 style='color: #FF5722; text-align: center; font-size: 50px; font-weight: bold;'>
                Rp {prediksi:,.2f}
            </h3>
        """, unsafe_allow_html=True)
