from Video import get_Video
from audio import get_tts
from moviepy.editor import *

def get_scene(search,tts):

  video=get_Video(search)
  spech=get_tts(tts,search)
  videoclip=[]  
  duration_each_img=spech[0].duration
  try:    
    for x in video:        
      videoclip.append(x.set_duration(duration_each_img).resize( (406,720)))  
    video_clip=concatenate_videoclips(videoclip,method='compose')
    audio_clip = concatenate_audioclips(spech)
    clip = video_clip.set_audio(audio_clip)
    return clip  
    
  except Exception as e: print(e)
