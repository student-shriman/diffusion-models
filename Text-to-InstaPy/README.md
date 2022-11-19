# Text-to-InstaPy
This is my first Python project inspired by This guy https://github.com/iJohnMaged/Text-To-Video-Py

I tried to mix image video and voice to generate the video

FAKE YOU API: https://docs.fakeyou.com/ get your credentials from here to start using this scipt

PIXABAY API : https://pixabay.com/api/docs/ get your API key here 

BING IMAGE DOWNLOAD: https://pypi.org/project/bing-image-downloader/


# CONFIG

Project includes ENV FILE

    "fakeyou_user": "--YOUR FAKEYOU EMAIL--",
 
    "fakeyou_password": "--YOUR FAKEYOU PASSWORD--",
    
     "PIXABAY_API": "--YOUR PIXABAY API KEY--",
     
    "fakeyou_voiceactor":"TM:9msyk3s92yrv" -- Kurzgesagt voice model  https://fakeyou.com/tts/TM:9msyk3s92yrv
    

# Create Scene 
JSON included in the project

    {
    "scene 1":
    {
        "image":"expansion of universe",
        "tts":"In the early 1990s, one thing was fairly certain about the expansion of the universe."
    },

    "scene 2":
    {
        "video":"dark matter",
        "tts":"It might have enough energy density to stop its expansion and recollapse,"
    },

    "scene 3":
    {
        "image":"gravity",
        "tts":"but gravity was certain to slow the expansion as time went on."
    },
    "scene 4":
    {
        "video":"time",
        "tts":"Granted, the slowing had not been observed, but, theoretically,"
    }

    }
# How to run

Create a virtual environment and run


pip3 install -r requirement.txt


Then you can create a script in script.json and run

py text_to_video.py

# Imprtant Note

1. Make scene smaller as API gets consumed and gives error
2. Text to Speech is max for 11 sec only for that create another scene 

# Report Bugs 



