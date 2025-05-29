import torch
from speechbrain.pretrained import EncoderClassifier

classifier = EncoderClassifier.from_hparams(
    source="Jzuluaga/accent-id-commonaccent_ecapa",
    savedir="pretrained_models/accent-id-commonaccent_ecapa"
)

def analyze_accent(audio_path):
    print(f"Analyzing accent for {audio_path}")
    
    out_prob, score, index, predicted_accent = classifier.classify_file(audio_path)

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
