"""
Video Creator Module
Handles video creation and editing
"""

import cv2
import subprocess
from pathlib import Path
from pydub import AudioSegment
import os

def wrap_text(words, font, max_width):
    """Wrap words to fit within the width of the video frame."""
    lines = []
    current_line = []
    current_line_text = ''
    
    for word in words:
        test_line = (current_line_text + ' ' + word).strip()
        (w, h), _ = cv2.getTextSize(test_line, font, 2, 3)
        
        if w <= max_width:
            current_line.append(word)
            current_line_text = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = [word]
            current_line_text = word
            
    if current_line:
        lines.append(current_line)
    return lines

def pad_image_to_fit(img, target_width, target_height):
    """Pad the image to fit the target dimensions without resizing."""
    height, width, _ = img.shape
    top = (target_height - height) // 2
    bottom = target_height - height - top
    left = (target_width - width) // 2
    right = target_width - width - left
    color = [0, 0, 0]  # Black padding
    padded_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return padded_img

def create_video_from_images_and_audio(image_dir, audio_dir, output_video_path, script, bgm_path, input, bgm_reduce, transition_duration_ms=500):
    # Split the script into sentences
    sentences = script.split('.')
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Get the list of images and sort them
    images = sorted([os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith(".png")])

    # Get the list of audio chunks and sort them
    audio_chunks = sorted([os.path.join(audio_dir, audio) for audio in os.listdir(audio_dir) if audio.endswith(".wav")])

    # Video parameters
    frame_width = 1080
    frame_height = 1920
    frame_rate = 30

    # Create temporary video file using XVID codec
    temp_video_path = "temp_video_output.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_video_path, fourcc, frame_rate, (frame_width, frame_height))

    if not out.isOpened():
        raise Exception("Could not open video writer")

    # Font settings for subtitles
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 5
    text_color = (255, 255, 255)  # White for subtitles
    border_color = (0, 0, 0)  # Black border for subtitles

    # Font settings for title
    title_text_color = (0, 0, 0)  # Black text for the title
    title_bg_color = (255, 255, 255)  # White background for the title
    title_font_scale = 2
    title_font_thickness = 5

    # Initialize final audio track with first chunk
    final_audio = AudioSegment.from_wav(audio_chunks[0])
    current_position_ms = len(final_audio)

    # Process each image and its corresponding sentence
    for i in range(len(images)):
        # Load and process current image
        img = cv2.imread(images[i])
        if img is None:
            raise Exception(f"Could not read image: {images[i]}")

        # Pad the image to fit the video size
        img = pad_image_to_fit(img, frame_width, frame_height)

        # Load current audio chunk
        if i > 0:
            current_audio = AudioSegment.from_wav(audio_chunks[i])
            final_audio = final_audio + current_audio
            current_position_ms += len(current_audio)

        # Add title to the image
        title_text = f"POV: AI on\n {input}"
        title_lines = title_text.split("\n")

        # Calculate the size for both lines
        title_size_1 = cv2.getTextSize(title_lines[0], font, title_font_scale, title_font_thickness)[0]
        title_size_2 = cv2.getTextSize(title_lines[1], font, title_font_scale, title_font_thickness)[0]

        # Calculate the x position for centering the title for both lines
        title_x_1 = (frame_width - title_size_1[0]) // 2
        title_x_2 = (frame_width - title_size_2[0]) // 2

        # Set y position for the two lines
        title_y_1 = 100  # Position the first line near the top
        title_y_2 = title_y_1 + title_size_1[1] + 10  # Position the second line below the first one

        # Draw background rectangle for the title
        rect_x1 = min(title_x_1, title_x_2) - 10
        rect_y1 = title_y_1 - title_size_1[1] - 10
        rect_x2 = max(title_x_1 + title_size_1[0], title_x_2 + title_size_2[0]) + 10
        rect_y2 = title_y_2 + 10
        cv2.rectangle(img, (rect_x1, rect_y1), (rect_x2, rect_y2), title_bg_color, -1)

        # Add title text
        cv2.putText(img, title_lines[0], (title_x_1, title_y_1), font, title_font_scale, title_text_color, title_font_thickness, cv2.LINE_AA)
        cv2.putText(img, title_lines[1], (title_x_2, title_y_2), font, title_font_scale, title_text_color, title_font_thickness, cv2.LINE_AA)


        # Get current sentence
        if i < len(sentences):
            current_sentence = sentences[i] + '.'  # Add period back
            words = current_sentence.split()

            # Calculate frames for current audio segment
            current_audio_duration = len(final_audio) if i == 0 else len(AudioSegment.from_wav(audio_chunks[i]))
            total_frames = int(current_audio_duration / 1000 * frame_rate)

            # Create frames with full sentence
            for frame_num in range(total_frames):
                current_frame = img.copy()

                # Wrap the sentence
                wrapped_lines = wrap_text(words, font, frame_width - 100)
                subtitle_height = len(wrapped_lines) * 60
                y_position = (frame_height - subtitle_height) // 2

                # Display each line
                for line_idx, line in enumerate(wrapped_lines):
                    line_text = ' '.join(line)
                    text_size = cv2.getTextSize(line_text, font, font_scale, font_thickness)[0]
                    text_x = (frame_width - text_size[0]) // 2
                    text_y = y_position + (line_idx * 60)

                    # Add text border and main text
                    cv2.putText(current_frame, line_text, (text_x - 2, text_y - 2), font, font_scale, 
                              border_color, font_thickness + 2, cv2.LINE_AA)
                    cv2.putText(current_frame, line_text, (text_x, text_y), font, font_scale, 
                              text_color, font_thickness, cv2.LINE_AA)

                out.write(current_frame)

        # Add transition if not the last image
        if i < len(images) - 1:
            next_img = cv2.imread(images[i + 1])
            if next_img is None:
                raise Exception(f"Could not read next image: {images[i + 1]}")
            next_img_padded = pad_image_to_fit(next_img, frame_width, frame_height)

            transition_frames = int((transition_duration_ms / 1000) * frame_rate)
            for t in range(transition_frames):
                alpha = t / transition_frames
                blended_frame = cv2.addWeighted(img, 1 - alpha, next_img_padded, alpha, 0)
                out.write(blended_frame)

            silence = AudioSegment.silent(duration=transition_duration_ms)
            final_audio = final_audio + silence
            current_position_ms += transition_duration_ms

    # Close video writer
    out.release()

    # Load background music
    bgm = AudioSegment.from_file(bgm_path)

    # Get the duration of the final narration audio
    narration_duration = len(final_audio)

    # Loop the BGM if it's shorter than the narration
    if len(bgm) < narration_duration:
        repetitions = (narration_duration // len(bgm)) + 1
        bgm = bgm * repetitions

    # Trim BGM to match narration length
    bgm = bgm[:narration_duration]

    # Lower BGM volume (adjust the -20 value to make BGM louder or quieter)
    bgm = bgm - bgm_reduce  # Reduce volume by 20 dB

    # Overlay BGM with narration
    final_audio = final_audio.overlay(bgm)

    # Export final audio to temporary file
    temp_audio_path = "temp_audio_output.wav"
    final_audio.export(temp_audio_path, format="wav")

    # Combine video and audio with simplified ffmpeg command
    command = [
        "ffmpeg", "-y",
        "-i", temp_video_path,
        "-i", temp_audio_path,
        "-c:v", "mpeg4",
        "-c:a", "aac",
        "-strict", "experimental",
        "-shortest",
        output_video_path
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Video successfully created at {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during video creation: {e.stderr}")