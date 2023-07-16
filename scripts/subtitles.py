import subprocess
import pysubs2

def generateSubtitles(video_path):
    command = ['auto_subtitle', "--srt_only", "True", "--verbose", "True", "--model", "small", video_path]
    subprocess.run(command)

def get_last_subtitle_end_time(path_to_the_srt_file):
    subs = pysubs2.load(path_to_the_srt_file, encoding="utf-8")
    last_line = subs[-1]
    end_time = last_line.end / 1000
    return end_time