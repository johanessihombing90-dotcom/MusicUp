import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="MusicUp", page_icon="🎵", layout="centered")

st.title("🎵 MusicUp")
st.caption("AI Pembuat Musik, Not Angka & Chord Otomatis")

# Mengambil kunci dari pengaturan Hugging Face Secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key Gemini belum diatur di menu Settings -> Variables and secrets!")
    st.stop()

genai.configure(api_key=api_key)

tab1, tab2 = st.tabs(["🔍 Analisis & Bedah Musik", "✍️ Ciptakan Lagu Baru"])

with tab1:
    st.header("🔍 Analisis Komposisi Musik")
    input_musik = st.text_area("Tempel lirik atau progresi chord di sini:", height=150)
    if st.button("Bedah Musik Sekarang", key="btn_analisis"):
        if input_musik.strip() == "":
            st.warning("Silakan masukkan teks musik!")
        else:
            with st.spinner("AI sedang membedah struktur musikmu..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    perintah = f"Analisis struktur musik, progresi chord, dan makna dari teks musik berikut: {input_musik}"
                    respons = model.generate_content(perintah)
                    st.success("Analisis Selesai!")
                    st.markdown(respons.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

with tab2:
    st.header("✍️ Generator Lagu & Not Angka")
    tema = st.text_input("Apa tema lagu yang diinginkan?", placeholder="Contoh: Cinta budaya Batak Toba")
    genre = st.selectbox("Pilih Genre Musik:", ["Pop", "Akustik / Folk", "Dangdut", "Rock", "Jazz", "Reggae"])
    tempo = st.select_slider("Pilih Tempo Lagu:", options=["Lambat", "Sedang", "Cepat"])
    
    if st.button("Ciptakan Lagu Sekarang", key="btn_cipta"):
        if tema.strip() == "":
            st.warning("Silakan isi tema lagu!")
        else:
            with st.spinner("AI sedang menggubah lagu untukmu..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    perintah = (
                        f"Buatkan sebuah lagu utuh dengan tema '{tema}', bergenre {genre}, dengan tempo {tempo}. "
                        f"PENTING: Tuliskan chord gitarnya di atas lirik secara presisi, "
                        f"dan sertakan juga panduan 'Not Angka' (1 2 3 4 5 6 7) di setiap baris liriknya."
                    )
                    respons = model.generate_content(perintah)
                    st.success("Lagu Berhasil Diciptakan!")
                    st.markdown(respons.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
