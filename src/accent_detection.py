import os
import torch
import numpy as np
from scipy.spatial.distance import cosine
from speechbrain.pretrained import EncoderClassifier
import torchaudio
from sklearn.preprocessing import normalize

classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# todo: american_proto = np.mean([extract_embedding("american1.wav"), extract_embedding("american2.wav")], axis=0)

ACCENT_PROTOTYPES = {
    "American": np.random.rand(192),
    "British": np.random.rand(192),
    "Australian": np.random.rand(192),
}

def extract_embedding(audio_path):

    signal = classifier.load_audio(audio_path)
    embedding = classifier.encode_batch(signal)
    
    embedding = embedding.squeeze().detach().cpu().numpy().flatten()

    return embedding

def classify_accent(embedding):
    embedding = embedding / np.linalg.norm(embedding)

    scores = {}
    for accent, proto in ACCENT_PROTOTYPES.items():
        proto = proto / np.linalg.norm(proto)
        sim = 1 - cosine(embedding, proto)
        scores[accent] = sim

    best_accent = max(scores, key=scores.get)
    confidence = round(scores[best_accent] * 100, 2)
    return best_accent, confidence, scores

def analyze_accent(audio_path):
    print(f"Analyzing accent for {audio_path}")
    embedding = extract_embedding(audio_path)
    accent, confidence, raw_scores = classify_accent(embedding)
    return {
        "accent": accent,
        "confidence": confidence,
        "details": raw_scores
    }

if __name__ == '__main__':
    test_audio = input("Path to .wav audio: ")
    result = analyze_accent(test_audio)
    print(result)