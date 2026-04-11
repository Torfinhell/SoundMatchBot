"""
Embedding extraction service using CLMR ONNX model.
"""

import os
import torch
import torchaudio
import urllib.request
import onnxruntime as ort
import numpy as np
from backend.config import settings


class EmbeddingExtractor:
    def __init__(self):
        self.model_path = "clmr_sample-cnn.onnx"
        self._ensure_model()
        self.session = ort.InferenceSession(self.model_path)
        self.target_length = 59049
        self.sample_rate = 22050

    def _ensure_model(self):
        """Download CLMR ONNX model if not exists."""
        if not os.path.exists(self.model_path):
            url = "https://github.com/Spijkervet/CLMR/raw/master/examples/clmr-onnxruntime-web/clmr_sample-cnn.onnx"
            print(f"Downloading CLMR model to {self.model_path}...")
            urllib.request.urlretrieve(url, self.model_path)
            print("Download complete.")
        else:
            print(f"Model already exists at {self.model_path}")

    def preprocess_audio(self, audio_path: str) -> torch.Tensor:
        """
        Preprocess audio file for CLMR model.

        Args:
            audio_path: Path to audio file

        Returns:
            Preprocessed audio tensor of shape (1, 1, target_length)
        """
        # Load audio
        audio, sr = torchaudio.load(audio_path)

        # Resample to target sample rate
        if sr != self.sample_rate:
            resample = torchaudio.transforms.Resample(sr, self.sample_rate)
            audio = resample(audio)

        # Convert to mono if stereo
        if audio.shape[0] > 1:
            audio = torch.mean(audio, dim=0, keepdim=True)

        # Trim/pad to target length
        current_length = audio.shape[1]
        if current_length > self.target_length:
            audio = audio[:, :self.target_length]
        elif current_length < self.target_length:
            padding = self.target_length - current_length
            audio = torch.nn.functional.pad(audio, (0, padding))

        # Add batch dimension: (1, 1, target_length)
        audio = audio.unsqueeze(0)

        return audio

    def extract(self, audio_path: str) -> np.ndarray:
        """
        Extract embedding from audio file.

        Args:
            audio_path: Path to audio file

        Returns:
            Embedding vector (50-dimensional)
        """
        # Preprocess audio
        audio = self.preprocess_audio(audio_path)

        # Run inference
        inputs = {self.session.get_inputs()[0].name: audio.numpy()}
        outputs = self.session.run(None, inputs)

        # Return the embedding
        return outputs[0].squeeze().astype(np.float32)  # Shape: (50,)


# Global instance
embedding_extractor = EmbeddingExtractor()