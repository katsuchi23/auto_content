"""
Main entry point for the video generation system
"""

import torch
import shutil
import random
from pathlib import Path
from src.generators import ImageGenerator, AudioGenerator, generate_story, setup_model
from src.utils import create_video_from_images_and_audio, ensure_output_dirs

def main():
    """Main function to run the video generation process"""
    # Clean up previous outputs
    output_dir = Path("output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
        
    ensure_output_dirs() # create a new directory

    model, tokenizer = setup_model()
    # Get user input
    while True:
        topic = input("Enter your topic: ")
        print("---------------------------------------------\n")
        script = generate_story(topic, model, tokenizer)
        print(script)
        print()

        if input("Do you want to use this script? (y/n): ").lower() == "y":
            title = input("Enter your title: ")
            style = input("Enter your style (pixel / papercut): ")
            break

    # Generate content
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

    image_generator = ImageGenerator(style)
    image_metadata = image_generator.generate_images(script)
    
    audio_generator = AudioGenerator()
    audio_metadata = audio_generator.generate_audio(script)

    # Select background music
    bgm_config = {
        'Sweet_Donut-500audio.com.mp3': 20,
        'Vacation_Vlog_Sound_Track-500audio.com.mp3': 17,
        'Witty_Cartoon-500audio.com.mp3': 15
    }
    
    selected_bgm = random.choice(list(bgm_config.keys()))
    bgm_reduce = bgm_config[selected_bgm]

    # Create final video
    create_video_from_images_and_audio(
        image_dir="src/output/images",
        audio_dir="src/output/audio",
        output_video_path=f"src/output/video/AI on {title}.mp4",
        script=script,
        bgm_path=f"src/assets/bgm/{selected_bgm}",
        input=title,
        bgm_reduce=bgm_reduce,
        transition_duration_ms=200
    )

    torch.cuda.empty_cache()
    torch.cuda.synchronize()

if __name__ == "__main__":
    main()