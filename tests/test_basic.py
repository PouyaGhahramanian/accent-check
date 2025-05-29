# tests/test_basic.py

import os
import pytest
from src.audio_extraction import extract_audio
from src.accent_detection import analyze_accent

TEST_VIDEO_PATH = "tests/sample_video.mp4"

@pytest.mark.skipif(not os.path.exists(TEST_VIDEO_PATH), reason="Test video not found")
def test_extract_audio():
    audio_path = extract_audio(TEST_VIDEO_PATH, audio_dir="tests/audio_test")
    assert os.path.exists(audio_path)
    assert audio_path.endswith(".wav")

@pytest.mark.skipif(not os.path.exists(TEST_VIDEO_PATH), reason="Test video not found")
def test_accent_analysis():
    audio_path = extract_audio(TEST_VIDEO_PATH, audio_dir="tests/audio_test")
    result = analyze_accent(audio_path)
    assert "accent" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], (int, float, float))