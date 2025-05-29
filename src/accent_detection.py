import torch
from speechbrain.pretrained import EncoderClassifier
import soundfile as sf
import torchaudio
import torchaudio.transforms as T
import torch.nn.functional as F

classifier = EncoderClassifier.from_hparams(
    source="Jzuluaga/accent-id-commonaccent_ecapa",
    savedir="pretrained_models/accent-id-commonaccent_ecapa"
)

def analyze_accent(audio_path):
    print(f"Analyzing accent for {audio_path}")
    
    waveform_np, sample_rate = sf.read(audio_path)
    
    if len(waveform_np.shape) > 1:
        waveform_np = waveform_np.mean(axis=1)
    
    waveform = torch.tensor(waveform_np, dtype=torch.float32).unsqueeze(0)

    if sample_rate != 16000:
        resampler = T.Resample(orig_freq=sample_rate, new_freq=16000).to(torch.float32)
        waveform = resampler(waveform)
        sample_rate = 16000 

    out_prob, score, index, predicted_accent = classifier.classify_batch(waveform)
    normalized_probs = F.softmax(out_prob.squeeze(), dim=0)
    
    all_labels = classifier.hparams.label_encoder.decode_ndim(
        torch.arange(len(out_prob.squeeze()))
    )

    raw_scores = {
        label: float(prob)
        for label, prob in zip(all_labels, out_prob.squeeze().tolist())
    }

    return {
        "accent": predicted_accent,
        "confidence": round(float(score) * 100, 2),
        "details": raw_scores
    }

if __name__ == '__main__':
    test_audio = "tests/audio_test/sample_video.wav"
    result = analyze_accent(test_audio)
    print(result)
