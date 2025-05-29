# 🗣️ Accent Check

**Accent Check** is a Streamlit web application that identifies the English accent of a speaker from:
- Public video URLs (MP4 or Loom),
- Uploaded video files, or
- Recorded voice input directly from the browser.

This project uses pretrained models from [SpeechBrain](https://huggingface.co/speechbrain) for inference and provides confidence scores for detected accents.

---

## 🌐 Try it Online

The app is hosted on **Streamlit Cloud**. You can try it here:  
👉 [https://accentcheck.streamlit.app](https://accentcheck.streamlit.app)

---

## 🚀 Features

- 🔗 **Video URL Analysis** (MP4, Loom)
- 📁 **Video File Upload Support** (`.mp4`, `.mov`, `.webm`)
- 🎙️ **In-browser Voice Recording**
- 🔍 **Per-Accent Confidence Breakdown**
- ✅ Powered by SpeechBrain and Streamlit

---

## 🧠 Supported Accents

- Australia
- England
- New Zealand
- US
- Wales
- Singapore
- Indian
- Scotland
- Canada
- Philippines
- Hong Kong
- Malaysia
- African
- South Atlantic
- Ireland
- Bermuda

---

## 🛠️ Technologies

- Python 3.11+
- Streamlit
- Torchaudio
- SpeechBrain
- MoviePy
- FFmpeg
- SoundFile
- HuggingFace Hub

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/pouyaghahramanian/accent-check.git
cd accent-check
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note**: Make sure `ffmpeg` is installed and available in your system PATH.

3. Run the Streamlit app:

```bash
streamlit run src/app.py
```

---

## 🧪 Example Usage

1. Open the app in a browser.
2. Choose one of the following options:
    - Paste a direct video URL (MP4 or public Loom link).
    - Upload a video file from your device.
    - Record your voice directly in the browser.
3. Click **Analyze**.
4. The app returns:
    - Predicted accent.
    - Confidence score.
    - Breakdown of scores for each accent.

---

## 🗃️ Directory Structure

```
accent-check/
├── src/
│   ├── app.py                # Streamlit app
│   ├── accent_detection.py   # Core logic for accent detection
│   ├── audio_extraction.py   # Handles audio extraction from video
├── requirements.txt
├── README.md
└── tests/
    └── audio_test/           # Example test files
```

---

## ℹ️ How to Use This App

**This app lets you analyze the English accent of a speaker using a video URL, a video file, or a microphone recording.**

### 🔗 Using a Video URL:
- Paste a public video URL (e.g., from Dropbox, Google Drive, Youtube, Loom, or a direct MP4 link).
- **Loom videos are supported _only if_ they meet these conditions:**
    - The Loom video must be **publicly shared**.
    - The **Download** option must be enabled by the owner.
    - If possible, provide the **direct MP4 link**, not the standard Loom share link.
- ❌ _Loom videos without public download enabled will not work due to platform restrictions._

### 📁 Uploading a Video File:
- Upload a `.mp4`, `.mov`, or `.webm` video file directly.
- This is the most reliable method if you're unsure about the video link format.

### 🎙️ Recording Your Voice:
- Allow microphone access in your browser.
- Record your voice using the built-in recorder.
- Click “Analyze Recorded Voice” to get the results.

---
If the app shows an error while downloading or analyzing, double-check the video format or try uploading the file instead.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License

---

## 🙌 Acknowledgements

- [SpeechBrain](https://github.com/speechbrain/speechbrain)
- [Streamlit](https://streamlit.io/)
- HuggingFace Model: `Jzuluaga/accent-id-commonaccent_ecapa`