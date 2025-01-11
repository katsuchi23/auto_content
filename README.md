# 🚀 Auto Content Generation

Welcome to **Auto Content Generation**! 🎥 This project generates videos from user input topics by creating scripts, images, and audio. It integrates various AI models to generate the content, and assembles everything into a cool video with transitions and background music. 🎬✨

I'm using this model for commercial use on tiktok video [TikTok](https://www.tiktok.com/@kei_2306)

I already make sure all the model I used in this project allow commercial usage and fair use, but if there are mistakes please let me know and I will change the model 😁

## 📚 Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Modules](#modules)
- [License](#license)

## 🖥️ Prerequisites

Before diving into the fun, make sure you have the following installed:

- **Python** (>= 3.7) 🐍
- **CUDA** (for GPU support) 🖥️
- **Anaconda** (for environment management) 🧑‍💻

## 🔧 Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/katsuchi23/auto_content.git
   cd auto_content

2. **Set up the Conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate auto_content_env

3. **Install additional dependencies (if any):**
   ```bash
   pip install -r requirements.txt

4. **Ensure you have the necessary CUDA environment for running models like Stable Diffusion and T5. 🎮**

## ▶️ How to Run

Now that you're all set up, it's time to generate some AI-powered videos! 🚀

### Steps:

1. **Navigate to the root directory of the project in the terminal.** 📂

2. **Run the application:**
   To start generating a video, simply run:

   ```bash
   python -m src.main
   ```

### When you run the program, here's what happens:

* You’ll be prompted to input a topic. 📝
* The system will generate a story/script based on the topic using the Mistral-7B language model. 🤖
* It will generate corresponding images for the script using Stable Diffusion. 🖼️
* Then, it will convert the script to audio using text-to-speech (TTS). 🎤
* Finally, all the images and audio will be combined into a cool video with transitions and background music! 🎶🎥

## 🛠️ Usage

### How to use the program:
* Enter your Topic: When prompted, input a topic to generate a story. 🌍
* Select Style: Choose between 
    * "pixel" 🖼️ 
    * "papercut" ✂️ style for the images.
* Script Review: After generating the script, you’ll be asked if you’d like to proceed with it. 😎
Let the AI do its magic and generate your video! ✨

## 🛠️ Personal Modification

### You can change your own parameter to suit your need:
* Using your own LLM 🤖
* Adding your own style image 🖼️
* Modifying image resolution (I'm using 1080 x 1920 for tiktok video)   
* Using your own tts model (I'm using default one)
✨

## 🤖 Model Specifications
Here are the models used for each of the three components of the project:

### 1. Text Generation 📝(Original Model)
* Model: [Mistral-7B Instruct](https://huggingface.co/unsloth/mistral-7b-instruct-v0.3-bnb-4bit) (Fine-tuned on [Wikipedia Dataset](https://huggingface.co/datasets/katsuchi/wikipedia-didyouknow) (Original Dataset) with unsloth)
* Description: This model is used for generating scripts or stories based on the provided topic. It is fine-tuned for instruction-based tasks, making it ideal for creating engaging content.
* Hugging Face Repo: [katsuchi/mistral-7b-instruct-wikipedia-finetune](https://huggingface.co/katsuchi/mistral-7b-instruct-wikipedia-finetune)

### 2. Image Generation 🖼️/sp
* Model: Stable Diffusion XL (Base 1.0)
* Description: This model generates images based on the script text. It supports two distinct styles: "pixel" and "papercut," which you can choose based on your preference.
* Hugging Face Repo: 
    * [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
    * LCM Adapter: [LCM](https://huggingface.co/latent-consistency/lcm-lora-sdxl)
    * Pixel Adapter: [Pixel](https://huggingface.co/nerijs/pixel-art-xl)
    * Papercut Adapter: [Papercut](https://huggingface.co/TheLastBen/Papercut_SDXL)

### 3. Audio Generation 🎤
* Model: SpeechT5 TTS (Text-to-Speech)
* Description: This model converts the generated script into human-like speech. The T5-based SpeechT5 model is capable of generating clear and expressive audio from text.
* Hugging Face Repo: [microsoft/speecht5_tts](https://huggingface.co/microsoft/speecht5_tts)

## 🧑‍💻 Modules

### 1. 🖼️ Image Generator (src/generators/image_generator.py)
* Description: Generates images from your script text using Stable Diffusion. You can choose between "pixel" and "papercut" styles. 🎨
* Dependencies: torch, diffusers, LCMScheduler

### 2. 🎤 Audio Generator (src/generators/audio_generator.py)
* Description: Converts the generated script into speech using the SpeechT5 model and saves it as .wav files. 🎧
* Dependencies: torch, transformers, datasets, soundfile

### 3. ✍️ Text Generator (src/generators/text_generator.py)
* Description: Generates a story or script based on the provided topic using the Mistral-7B language model. 📝
* Dependencies: torch, unsloth

### 4. 🎬 Video Creator (src/utils/video_creator.py)
* Description: Combines images and audio into a video, adding transitions and background music to make it look awesome! 🎶
* Dependencies: cv2, pydub, subprocess

### 5. 🔧 Utilities
* Text Normalizer: Ensures the text is properly formatted for the TTS model, making sure everything sounds smooth. 🧹

### 6. 📝 License
This project is licensed under [LICENSE](https://www.apache.org/licenses/LICENSE-2.0.txt). 🎉 See the LICENSE file for more details. 📝