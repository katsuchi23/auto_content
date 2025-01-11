"""
Audio Generator Module
Handles text-to-speech conversion
"""

import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import soundfile as sf
from pathlib import Path
from src.utils.text_normalizer import TextNormalizer
from src.utils.ensure_output_dir import ensure_output_dirs

class AudioGenerator:
    def __init__(self):
        """Initialize the audio generator with T5 models"""
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        
        # Load speaker embeddings
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
        
        self.text_normalizer = TextNormalizer()
        ensure_output_dirs()

    def generate_audio(self, script):
        """
        Generate audio from script text
        Args:
            script (str): Input text to convert to speech
        Returns:
            list: List of metadata for generated audio chunks
        """
        sentences = [s.strip() + '.' for s in script.split('.') if s.strip()]
        audio_metadata = []

        for i, sentence in enumerate(sentences):
            print(f"\nGenerating audio for sentence {i+1}/{len(sentences)}:")
            print(f"Text: {sentence}")

            audio_chunk = self._generate_audio_chunk(sentence)
            audio_path = Path("src/output/audio") / f"chunk_{i}.wav"
            sf.write(str(audio_path), audio_chunk, samplerate=16000)
            
            audio_metadata.append({
                "chunk_index": i,
                "text": sentence,
                "audio_path": str(audio_path),
                "duration": len(audio_chunk) / 16000
            })

        self._cleanup()
        return audio_metadata

    def _generate_audio_chunk(self, text):
        """Generate audio for a single chunk of text"""
        normalized_text = self.text_normalizer.normalize_numbers(text)
        
        inputs = self.processor(text=normalized_text, return_tensors="pt", padding=True)
        speech = self.model.generate_speech(
            inputs["input_ids"], 
            self.speaker_embeddings, 
            vocoder=self.vocoder
        )
        return speech.squeeze(0).cpu().numpy()

    def _cleanup(self):
        """Clean up GPU memory"""
        torch.cuda.empty_cache()
        del self.model
        del self.vocoder
        torch.cuda.empty_cache()