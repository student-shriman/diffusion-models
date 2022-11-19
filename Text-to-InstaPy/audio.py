import os
import requests
from common import mkdir
import uuid
from moviepy.editor import *
import json
# api-endpoint

api_key = open('env.json',)
data = json.load(api_key)
def getijt(ijt):
    
    URL = "https://api.fakeyou.com/"
    getwav= requests.get(URL+"tts/job/"+ijt,headers={"accept":"application/json","content-Type": "application/json"})
    hjson2=getwav.json()
    wavurl=hjson2["state"]["maybe_public_bucket_wav_audio_path"]
    if wavurl != None:
        return wavurl
    else:
        return ( getijt(ijt))

def get_tts(query_string,search):
    URL = "https://api.fakeyou.com/"
    creds={"username_or_email":data["fakeyou_user"],"password":data["fakeyou_password"]}
    DATA={
    "uuid_idempotency_token":str(uuid.uuid4()),
    "tts_model_token":data["fakeyou_voiceactor"],
    "inference_text":query_string
        }

    
    r = requests.post(url = URL+"login", json=creds)
    res_login=r.json()['success']
    if res_login==True:
      
        handler=requests.post(URL+"tts/inference",json=DATA)
        ijt=handler.json()["inference_job_token"]
        # getwav= requests.get(URL+"tts/job/"+ijt,headers={"accept":"application/json","content-Type": "application/json"})
        # hjson2=getwav.json()
        wavurl=getijt(ijt)
        content=requests.get("https://storage.googleapis.com/vocodes-public"+wavurl)
        flder="Downloads/audio"
        mkdir(flder)
        FILE_TO_SAVE_AS = flder+"/"+search+".wav" #s
        with open(FILE_TO_SAVE_AS, "wb") as f:     
            f.write(content.content)

        audio_clip=[]
        path="Downloads/audio/"
        for x in os.listdir(path):
            if  x.endswith(search+".wav"):
            # Prints only text file present in My Folder
                print(x)
                audio_clip.append(AudioFileClip(path+"/"+search+".wav"))
        return audio_clip    #return x 		

    else:
        print("failed")