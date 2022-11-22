from scene import get_scene
from videoscene import get_scene as Videoscene
from moviepy.editor import *
import json

script = open('script.json',)
scenes= json.load(script)

search_array=[]
tts_array=[]
cliptype=[]

for scene in scenes:
    for i in scenes[scene]:
        if i=="image":
            cliptype.append("1")
            search_array.append(scenes[scene][i]) 
        elif i=="tts":
             tts_array.append(scenes[scene][i]) 
        else:
            cliptype.append("0")
            search_array.append(scenes[scene][i])  
                  
zipped_scene = zip(search_array, tts_array,cliptype)
finalclip=[]
for x,y,z in zipped_scene:
    if z=="1":
        finalclip.append(get_scene(x,y))
    else:
        finalclip.append(Videoscene(x,y))

video_clip=concatenate_videoclips(finalclip,method='compose')
video_clip.write_videofile("Video_final.mp4", fps=24)

 








