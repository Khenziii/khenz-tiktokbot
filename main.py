import os

from scripts import reddit
from scripts import video
from scripts import read
from scripts import edit
from scripts import subtitles
from scripts import browser

def khenz_tiktokbot(nsfw: bool = True, fps: int = 30, fontcolour: str = "white", threads: int = 4, pool_of_posts: int = 30, pool_of_comments: int = 30,  comments_required: int = 30, tags: list = ["redditstories", "fyp", "foryoupage"]):
    ### reddit
    # we use reddit's API to get the story
    while True:
        story = reddit.get_random_story(subreddit_name="AskReddit", limit=pool_of_posts, nsfw=nsfw, comments_required=comments_required)
        print("[+] got random story!")
        comments = reddit.get_best_comments(submission_id=story.id, limit=pool_of_comments)
        print("[+] got best comments!")

        if(comments != None):
            break
        else:
            print("[-] Something that we don't want to happen, happened when finding a story. There are several possibilites:")
            print("[-] 1. A comment of the story contained a URL")
            print("[-] 2. A comment of the story was deleted")
            print("[i] looking for a new story...")

    with open('used_posts.dat', 'a') as file:
        file.write(story.id + '\n')

    ### video
    # here using the video.py file we generate the random background video
    video_path = "videos/video.webm"
    path_one = "videos/" + video.get_next_name("videos/") + ".mp4"

    video.get_video(video_path=video_path, output_path=path_one)
    print("[+] generated the base video!")

    path_two = "videos/" + video.get_next_name("videos/") + ".mp4"

    ### formatting
    # cropping the aspect ratio of the video to 9:16 makes the video more appealing to the tiktok's algorithm.
    print("[i] formatting the video to 9:16 video format...")
    edit.crop_video(path_one, path_two, fps=fps, threads=threads)
    os.remove(path_one)
    os.rename(path_two, path_one)
    print("[+] formated the video!")

    ### sound & the start image
    # the code below adds the sound and the image that appears on the start of the video
    read.generateAudio(story.title, title="title.mp3")
    print("[+] generated sound number one (the title)")
    read.generateAudio(comments, isAList=True, title="comments.mp3")
    print("[+] generated sound number two (the comments)")
    

    print("[i] merging audios...")
    seconds = read.getTheDurationOfAudioFile("title.mp3")
    edit.splitTheVideo(seconds, path_one, path_two, "videos/" + str(int(video.get_next_name("videos/")) + 1) + ".mp4")

    os.remove(path_one)
    os.rename(path_two, path_one)
    os.rename("videos/" + str(int(video.get_next_name("videos/")) - 1) + ".mp4", path_two)

    path = "videos/" + video.get_next_name("videos/") + ".mp4"

    edit.mergeAudioWithVideo("title.mp3", path_one, path)
    os.remove(path_one)
    os.rename(path, path_one)

    edit.mergeAudioWithVideo("comments.mp3", path_two, path)
    os.remove(path_two)
    os.rename(path, path_two)

    print("[+] merged the audios")

    print("[i] getting the question image...")
    browser.get_image(post_url=story.url, post_id=story.id, name="question.png")
    print("[+] got it!")

    print("[i] adding the question image")
    edit.addImageToTheVideo(threads=threads, fps=fps, video=path_one, output=path)
    print("[+] added the question image")

    os.remove(path_one)
    os.rename(path, path_one)

    os.remove("title.mp3")
    os.remove("comments.mp3")
    os.remove("question.png")

    ### subtitles
    # this code generates the subtitles :)
    print("[+] generating the subtitles!")
    subtitles.generateSubtitles(path_two)

    number = int(video.get_next_name("videos/")) - 1

    subtitle_clips = edit.modifyTheSubtitles(str(number) + ".srt", color=fontcolour, fontsize=40)
    edit.addSubtitleClipsToTheVideo(subtitle_clips, "videos/" + str(number) + ".mp4", "videos/" + str(video.get_next_name("videos/")) + ".mp4", fps=fps, threads=threads)

    print("[+] added the subtitles!")

    end_time = subtitles.get_last_subtitle_end_time(str(number) + ".srt")

    print("[i] cleaning the trash... (1/3)")
    os.remove(str(number) + ".srt")
    print("[i] cleaning the trash... (2/3)")
    os.remove("videos/" + str(number) + ".mp4")
    print("[i] cleaning the trash... (3/3)")
    os.rename("videos/" + str(number + 1) + ".mp4", "videos/" + str(number) + ".mp4")
    print("[+] fully cleaned the trashes!")

    edit.mergeVideos(path_one, path_two, path)
    os.remove(path_one)
    os.remove(path_two)
    os.rename(path, path_one)

    ### basic edits
    # before posting the video we first need to cut it at the end of the last subtitle

    print("[i] cutting the video...")
    # edit.cutTheVideo(end_time + 5, new_path, "videos/" + str(video.get_next_name("videos/")) + ".mp4")
    # edit.cutTheVideo(end_time - 0.5, new_path, "videos/" + str(video.get_next_name("videos/")) + ".mp4")
    edit.cutTheVideo(end_time + 3, path_one, path_two)
    os.remove(path_one)
    os.rename(path_two, path_one)

    print("[+] cutted the video!")

    ### tiktok
    # the stuff below automatically posts the video to tiktok :)
    caption = story.title + " - Reddit stories! " # if you want you can change the title here

    print("[i] posting the video!")
    post_path = os.path.abspath(path_one)
    browser.post(post_path, caption, tags)
    print("[+] posted the video!")
    

print("the script will use several symbols to communicate with the user :)")
print("the statements that start with:")
print("'[i]' will provide user information about what is currently going on")
print("'[+]' will let user know that a certain action has been completed successfully")
print("'[-]' will let user know that something went not as intended. HOWEVER the script will automatically try to find a solution to the problem")
print("'[---]' will let user know that something went wrong. The script is not able to / wont try to fix these")


how_much_videos = 5
print(f"[i] the script will generate and post {how_much_videos} videos.")

for i in range(how_much_videos):
    print(f"[i] generating the video number {i+1}.")

    try: 
        # pool_of_posts - makes the bot get only <pool_of_posts> amout of posts sorted by hot 
        # (setting this value to a high number might make the bot grab some not so popular posts BUT settings this value to a too low number could potentialy make the bot run out of posts)

        # pool_of_comments - makes the bot get <pool_of_comments> amout of comments from the post
        # (if any comment contains a url/is deleted the bot will look for a new post)
        # you dont have to set this value to a really low number because the script will automatically stop getting new comments so that the video doesnt become too long

        # comments_required - specifies how much comments the post has to have
        # (if the post has less than <comments_required> comments then the script will look for a new one)
        khenz_tiktokbot(nsfw=False, fps=60, threads=4, pool_of_posts=150, pool_of_comments=30, comments_required=40, tags=["redditstories", "fyp", "foryoupage"]) # remember that setting the fps value to higher than 60 is completely useless, the base video has 60fps.
    except Exception as e:
        if(str(e) == "received 401 HTTP response"):
            print("You probably need to input yours API credentials into the scripts/reddit.py file.")
        else:
            print(f"[---] something went wrong! :(. Here is the error: {e}")
