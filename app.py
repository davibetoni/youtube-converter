import streamlit as st
import yt_dlp
import os

DESTINO = "downloads"

def baixar_audio_mp3(url, destino=DESTINO):
    if not os.path.exists(destino):
        os.makedirs(destino)

    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
        # NÃO definimos ffmpeg_location aqui!
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info.get("title", "audio")
        filename = f"{titulo}.mp3"
        return filename, os.path.join(destino, filename)

# Interface
st.title("🎵 YouTube MP3 Downloader")

url = st.text_input("Cole a URL do vídeo do YouTube:")

if st.button("⬇️ Baixar MP3"):
    if not url:
        st.warning("Por favor, insira uma URL válida.")
    else:
        try:
            filename, filepath = baixar_audio_mp3(url)
            with open(filepath, "rb") as f:
                st.success(f"✅ MP3 '{filename}' pronto para ser baixado!")
                st.download_button("📥 Baixar arquivo", f, file_name=filename)
        except Exception as e:
            st.error(f"❌ Erro ao baixar: {e}")
