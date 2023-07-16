from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip
from moviepy.video.fx.all import crop
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pysubs2
import subprocess


def get_video_duration(video_path):
    video = VideoFileClip(video_path)
    duration = video.duration
    video.close()
    return duration

def addImageToTheVideo(threads, fps, video: str, output: str, image: str = "question.png", audio: str = "title.mp3"):
    image_clip = ImageClip(image).resize(0.75).set_position(("center", "center"))
    audio_clip = AudioFileClip(audio)
    video_clip = VideoFileClip(video)

    composite_clip = CompositeVideoClip([video_clip, image_clip.set_start(0).set_end(audio_clip.duration)])
    composite_clip.write_videofile(output, fps=fps, threads=threads)

    audio_clip.close()

def mergeVideos(path_one, path_two, output):
    command = ['ffmpeg', '-i', path_one, '-i', path_two, '-filter_complex',
               '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]',
               '-map', '[outv]', '-map', '[outa]', output]
    
    subprocess.run(command, check=True)

def mergeAudioWithVideo(audio_path, video_path, output_path):
    command = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy',
               '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0', output_path]
    
    subprocess.run(command, check=True)

def modifyTheSubtitles(path_to_the_srt_file, color: str = "white", fontsize: int = 20, max_width: int = 600):
    subs = pysubs2.load(path_to_the_srt_file, encoding="utf-8")
    subtitle_clips = []

    for line in subs:
        start_time = line.start / 1000
        end_time = line.end / 1000
        duration = end_time - start_time
        text = line.text.replace("\\N", "\n")

        if(text.strip() == ""):
            continue

        #clip = TextClip(text, font="fonts/RobotoMono-VariableFont_wght.ttf", fontsize=fontsize, color=color, bg_color="transparent", print_cmd=False, method='caption', 
        #               size=(max_width, None), align='center', stroke_color="black", stroke_width=2)

        clip = TextClip(text, font="fonts/Montserrat-ExtraBoldItalic.ttf", fontsize=fontsize, color=color, bg_color="transparent", print_cmd=False, method='caption', 
                       size=(max_width, None), align='center')

        #clip = TextClip(text, font="fonts/Montserrat-VariableFont_wght.ttf", fontsize=fontsize, color=color, bg_color="transparent", print_cmd=False, method='caption', 
                        #size=(max_width, None), align='center', stroke_color="black", stroke_width=1)
        
        # First font: a basic one with a stroke # Second font: a italic thicker one without a stroke # Third font: a thicker one with a stroke
        # (if you want to use a different font just comment the line starting with "clip" and uncomment the other font by getting rid of the "#")


        clip = clip.set_start(start_time).set_duration(duration).set_position('center')
        subtitle_clips.append(clip)

    return subtitle_clips

def addSubtitleClipsToTheVideo(subtitle_clips, video_path, output_path, fps, threads):
    video = VideoFileClip(video_path)
    final_clip = CompositeVideoClip([video] + subtitle_clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps, threads=threads)

def cutTheVideo(when, video_path, output_path):
    ffmpeg_extract_subclip(video_path, 0, when, targetname=output_path)

def splitTheVideo(when, video_path, output_path_one, output_path_two):
    video_duration = get_video_duration(video_path)

    ffmpeg_extract_subclip(video_path, 0, when, targetname=output_path_one)
    ffmpeg_extract_subclip(video_path, when, video_duration, targetname=output_path_two)

def crop_video(input_path, output_path, fps, threads):
    clip = VideoFileClip(input_path)
    (w, h) = clip.size
    cropped_clip = crop(clip, width=600, height=5000, x_center=w/2, y_center=h/2)
    cropped_clip.write_videofile(output_path, codec="libx264", fps=fps, threads=threads)