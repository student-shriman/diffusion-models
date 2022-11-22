import requests

API_KEY = '<YOUR_API_KEY>' # Get your API key here: https://app.fliki.ai/account/api
API_URL = 'https://api.fliki.ai/v1'

# Language list
def languageList():
  try:
    headers = {'Authentication': 'Bearer ' + API_KEY}
    r = requests.get(API_URL + '/languages', headers=headers)
    data = r.json()
    return data['data']
  except:
    print('An exception occurred')
  return None

# Dialect list
def dialectList():
  try:
    headers = {'Authentication': 'Bearer ' + API_KEY}
    r = requests.get(API_URL + '/dialects', headers=headers)
    data = r.json()
    return data['data']
  except:
    print('An exception occurred')
  return None

# Voice list
def voiceList(languageId, dialectId):
  try:
    data = {'languageId': languageId, 'dialectId': dialectId}
    headers = {'Authentication': 'Bearer ' + API_KEY}
    r = requests.post(API_URL + '/voices', data=data, headers=headers)
    data = r.json()
    return data['data']
  except:
    print('An exception occurred')
  return None

# Generate audio
def generateAudio(content, voiceId, voiceStyleId = None):
  try:
    data = {'content': content, 'voiceId': voiceId}
    if voiceStyleId:
      data['voiceStyleId'] = voiceStyleId
    headers = {'Authentication': 'Bearer ' + API_KEY}
    r = requests.post(API_URL + '/generate/audio', data=data, headers=headers)
    data = r.json()
    return data['data']
  except:
    print('An exception occurred')
  return None

def main():
  # Get languages
  if True:
    languages = languageList()
    print(languages)

  # Get dialects
  if False:
    dialects = dialectList()
    print(dialects)

  # Get voices
  if False:
    languageId = '61b8b2f54268666c126babc9', # English
    dialectId = '61b8b31c4268666c126bace7', # United States
    voices = voiceList(languageId, dialectId)
    print(voices)

  # Generate audio
  if False:
    content = 'Hello, thank you for giving Fliki API a try!',
    voiceId = '61b8b45a4268666c126bb32b', # English, United States, Sara
    audio = generateAudio(content, voiceId)
    print(audio)

main()
