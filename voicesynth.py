# -*- coding: utf-8 -*-
import gtts
import os
#import subprocess
#import cv2

#Initializing
if os.path.isdir("./Voices") == 0:
    os.mkdir("Voices")
i = 1

#Calculation process
while 1:
    s = str(i)
    savefilename = s.rjust(4, '0')
    savefilename = "./Voices/gttstest" + s + ".mp3"
    print ('Please enter the speech '+ s +"   (enter [>>>exit] to exit.)")
    input_test_word = input('>>>  ')
    if input_test_word == "exit" :
        print("Getting the word EXIT. Now deleting files made in this process")
        break
    if input_test_word == "" :
        print("!!!Plese enter some letters!!!")
        continue
    print("now voice synthesizing")
    speakword = (input_test_word)
    tts = gtts.gTTS(text=speakword, lang="ja")
    tts.save(savefilename)
    #speak
    os.system("start "+savefilename)
    """
    # pick an external mp3 player you have
    soundprogram = "wmp"#"D:\Program Files (x86)\Evil Player\Evil_Player.exe"
    subprocess.call([soundprogram, savefilename])    
    """
    i = i + 1
    
#Delete files and dir.
for var in range(1, i):
    vas = str(var)
    os.remove("./Voices/gttstest" + vas + ".mp3")
while 1:
    if os.listdir('./Voices') == []:
        break
    pass
os.rmdir("Voices")
#os.system("start ./sounds/endcall.mp3")
print("Files and dir have been deleted successfully")
print("program finished")
