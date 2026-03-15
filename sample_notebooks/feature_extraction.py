"""
Feature extraction using CLMR ONNX model.
Converted from music_extraction.ipynb notebook.
"""

import torch
import torchaudio
import os
import urllib.request
import onnxruntime as ort
import numpy as np


def preprocess_audio(audio_path: str, target_length: int = 59049, sample_rate: int = 22050) -> torch.Tensor:
    """
    Preprocess audio file for CLMR model.

    Args:
        audio_path: Path to audio file
        target_length: Target length in samples (59,049 for CLMR)
        sample_rate: Target sample rate (22,050 Hz for CLMR)

    Returns:
        Preprocessed audio tensor of shape (1, 1, target_length)
    """
    # Load audio
    audio, sr = torchaudio.load(audio_path)

    # Resample to target sample rate
    if sr != sample_rate:
        resample = torchaudio.transforms.Resample(sr, sample_rate)
        audio = resample(audio)

    # Convert to mono if stereo
    if audio.shape[0] > 1:
        audio = torch.mean(audio, dim=0, keepdim=True)

    # Trim/pad to target length
    current_length = audio.shape[1]
    if current_length > target_length:
        audio = audio[:, :target_length]
    elif current_length < target_length:
        padding = target_length - current_length
        audio = torch.nn.functional.pad(audio, (0, padding))

    # Add batch dimension: (1, 1, target_length)
    audio = audio.unsqueeze(0)

    return audio


def download_clmr_model(model_path: str = "clmr_sample-cnn.onnx") -> str:
    """
    Download CLMR ONNX model if not exists.

    Args:
        model_path: Local path to save the model

    Returns:
        Path to the downloaded model
    """
    if not os.path.exists(model_path):
        url = "https://github.com/Spijkervet/CLMR/raw/master/examples/clmr-onnxruntime-web/clmr_sample-cnn.onnx"
        print(f"Downloading CLMR model to {model_path}...")
        urllib.request.urlretrieve(url, model_path)
        print("Download complete.")
    else:
        print(f"Model already exists at {model_path}")

    return model_path


def extract_features(audio_path: str, model_path: str = "clmr_sample-cnn.onnx") -> np.ndarray:
    """
    Extract features from audio using CLMR ONNX model.

    Args:
        audio_path: Path to audio file
        model_path: Path to ONNX model

    Returns:
        Feature vector (50-dimensional for the full model)
    """
    # Ensure model is downloaded
    model_path = download_clmr_model(model_path)

    # Load ONNX model
    session = ort.InferenceSession(model_path)

    # Preprocess audio
    audio = preprocess_audio(audio_path)

    # Run inference
    inputs = {session.get_inputs()[0].name: audio.numpy()}
    outputs = session.run(None, inputs)

    # Return the feature vector
    return outputs[0].squeeze()  # Shape: (50,)


if __name__ == "__main__":
    # Example usage
    audio_file = "sample.wav"  # Replace with actual audio file

    if os.path.exists(audio_file):
        features = extract_features(audio_file)
        print(f"Extracted features shape: {features.shape}")
        print(f"Features: {features}")
    else:
        print(f"Audio file {audio_file} not found. Please provide a valid audio file.")