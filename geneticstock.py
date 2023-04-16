import random
import time
from datetime import timedelta
import os
import glob

fileOne = r'historicalstockprices'
os.chdir(r'historicalstockprices')
my_files = glob.glob('*.txt')
fileMat = []
for i in my_files:
    fileTwo = open(i)
    fileList = fileTwo.read().split("\n")
    fileList = fileList[2:]
    
    fileMat.append(fileList)

for i in range(len(fileMat)):
    for b in range(len(fileMat[i])):
        fileMat[i][b] = float(fileMat[i][b])

geno = ['s010&e000&m000','s000&e010&m000','s000&e000&m010','s010&e010&m000','s010&e000&m020','s025|e015&m000','s030|e030|m030','s010&s025|e000','s900&e950|m950','s008&e008|m050']

MAX_POPULATION = 50
MAX_GENERATION = 200
MUTATION = .01
COPY_RATE = .2

def SMA(N, LLC, offset):
    summation = sum(fileMat[LLC][N - offset:N])
    simple_moving_average = summation / offset

    if simple_moving_average < fileMat[LLC][N]:
        return True
    else:
        return False
    

def EMA(N, LLC, offset):
    summation = 0.0
    denominator = 0.0
    alpha = 2 / (N + 1)
    for i in range(offset+1):
        summation += ((1 - alpha) ** i) * fileMat[LLC][N-(i+1)]
        denominator += ((1 - alpha) ** i)
    exponential_moving_average = summation / denominator
    
    if exponential_moving_average < fileMat[LLC][N]:
        return True
    else:
        return False

def MAX(N, LLC, offset):
    max = 0
    for i in range(offset + 1):
        if max < (fileMat[LLC][N - (i+1)]):
            max = (fileMat[LLC][N - (i+1)])
    
    if max < fileMat[LLC][N]:
        return True
    else:
        return False


def initialPopulation():
    population = []
    for i in range(MAX_POPULATION):
        inidividual = ""
        for j in range(14):
            chance = random.random()
            if(j == 0 or j == 5 or j == 10):
                if chance < .33:
                    inidividual += 's'
                elif (chance > .33 and chance < .66):
                    inidividual += 'm'
                else:
                    inidividual += 'e'
            elif(j == 4 or j == 9):
                if chance < .5:
                    inidividual += '&'
                else:
                    inidividual += '|'
            else:
                randomNumber = random.randint(0, 9)
                inidividual += str(randomNumber)
        population.append(inidividual)
    return population

