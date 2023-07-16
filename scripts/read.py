from gtts import gTTS
import pydub

def getTheDurationOfAudioFile(file: str):
    audio = pydub.AudioSegment.from_file(file)
    duration_seconds = audio.duration_seconds

    return duration_seconds


def generateAudio(text, title: str = "tts_generated.mp3", isAList: bool = False):
    if(isAList == True):
        text = fromListToString(text)

    try: 
        tts = gTTS(text)
    except AssertionError: # who even cares about assertion errors, lol :>
        generateAudio(text=text, isAList=isAList, title=title)

    tts.save(title)

def fromListToString(thelist):
    text = ""

    for i in range(len(thelist)):
        if(thelist[i].endswith(".") or thelist[i].endswith("!") or thelist[i].endswith("?")):
            text += f"Answer {i+1}. {thelist[i]} "
        else:
            text += f"Answer {i+1}. {thelist[i]}. "
        

        if(len(text) >= 1000):
            break

    return text