#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
import os

class recoder:
    NUM_SAMPLES = 2000      #size of pyaudio buffer
    SAMPLING_RATE = 16000    #samping fre.
    LEVEL = 1500         #threshold
    COUNT_NUM = 20    
    SAVE_LENGTH = 8    
    TIME_COUNT = 20     #recording time unit:s. 
    #there are two condation that the recording process will stop,first, time out;second, after a period slience.

    Voice_String = []

    def savewav(self,filename):
        wf = wave.open(filename, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.SAMPLING_RATE) 
        wf.writeframes(np.array(self.Voice_String).tostring()) 
        # wf.writeframes(self.Voice_String.decode())
        wf.close() 

    def recoder(self):
        pa = PyAudio() 
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True, 
            frames_per_buffer=self.NUM_SAMPLES) 
        save_count = 0 
        save_buffer = [] 
        time_count = self.TIME_COUNT
        os.system("echo 1 > /sys/class/leds/status_led/brightness")
        while True:
            time_count -= 1
            string_audio_data = stream.read(self.NUM_SAMPLES) 
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            large_sample_count = np.sum( audio_data > self.LEVEL )
            print(np.max(audio_data))
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH 
            else: 
                save_count -= 1

            if save_count < 0:
                save_count = 0 

            if save_count > 0 : 
                save_buffer.append( string_audio_data ) 
            else: 
            #print save_buffer
                #print "debug"
                if len(save_buffer) > 0 : 
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
            if time_count==0: 
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False
def main():
    r = recoder()
    r.recoder()
    r.savewav("asr.wav")  

if __name__ == "__main__":
    main() 
