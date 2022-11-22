from common import mkdir
import requests
from moviepy.editor import *
import json
# api-endpoint

api_key = open('env.json',)
data_key = json.load(api_key)

def get_Video(search):
    URL = "https://pixabay.com/api/videos"
       
    PARAMS = {"key":data_key["PIXABAY_API"],
                "q": search
    } 
    r = requests.get(url = URL, params = PARAMS)  
    data = r.json()  
    print(data['hits'][0]['duration'])
    print(data['hits'][0]['videos']['tiny']['url'])
    URL = data['hits'][0]['videos']['tiny']['url']
    flder="Downloads/video"
    mkdir(flder)
    FILE_TO_SAVE_AS = flder+"/"+search+".mp4"
    resp = requests.get(URL) 
    with open(FILE_TO_SAVE_AS, "wb") as f: 
        f.write(resp.content) 

    video_clip=[]
    path="Downloads/video/"
    for x in os.listdir(path):
        if  x.endswith(search+".mp4"):
            print(x)
            video_clip.append(VideoFileClip(path+"/"+search+".mp4"))
    return video_clip   
