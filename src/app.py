import os
import streamlit as st
from tempfile import NamedTemporaryFile
from audio_extraction import download_and_extract_audio, extract_audio
from accent_detection import analyze_accent
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import numpy as np
import av
import soundfile as sf

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

    def get_audio(self):
        if self.frames:
            return np.concatenate(self.frames, axis=1).flatten()
        return None

st.set_page_config(page_title="AccentCheck", layout="centered")

with st.expander("ℹ️ How to Use This App"):
    st.markdown("""
    **This app lets you analyze the English accent of a speaker using a video URL, an uploaded video file, or live voice recording.**

    ### 🔗 Using a Video URL:
    - Paste a public video URL (e.g., Dropbox, Google Drive, or direct MP4 links).
    - **Loom videos are supported _only if_ they meet these conditions:**
        - The Loom video must be **publicly shared**.
        - The **Download** option must be enabled by the owner.
        - Preferably provide the **direct MP4 link**, not just the standard Loom share link.
    - ❌ _Loom videos without public download access will not work._

    ### 📁 Uploading a Video File:
    - Upload `.mp4`, `.mov`, or `.webm` video files directly from your device.
    - This is the most reliable method if you're unsure about URL compatibility.

    ### 🎙️ Recording Your Voice:
    - Use the **Record Voice** tab to speak directly into your microphone.
    - Click **Start Recording**, then **Stop**, and finally **Analyze** to detect your accent.
    - Make sure your browser has microphone permissions enabled.
    - Audio is automatically converted to 16kHz format for accurate analysis.

    ---
    💡 **Tip:** If you see errors while downloading or analyzing, make sure:
    - The video/audio format is supported,
    - The source is publicly accessible,
    - Your microphone is active (for recording).
    """)

st.title("🗣️ Accent Check")
st.markdown("Analyze the **English accent** of a speaker from a public video URL or uploaded file.")

tab1, tab2, tab3 = st.tabs(["🔗 Analyze from URL", "📁 Upload Video File", "🎙️ Record your voice to detect accent"])

with tab1:
    video_url = st.text_input("Enter a public video URL (MP4 or Loom):")
    if st.button("Analyze from URL"):
        if not video_url:
            st.warning("Please enter a valid video URL.")
        else:
            with st.spinner("Downloading and processing..."):
                try:
                    audio_path = download_and_extract_audio(video_url)
                        
                    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                        with open(audio_path, 'rb') as src_file:
                            tmp_audio.write(src_file.read())
                        tmp_audio_path = tmp_audio.name

                    result = analyze_accent(tmp_audio_path)
                    os.remove(tmp_audio_path)

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

                    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                        with open(audio_path, 'rb') as src_file:
                            tmp_audio.write(src_file.read())
                        tmp_audio_path = tmp_audio.name

                    result = analyze_accent(tmp_audio_path)

                    os.remove(temp_video_path)
                    os.remove(tmp_audio_path)

                    st.success("✅ Accent analysis complete!")
                    st.markdown(f"**Predicted Accent:** `{result['accent']}`")
                    st.markdown(f"**Confidence Score:** `{result['confidence']}%`")
                    with st.expander("🔍 Show Raw Scores"):
                        for accent, score in result["details"].items():
                            st.write(f"{accent}: {round(score * 100, 2)}%")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
with tab3:
    st.markdown("🎙️ **Record your voice to detect accent**")
    ctx = webrtc_streamer(
        key="accent-audio",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True},
    )

    if ctx.audio_processor and st.button("Analyze Recorded Voice"):
        audio_data = ctx.audio_processor.get_audio()
        if audio_data is not None:
            with NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                sf.write(tmpfile.name, audio_data, 16000)
                result = analyze_accent(tmpfile.name)
                st.success("✅ Accent analysis complete!")
                st.markdown(f"**Predicted Accent:** `{result['accent']}`")
                st.markdown(f"**Confidence Score:** `{result['confidence']}%`")
                with st.expander("🔍 Show Raw Scores"):
                    for accent, score in result["details"].items():
                        st.write(f"{accent}: {round(score * 100, 2)}%")
        else:
            st.warning("❗ No audio recorded.")