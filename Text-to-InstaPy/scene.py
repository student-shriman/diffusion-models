from Image import get_images
from audio import get_tts
from moviepy.editor import *

def get_scene(search,tts):

  img=get_images(search)
  spech=get_tts(tts,search)
  imageclip=[]
  
  try:
    duration_each_img=spech[0].duration/len(img)
    for x in img:        
      imageclip.append(x.set_duration(duration_each_img).resize( (406,720)))
  
    video_clip=concatenate_videoclips(imageclip,method='compose')
    audio_clip = concatenate_audioclips(spech)
    clip = video_clip.set_audio(audio_clip)
    return clip  
    
  except Exception as e: print(e)
