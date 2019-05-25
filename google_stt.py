import json
import urllib2
import base64
import record

#please change it to you api key!!
api_url = "https://speech.googleapis.com/v1p1beta1/speech:recognize?key=your_api_key" 
record.main()
audio_file = open('asr.wav', 'rb')
def encode_audio(audio):
  audio_content = audio.read()
  return base64.b64encode(audio_content)

audio_base64=encode_audio(audio_file)
voice = {
  "config":
  {
    #"encoding": "ENCODING_UNSPECIFIED",
    "sampleRateHertz": 16000,
    "languageCode": "en-GB"
  },

  "audio":
  {
    "content": audio_base64
  }
}
headers = {'Content-Type': 'application/json'}
request = urllib2.Request(url=api_url, headers=headers, data=json.dumps(voice))
response = urllib2.urlopen(request)
print(response.read())
