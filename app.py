import streamlit as st
import yt_dlp
import os

DESTINO = "downloads"

def baixar_audio_mp3(url, destino=DESTINO):
    if not os.path.exists(destino):
        os.makedirs(destino)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'http_headers': {
            # Simula navegador moderno
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "audio")
        filename = f"{title}.mp3"
        filepath = os.path.join(destino, filename)
        return title, filepath

st.set_page_config(page_title="YouTube MP3 Downloader", page_icon="🎵")
st.title("🎵 YouTube MP3 Downloader")
st.markdown("Cole a URL de um vídeo do YouTube e baixe o áudio em MP3.")

url = st.text_input("URL do vídeo:")

if st.button("⬇️ Baixar MP3"):
    if not url:
        st.warning("Por favor, insira uma URL válida.")
    else:
        try:
            title, path = baixar_audio_mp3(url)
            with open(path, "rb") as f:
                st.success(f"✅ MP3 '{title}' pronta para ser baixada!")
                st.download_button("📥 Baixar arquivo MP3", f, file_name=os.path.basename(path))
        except Exception as e:
            st.error(f"❌ Erro ao baixar: {e}")
