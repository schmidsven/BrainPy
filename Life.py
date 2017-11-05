#!/usr/bin/env python
# coding=UTF-8
import math, subprocess, time, os, psutil
from collections import deque
from nltk.corpus import wordnet

#------------------GENOM----------------------------------------------
class Something:
    def __init__(self, shortdata, longdata, trustvalue):
            self.shortdata = shortdata
            self.longdata = longdata
            self.trustvalue =  trustvalue

class Question:
    def __init__(self, question, trustvalue):
            self.question = question
            self.answers = []
            self.trustvalue = trustvalue
    def __repr__(self):
            return repr((self.question, self.answers, self.bestanswer, self.trustvalue))

class Answer:
    def __init__(self, answer, identity):
            self.answer = answer
            self.identity = identity
            self.trustvalue = identity.trustvalue
    def __repr__(self):
            return repr((self.answer, self.identity, self.trustvalue))

def getSensor(sensor):

    if sensor == "energy":
        p = subprocess.Popen(["ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
        output = p.communicate()[0]
        o_max = [l for l in output.splitlines() if 'MaxCapacity' in l][0]
        o_cur = [l for l in output.splitlines() if 'CurrentCapacity' in l][0]
        b_max = float(o_max.rpartition('=')[-1].strip())
        b_cur = float(o_cur.rpartition('=')[-1].strip())
        charge = b_cur / b_max
        charge_threshold = int(math.ceil(10 * charge))
        return charge

    elif sensor == "temperature":
        temperature = subprocess.check_output(["/Applications/TemperatureMonitor.app/Contents/MacOs/tempmonitor", "-c", "-l", "-a"]);
        temperature = temperature.splitlines()
        for tempsensor in temperature:
            tempsensor = tempsensor.split(":")
            if tempsensor[0]=="SMC MAIN HEAT SINK 2":
                insidetemp=tempsensor[1].split(" ")
                insidetemp=insidetemp[1]
            elif  tempsensor[0]=="SMC BATTERY":
                outsidetemp=tempsensor[1].split(" ")
                outsidetemp=outsidetemp[1]
        return insidetemp

    elif sensor == "cpuload":
        return str(psutil.cpu_percent())

    elif sensor == "look":
        camdata=0
        return camdata

    elif sensor == "hear":
        micdata=0
        return micdata

    elif sensor == "feel":
        preasure=0
        return preasure

def setActor(action):

    if action == move:
        return 0

    elif action == call:
        return 0

# self-consiousness initially given to the answers from myself
Poise = 100

# Amount of basic trust Me initially gives to other Identities
BasicTrust = 100

Globalclock = 1

Inventory = []
Inventory.append(Something("Me", "BrainPy", Poise))
#Identities.append(Identity("Daddy", BasicTrust))

QuestionQueue = deque()

#QuestionQueue.append(Question("Me needs energy"))
#QuestionQueue.append(Question("Me needs temperatureregulation"))
QuestionQueue.append(Question("Me needs cpuusage", 0))



#-----------END OF GENOM----------------------------------------------






#input
#-----------LANGUAGE--------------------------------------------------
def understand(questionStr):
    # CC  coordinating conjunction    and
    # CD  cardinal number     1, third
    # DT  determiner  the
    # EX  existential there   there is
    # FW  foreign word    d’hoevre
    # IN  preposition/subordinating conjunction   in, of, like
    # JJ  adjective   big
    # JJR     adjective, comparative  bigger
    # JJS     adjective, superlative  biggest
    # LS  list marker     1)
    # MD  modal   could, will
    # NN  noun, singular or mass  door
    # NNS     noun plural     doors
    # NNP     proper noun, singular   John
    # NNPS    proper noun, plural     Vikings
    # PDT     predeterminer   both the boys
    # POS     possessive ending   friend‘s
    # PRP     personal pronoun    I, he, it
    # PRP$    possessive pronoun  my, his
    # RB  adverb  however, usually, naturally, here, good
    # RBR     adverb, comparative     better
    # RBS     adverb, superlative     best
    # RP  particle    give up
    # TO  to  to go, to him
    # UH  interjection    uhhuhhuhh
    # VB  verb, base form     take
    # VBD     verb, past tense    took
    # VBG     verb, gerund/present participle     taking
    # VBN     verb, past participle   taken
    # VBP     verb, sing. present, non-3d     take
    # VBZ     verb, 3rd person sing. present  takes
    # WDT     wh-determiner   which
    # WP  wh-pronoun  who, what
    # WP$     possessive wh-pronoun   whose
    # WRB     wh-abverb   where, when

    text = nltk.word_tokenize(questionStr)
    words = nltk.pos_tag(text)
    for word in words:
        print word

    for word_meaning in wordnet.synsets(questionStr):
        print word_meaning.definition

    return 'what'
#---------------------------------------------------------------------

#Audio Output
def say(questionStr):
    os.system('say ' + questionStr + '?')
    try:
            print questionStr
            answer = raw_input()
            return answer
    except:
            # timeout
            return

#Suche nach
def find(IdentityName):

    if IdentityName=="Daddy":
        return Identities[1]

    #look -> 
    #move -> 
    #call ->

#Frage an Anderen
def ask(identityObj, questionObj):
    words = questionObj.question.split()
    who = words[0]
    what = words[2]

    if identityObj is Identities[0]:
        answer = Answer(identityObj.identity + " says " + feel(what), identityObj)
    elif identityObj is Identities[1]:
        answer = Answer(identityObj.identity+ " says "+ say(questionObj.question), identityObj)
    
    answer.trustvalue = identityObj.trustvalue

    return answer 

def possibility(currentQuestion, answer):
    foundAnswers=0;
    # wir prüfen wie oft diese antwort bisher vorkam
    for pastAnswer in currentQuestion.answers:
        if pastAnswer.answer == answer.answer:
            foundAnswers+=1

    # und setzen das Ergebnis ins Verhältnis zu allen Antworten
    # 0 = unwahrscheinlich
    # 1 = wahrscheinlich

    allAnswers=len(currentQuestion.answers)
    possible = float(foundAnswers) / float(allAnswers)
    return possible

def average(currentQuestion, answer):
    foundAnswers=0;
    # wir prüfen wie oft diese antwort bisher vorkam
    for pastAnswer in currentQuestion.answers:
        if pastAnswer.answer == answer.answer:
            foundAnswers+=1

    # und setzen das Ergebnis ins Verhältnis zu allen Antworten
    allAnswers=len(currentQuestion.answers)
    possibility = 1-(float(foundAnswers) / float(allAnswers))
    return possibility

def between(currentQuestion, answer):
    foundAnswers=0;
    # wir prüfen wie oft -- die Quersumme -- diese antwort bisher vorkam
    for pastAnswer in currentQuestion.answers:
        if crosssum(pastAnswer.answer) == crosssum(answer.answer):
            foundAnswers+=1

    # und setzen das Ergebnis ins Verhältnis zu allen Antworten
    allAnswers=len(currentQuestion.answers)
    possibility = 1-(float(foundAnswers) / float(allAnswers))
    return possibility


def crosssum(answerstring):
    querSumme=0
    for Byte in answerstring:
            querSumme=querSumme+ord(Byte)
    return querSumme


def predict(currentQuestion):
    # Ich erwarte...

    # irgendwas zwischen max und min
    #answer = between(currentQuestion,answer)

    # irgendwas durchschnittliches
    #answer = average(currentQuestion)

    # irgendwas wahrscheinliches  
    #expectedAnswer = possibility(currentQuestion,answer)

    # das selbe wie zuvor
    if len(currentQuestion.answers)>0 :
        answer = currentQuestion.answers[len(currentQuestion.answers)-1]
    else:
        answer = Answer("Keine Ahnung",Identities[0])
        answer.trustvalue = 0 

    return answer


#Fragen des Lebens beantworten
while len(questionQueue) > 0:

    # Aktuelle Situation erfassen 
    currentQuestion = questionQueue.popleft()

    # predict answer
    predictedAnswer = predict(currentQuestion)
    
    # ask yourself
    answer = ask(Identities[0], currentQuestion)
    
    # save in brain
    currentQuestion.answers.append(answer)
    
    # Aktuelle Situation bewerten
    # Erwartung erfüllt?
    trustLossValue = 0
    if answer.answer == predictedAnswer.answer:
        currentQuestion.trustvalue += 1 
        answer.identity.trustvalue += 1
        trustLossValue = "as expected!"
    else:
        trustLossValue = answer.trustvalue - predictedAnswer.trustvalue
        trustLossValue = trustLossValue/2
        currentQuestion.trustvalue -= abs(trustLossValue)
        if currentQuestion.trustvalue < 0:
            currentQuestion.trustvalue = 0

        answer.identity.trustvalue -= abs(trustLossValue)
        if answer.identity.trustvalue < 0:
            answer.identity.trustvalue = 0

    #time.sleep(max(0,currentQuestion.trustvalue))

    # adjust State
    output = ""
    output += currentQuestion.question +"("+ str(max(0,currentQuestion.trustvalue)) +"%)" +"? "
    output += answer.answer +"! "
    output += str(answer.trustvalue)
    output += " --- expected "+ str(predictedAnswer.answer) 
    output += " " + str(predictedAnswer.trustvalue)
    output += " ("+ str(trustLossValue) +")"
    print output

    questionQueue.append(currentQuestion)


