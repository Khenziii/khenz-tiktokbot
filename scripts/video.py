from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import random
import os

def get_next_name(directory):
    files = os.listdir(directory)

    existing_numbers = [int(file.split(".")[0]) for file in files if file.endswith(".mp4") and file[:-4].isdigit()]
    max_number = max(existing_numbers) if existing_numbers else 0

    segment_name = str(max_number + 1)

    return segment_name

def get_video(video_path, output_path):
    start_time = random.randint(0, int(9 * 60 - 200))
    end_time = start_time + 180

    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)