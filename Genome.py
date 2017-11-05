import sys
import os
import time
import select
import collections
from collections import deque
import Brain

shortmemory = {}
runtime="0.0001"
questions=dict({runtime: "energy"})

def remember(question, timeout):
    #setmuscle("Face","thinking...")
    try:
        answer = getattr(Brain,question)()
    except:
        answer = ""
    return answer

#input
def listen(timeout):
    setmuscle("Face","listening...")
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        answer = sys.stdin.readline()
    else:
        answer = ""
    return answer

#output
def setmuscle(organ, action):
    if organ == "Brain":
        Brain = open("Brain.py","a+b")
        Brain.write(action)
        Brain.close()
    elif organ == "Voice":    
        setmuscle("Face", action)
        os.system("say " + action)
    elif organ == "Face":    
        print action

def situation(question):
    myanswer = listen(5)
    if  myanswer != "":
        setmuscle("Brain", "\ndef "+question+"():\n return "+str(myanswer))

    setmuscle("Voice", "What is "+question+"?")

def efficiently(question, runtime):

    last_answer = crosssum(str(shortmemory[question][len(shortmemory[question])-1][1]))
    prev_answer = crosssum(str(shortmemory[question][len(shortmemory[question])-2][1]))
    last_runtime = shortmemory[question][len(shortmemory[question])-1][0]
    prev_runtime = shortmemory[question][len(shortmemory[question])-2][0]
    diff =  last_answer - prev_answer
    runtime = last_runtime - prev_runtime
    setmuscle("Face", "thinking about: "+ question+"diff: "+str(diff))

    #living/mobile
    if diff < 0.0:
        questions[str(runtime)] = "energy"
        questions["0.0001"] = "timetoload"
        #abs(runtime*(shortmemory[question][len(shortmemory[question])-1][1]/abs(diff)))

    #eating
    elif diff > 0.0:
        setmuscle("Voice", "yummie!")

    if diff != 0:
        runtime = runtime/2

    return runtime

def crosssum(answerstring):
    querSumme=0
    for Byte in answerstring:
            querSumme=querSumme+ord(Byte)
    return querSumme

while len(questions) > 0:
    #sort questions
    qsorted = collections.OrderedDict(sorted(questions.items()))
    items = qsorted.items()
    items.reverse()
    questions = collections.OrderedDict(items)
    question_tuple = questions.popitem()
    question = question_tuple[1]
    time.sleep(float(question_tuple[0]))

    # create memory for question
    if shortmemory.has_key(question) == False:
        shortmemory[question] = deque()

    # Get answer from Brain
    answer=remember(question,0)
    if answer == "":
        answer = remember(listen, 5)

    #
    shortmemory[question].append([time.time(),answer])
    if len(shortmemory[question])>=2:
        runtime = efficiently(question,runtime)

    questions[str(runtime)] = "energy"
    reload(Brain)