def fitness(pop): #going to return an array the size of the given population that will hold each fitness, or the total money gained for each genome
    gains = [0] * (len(pop))
    invested = [0] * (len(pop))
    for i in range(len(pop)): #check each genotype in the array
        capital = [20000] * 25
        ruleOne = pop[i][0]
        ruleTwo = pop[i][5]
        ruleThree = pop[i][10]
        operandOne = pop[i][4]
        operandTwo = pop[i][9]
        ruleOneDays = int(pop[i][1:4])
        ruleTwoDays = int(pop[i][6:9])
        ruleThreeDays = int(pop[i][11:14])
        offsetOne = ruleOneDays
        offsetTwo = ruleTwoDays
        offsetThree = ruleThreeDays
        useless1 = False
        useless2 = False
        useless3 = False

        for k in range(len(fileMat)): #go through all 25 txt files with each rule
            endDate = False
            while(endDate == False): #go through the individual txt file until end date is reached
                if ruleOne == 's': #check which letter is being used for each section
                    if offsetOne > 0 and ruleOneDays < len(fileMat[k])-1: #make sure that it isn't a dud
                        oneChoice = SMA(ruleOneDays,k,offsetOne)
                        ruleOneDays += 1
                    elif offsetOne == 0 and operandOne == '&':
                        oneChoice = True
                        useless1 = True
                    elif offsetOne == 0 and operandOne == '|':
                        oneChoice = False
                        useless1 = True
                    else:
                        oneChoice = False
                        useless1 = True

                elif ruleOne == 'e':
                    if offsetOne > 0 and ruleOneDays < len(fileMat[k])-1:
                        oneChoice = EMA(ruleOneDays,k,offsetOne)
                        ruleOneDays += 1
                    elif offsetOne == 0 and operandOne == '&':
                        oneChoice = True
                        useless1 = True
                    elif offsetOne == 0 and operandOne == '|':
                        oneChoice = False
                        useless1 = True
                    else:
                        oneChoice = False
                        useless1 = True
                else:
                    if offsetOne > 0 and ruleOneDays < len(fileMat[k])-1:
                        oneChoice = MAX(ruleOneDays,k,offsetOne)
                        ruleOneDays += 1
                    elif offsetOne == 0 and operandOne == '&':
                        oneChoice = True
                        useless1 = True
                    elif offsetOne == 0 and operandOne == '|':
                        oneChoice = False
                        useless1 = True
                    else:
                        oneChoice = False
                        useless1 = True

                if ruleTwo == 's':
                    if offsetTwo > 0 and ruleTwoDays < len(fileMat[k])-1:
                        twoChoice = SMA(ruleTwoDays,k,offsetTwo)
                        ruleTwoDays += 1
                    elif offsetTwo == 0 and operandOne == '&':
                        twoChoice = True
                        useless2 = True
                    elif offsetTwo == 0 and operandOne == '|':
                        twoChoice = False
                        useless2 = True
                    else:
                        twoChoice = False
                        useless2 = True
                elif ruleTwo == 'e':
                    if offsetTwo > 0 and ruleTwoDays < len(fileMat[k])-1:
                        twoChoice = EMA(ruleTwoDays,k,offsetTwo)
                        ruleTwoDays += 1
                    elif offsetTwo == 0 and operandOne == '&':
                        twoChoice = True
                        useless2 = True
                    elif offsetTwo == 0 and operandOne == '|':
                        twoChoice = False
                        useless2 = True
                    else:
                        twoChoice = False
                        useless2 = True
                else:
                    if offsetTwo > 0 and ruleTwoDays < len(fileMat[k])-1:
                        twoChoice = MAX(ruleTwoDays,k,offsetTwo)
                        ruleTwoDays += 1
                    elif offsetTwo == 0 and operandOne == '&':
                        twoChoice = True
                        useless2 = True
                    elif offsetTwo == 0 and operandOne == '|':
                        twoChoice = False
                        useless2 = True
                    else:
                        twoChoice = False
                        useless2 = True

                if ruleThree == 's':
                    if offsetThree > 0 and ruleThreeDays < len(fileMat[k])-1:
                        threeChoice = SMA(ruleThreeDays,k,offsetThree)
                        ruleThreeDays += 1
                    elif offsetThree == 0 and operandTwo == '&':
                        threeChoice = True
                        useless3 = True
                    elif offsetThree == 0 and operandTwo == '|':
                        threeChoice = False
                        useless3 = True
                    else:
                        threeChoice = False
                        useless3 = True
                elif ruleThree == 'e':
                    if offsetThree > 0 and ruleThreeDays < len(fileMat[k])-1:
                        threeChoice = EMA(ruleThreeDays,k,offsetThree)
                        ruleThreeDays += 1
                    elif offsetThree == 0 and operandTwo == '&':
                        threeChoice = True
                        useless3 = True
                    elif offsetThree == 0 and operandTwo == '|':
                        threeChoice = False
                        useless3 = True
                    else:
                        threeChoice = False
                        useless3 = True
                else:
                    if offsetThree > 0 and ruleThreeDays < len(fileMat[k])-1:
                        threeChoice = MAX(ruleThreeDays,k,offsetThree)
                        ruleThreeDays += 1
                    elif offsetThree == 0 and operandTwo == '&':
                        threeChoice = True
                        useless3 = True
                    elif offsetThree == 0 and operandTwo == '|':
                        threeChoice = False
                        useless3 = True
                    else:
                        threeChoice = False
                        useless3 = True
                

                if operandOne == '&': #check operands
                    oneTwo = oneChoice and twoChoice
                else:
                    oneTwo = oneChoice or twoChoice

                if operandTwo == '&':
                    twoThree = oneTwo and threeChoice
                else:
                    twoThree = oneTwo or threeChoice

                if(twoThree): #based on the operands together, we buy
                    if ruleOneDays < len(fileMat[k]): #make sure it one isnt out of range on the last iteration
                        capital[k] -= fileMat[k][ruleOneDays-1] #take from capital, add to investment
                        invested[i] += fileMat[k][ruleOneDays-1]
                    if ruleTwoDays < len(fileMat[k]):
                        capital[k] -= fileMat[k][ruleTwoDays-1]
                        invested[i] += fileMat[k][ruleTwoDays-1]
                    if ruleThreeDays < len(fileMat[k]):
                        capital[k] -= fileMat[k][ruleThreeDays-1]
                        invested[i] += fileMat[k][ruleThreeDays-1]
                else: #we sell
                    if invested[i] == 0: #if theres nothing to sell
                        count = 0
                    else: #if we got invested money
                        gains[i] += invested[i]
                        invested[i] = 0

                if capital[k] < 20000 and gains[i] > 0: #keep capital capped off at 20 grand
                    dif = float(20000 - capital[k])
                    if dif > gains[i]:
                        capital[k] += gains[i]
                        gains[i] = 0
                    else:
                        capital[k] += dif
                        gains[i] -= dif

                if (ruleOneDays == len(fileMat[k])-1 or ruleTwoDays == len(fileMat[k])-1 or ruleThreeDays == len(fileMat[k])-1) or (ruleOneDays > len(fileMat[k])-1 and ruleTwoDays > len(fileMat[k])-1 and ruleThreeDays > len(fileMat[k])-1): #if even one hit the cap, stop it all
                    if offsetOne == 0 or offsetTwo == 0 or offsetThree == 0:
                        gains[i] += invested[i]
                        invested[i] = 0
                        gains[i] = gains[i] / 2
                    else:
                        gains[i] += invested[i]
                        invested[i] = 0
                    useless1 = False
                    useless2 = False
                    useless3 = False
                    endDate = True
                if useless1 and useless2 and useless3: #if all turn to be duds, only some are useless and some others just hit the peak and became useless
                    endDate = True
    return gains

n = fitness(geno)
for i in range(len(n)):
    print("Fitness of ", geno[i], " is ", n[i])
                  

#check each day in chunks of whatever rule wants
#run each rule separatley and compare the true or false
#if buy, buy across all days that apply, else sell across all days, if no rule is applied sell (which should be nothing)
#keep a tab of capital and gains
#keep track of how much u have in a company at a certain time
#keep repeating for each genotype for every company and year
#one genotype should constantly be taking and putting in to capital and gains
