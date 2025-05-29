import os
import streamlit as st
from tempfile import NamedTemporaryFile
from audio_extraction import download_and_extract_audio, extract_audio
from accent_detection import analyze_accent

st.set_page_config(page_title="AccentCheck", layout="centered")

with st.expander("ℹ️ How to Use This App"):
    st.markdown("""
    **This app lets you analyze the English accent of a speaker using either a video URL or a video file.**

    ### 🔗 Using a Video URL:
    - You can paste a public video URL (e.g., from Dropbox, Google Drive, direct MP4 links).
    - **Loom videos are supported _only if_ they meet these conditions:**
        - The Loom video must be **publicly shared**.
        - The **Download** option must be enabled by the owner.
        - If possible, provide the **direct MP4 link**, not the standard Loom share link.
    - ❌ _Loom videos without public download enabled will not work due to platform restrictions._

    ### 📁 Uploading a Video File:
    - You can upload a `.mp4`, `.mov`, or `.webm` video file directly.
    - This is the most reliable method if you're unsure about the video link format.

    ---
    If the app shows an error while downloading or analyzing, double-check the video format or try uploading the file instead.
    """)

st.title("🗣️ Accent Check")
st.markdown("Analyze the **English accent** of a speaker from a public video URL or uploaded file.")

tab1, tab2 = st.tabs(["🔗 Analyze from URL", "📁 Upload Video File"])

with tab1:
    video_url = st.text_input("Enter a public video URL (MP4 or Loom):")
    if st.button("Analyze from URL"):
        if not video_url:
            st.warning("Please enter a valid video URL.")
        else:
            with st.spinner("Downloading and processing..."):
                try:
                    audio_path = download_and_extract_audio(video_url)
                    result = analyze_accent(audio_path)
                    st.success("✅ Accent analysis complete!")
                    st.markdown(f"**Predicted Accent:** `{result['accent']}`")
                    st.markdown(f"**Confidence Score:** `{result['confidence']}%`")
                    with st.expander("🔍 Show Raw Scores"):
                        for accent, score in result["details"].items():
                            st.write(f"{accent}: {round(score * 100, 2)}%")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

with tab2:
    uploaded_file = st.file_uploader("Upload a video file (MP4)", type=["mp4", "mov", "webm"])
    if uploaded_file is not None:
        if st.button("Analyze Uploaded File"):
            with st.spinner("Processing uploaded video..."):
                try:
                    with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                        temp_video.write(uploaded_file.read())
                        temp_video_path = temp_video.name
                    
                    audio_path = extract_audio(temp_video_path)
                    result = analyze_accent(audio_path)
                    st.success("✅ Accent analysis complete!")
                    st.markdown(f"**Predicted Accent:** `{result['accent']}`")
                    st.markdown(f"**Confidence Score:** `{result['confidence']}%`")
                    with st.expander("🔍 Show Raw Scores"):
                        for accent, score in result["details"].items():
                            st.write(f"{accent}: {round(score * 100, 2)}%")
                    
                    os.remove(temp_video_path)  # Clean up temp video

                except Exception as e:
                    st.error(f"❌ Error: {e}")
