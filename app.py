import streamlit as st
import google.generativeai as genai
import os
from gtts import gTTS
import io

st.set_page_config(page_title="MusicUp", page_icon="🎵", layout="centered")

st.title("🎵 MusicUpPro")
st.caption("AI Pembuat Musik, Not Angka, Chord & Audio Assistant")

# Mengambil kunci dari pengaturan Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key Gemini belum diatur di menu Advanced Settings -> Secrets!")
    st.stop()

genai.configure(api_key=api_key)

tab1, tab2 = st.tabs(["🔍 Analisis & Bedah Musik", "✍️ Ciptakan Lagu & Audio"])

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
    st.header("✍️ Generator Lagu & Audio")
    tema = st.text_input("Apa tema lagu yang diinginkan?", placeholder="Contoh: Cinta budaya Batak Toba di Samosir")
    genre = st.selectbox("Pilih Genre Musik:", ["Pop", "Akustik / Folk", "Dangdut", "Rock", "Jazz", "Reggae Batak", "Gondang Modern"])
    tempo = st.select_slider("Pilih Tempo Lagu:", options=["Lambat", "Sedang", "Cepat"])
    
    if st.button("Ciptakan Lagu Sekarang", key="btn_cipta"):
        if tema.strip() == "":
            st.warning("Silakan isi tema lagu!")
        else:
            with st.spinner("AI sedang menggubah lagu dan menyiapkan komponen audio..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    perintah = (
                        f"Buatkan sebuah lagu utuh dengan tema '{tema}', bergenre {genre}, dengan tempo {tempo}. "
                        f"PENTING: Tuliskan chord gitarnya di atas lirik secara presisi, "
                        f"dan sertakan juga panduan 'Not Angka' (1 2 3 4 5 6 7) di setiap baris liriknya.\n\n"
                        f"Di bagian paling bawah, buatkan satu bagian khusus berjudul '=== PROMPT SUNO AI ===' "
                        f"yang berisi ringkasan lirik tanpa chord dan baris 'Style of Music' yang cocok untuk dimasukkan ke Suno AI agar menjadi lagu jadi."
                    )
                    respons = model.generate_content(perintah)
                    st.success("Lagu Berhasil Diciptakan!")
                    
                    # Menyimpan teks lagu ke session state agar bisa diubah jadi audio bicaranya
                    st.session_state['teks_lagu'] = respons.text
                    st.markdown(respons.text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
                    
    # FITUR AUDIO: Mengubah Lirik Teks Menjadi Audio Suara Digital
    if 'teks_lagu' in st.session_state:
        st.write("---")
        st.subheader("📻 Pemutar Audio Lirik (Text-to-Speech)")
        st.info("Fitur ini akan membacakan panduan lirik lagu yang diciptakan AI di atas ke dalam format audio digital.")
        
        if st.button("Generate Audio Player"):
            with st.spinner("Sedang memproses audio..."):
                # Mengambil baris teks lirik saja (membersihkan format markdown sebisanya)
                teks_bersih = st.session_state['teks_lagu'].split("=== PROMPT SUNO AI ===")[0]
                
                # Menggunakan gTTS untuk mengubah teks menjadi suara audio
                tts = gTTS(text=teks_bersih, lang='id', slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                # Menampilkan widget player audio di Streamlit
                st.audio(fp, format='audio/mp3')
                st.success("Audio siap diputar! Klik tombol play di atas.")
