## DISCLAIMER !!!

As of 04/07/2024, it's been over a year since I have written this code. Looking back at it, there's defienietely lots of room for improvement. Here are the most important things:

1. This codebase surely should contain a Dockerfile that'd make using the app easier. Ideally, a GitHub workflow which'd automatically build a docker image and push it to [Docker Hub](https://hub.docker.com/).
2. Using geckodriver was a mistake. Assuming, that tiktok provides valid documentation, using their's API seems far more reasonable.
3. Both `geckodriver_stuff/` and `fonts/` shouldn't be version controlled.
4. Further development will be almost impossible without tests. Under no circumstances should the developer have to run the whole app in order to check if certain behaviour is working. Lots of tests are needed here, they also might get integrated into CI/CD. 
5. The code should follow basic conventions. Such as:
- DRY ("don't repeat yourself") principle. An example of this is the `without_post.py` file, which could be easily included in `main.py` (the posting behaviour should be controlled via a setting),
- hardcoding secrets. Reddit's API credentials should be stored in a environment variable.
- overwriting OS's environment variables. I have no idea why I did this, but overwriting `$TMPDIR` is for sure a mistake.

However, this doesn't mean that the app shouldn't be used at all! It's still functional. I probably won't ever bother to improve this old codebase, however if you'd like to contribute, I'm always going to happily review PRs!

## khenz-tiktokbot

khenz-tiktokbot is a simple and easy to mod bot that automatically generates and posts videos to tiktok.

## Installation

Here is a list of software that the script requires:

1. FireFox
2. geckodriver (you need to put it in `geckodriver_stuff/`)
3. FFmpeg
4. Python
5. Python packages (they're frozen in `requirements.txt`)
6. imagemagick
7. A reddit's API app

## Usage

After installing everything needed, you have to place a ~9 minutes long video in `videos/video.webm`; then run `browsersetup.py`, accept the cookies, log onto your tiktok account and finally close FireFox. After logging in, run `browsertest.py`, if you're logged in, then you shall be all setup :)

Now you can execute `main.py` to generate and post videos.

You can also edit a couple of things (such as the font color, font, fontsize, NSFW setting, etc..) in `main.py` :).

## Contact

You can find the developer here: discord - "khenzii" :D

