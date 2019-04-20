import speech_recognition as sr
global transcript

from Naked.toolshed.shell import execute_js, muterun_js, run_js
transcript=''
from word2number import w2n
r=sr.Recognizer()
with sr.Microphone() as source:
    while "addyu" not in transcript:
        audio=r.listen(source)
        print(transcript)
        try:
            transcript=r.recognize_google(audio)
            testy= transcript.split()
            if (testy[0]=='add') and len(testy)>=5:
                i=4;
                food= ''
                while(i<len(testy)):
                    food+= testy[i]
                    i=i+1
                print("food: " + food)
                print("quantity: " + testy[1] + " " + testy[2])
                quan= w2n.word_to_num(testy[1])
                quan=str(quan)
                print("Quantity: " +quan)
                print("'" + food + "'" + " " + quan + " " + testy[2])
                muterun_js('node/index2.js', "'" + food.lower() + "'" + " " + quan + " " + testy[2])
                print("updated")
            if testy[0]=='remove' and len(testy)>=5:
                i=4;
                food= ''
                while(i<len(testy)):
                    food+= testy[i]
                    i=i+1
                print("food: " + food)
                print("quantity: " + testy[1] + " " + testy[2])
                quan= w2n.word_to_num(testy[1])
                quan=str(quan)
                print("Quantity: " +quan)
                print("'" + food + "'" + " " + quan + " " + testy[2])
                muterun_js('node/remove2.js', "'" + food.lower() + "'" + " " + quan)
                print("updated")
        except:
            continue
##        try:
##            transcript=r.recognize_google(audio)
##            testy= transcript.split()
##            if(testy[0]=='add'):
##                print("food: "+ ' '.join(testy[2:]))
##                foodname=' '.join(testy[2:])
##                try:
##                    quan= w2n.word_to_num(transcript)
##                    quan=str(quan)
##                    print("Quantity: " +quan)
##                except:
##                    print ("Voice not recognized")
##                #muterun_js('node/index.js', "'" + itemdescription + "'")
##            if testy[0]=='remove':
##                print("food: "+ ' '.join(testy[2:]))
##                try:
##                    quan= w2n.word_to_num(transcript)
##                    quan=str(quan)
##                    print("Quantity: " +quan)
##                except:
##                    print ("Voice not recognized")
##                
##                
##            print(transcript)
##        except:
##            continue
##
