import os
from bing_image_downloader.downloader import download
from moviepy.editor import *


def get_images(query_string):
    download(query_string, limit=5, 
                output_dir='Downloads/Images', adult_filter_off=True,
                force_replace=False, timeout=60, verbose=True)
    path="Downloads/Images/"+query_string
    image_clip=[]
    for x in os.listdir(path):
        if  x.endswith(".jpg"):
        
            print(x)
            image_clip.append (ImageClip(path+"/"+x))
    return image_clip    
