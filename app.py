from sys import stdout
from threading import Thread
import random, time

malesNameFile = open("names/males", "r")
maleNames = malesNameFile.read().split("\n")

femalesNameFile = open("names/females", "r")
femaleNames = femalesNameFile.read().split("\n")

maleBurnNum = 0
femaleBurnNum = 0
maleDeadNum = 0
femaleDeadNum = 0
marriedNum = 0

def getRandFromLst(list:list):
    return list[random.randint(0, len(list)-1)]

def getCloseAge(list:list, age:int):
    if len(list) == 0: return None
    nearVal = list[0]
    nearNum = abs(list[0].age - age)

    for i in list[1:]:
        if nearNum > abs(i.age - age):
            nearNum = abs(i.age - age)
            nearVal = i
    if nearNum > 10:
        return None
    return nearVal

def getMaleName():
    return maleNames[random.randint(0, len(maleNames)-1)]

def getFemaleName():
    return femaleNames[random.randint(0, len(femaleNames)-1)]

class Human:
    def __init__(self, name:str, gender:bool):
        self.name = name
        self.gender = "male" if gender == True else "female"
        self.age = 0
        self.deadAge = random.randint(0, 25) if random.randint(1, 10) == 7 else random.randint(25, 120)
        self.marrieAge = random.randint(18, 50)
        self.marrieYear = 0
        self.burns = {}
        self.married = False
        self.dead = False
    
    def nextYear(self, marrie = False):
        global maleDeadNum, femaleDeadNum
        if self.dead == True: return
        self.age += 1
        if self.age >= self.deadAge:
            self.dead = True
            if self.gender == "male": maleDeadNum += 1
            else: femaleDeadNum += 1


humans = {
    "males":    [],
    "females":  [],
}
Males = []
Females = []
leftNum = 0
canMarries = {
    "males":    [],
    "females":  [],
}
marrieds = {
    "males":    [],
    "females":  [],
}

def addMale(num:int = 1):
    for i in range(0, num):
        humans["males"].append(Human(getMaleName(), True))

def addFemale(num:int = 1):
    for i in range(0, num):
        humans["females"].append(Human(getFemaleName(), False))

year = 0

def nextYearLoop():
    global maleDeadNum, femaleDeadNum
    global maleBurnNum, femaleBurnNum
    global marriedNum
    global canMarries, marrieds
    global year
    global Males, Females, leftNum

    print("\n\n________Year " + str(year) + "________\n")

    for male in humans["males"]:
        male.nextYear()

    for female in humans["females"]:
        female.nextYear()

    print(str(maleDeadNum) + " males and " + str(femaleDeadNum) + " are dead.")

    Males = [x for x in humans["males"] if x.dead == False]
    Females = [x for x in humans["males"] if x.dead == False]
    leftNum = len(Males)+len(Females)
    
    canMarries = {
        "males":    [x for x in humans["males"] if x.married == False and x.marrieAge <= x.age],
        "females":  [x for x in humans["females"] if x.married == False and x.marrieAge <= x.age],
    }

    marrieds = {
        "males":    [x for x in humans["males"] if x.married != False],
        "females":  [x for x in humans["females"] if x.married != False],
    }

    for female in marrieds["females"]:
        if female.age in female.burns.keys():
            maleNum = 0
            femaleNum = 0
            for child in female.burns[female.age]:
                if child == True:
                    addMale()
                    maleNum += 1
                    maleBurnNum += 1
                elif child == False:
                    addFemale()
                    femaleNum += 1
                    femaleBurnNum += 1
            #print(female.name + " has burn " + str(maleNum) + " boy and " + str(femaleNum) + " girl")

    print(str(maleBurnNum) + " males and " + str(femaleBurnNum) + " females has burn")

    for male in canMarries["males"]:                                                                                #   Marrie
        canMarries = {
            "males":    [x for x in humans["males"] if x.married == False and x.marrieAge <= x.age],
            "females":  [x for x in humans["females"] if x.married == False and x.marrieAge <= x.age],
        }
        female = getCloseAge(canMarries["females"], male.age)
        if female == None: continue
        female.married = male
        burns = {}
        y = female.age + random.randint(1, 5)
        for i in range(random.randint(0, 4)):
            burn = []
            for i in range(random.randint(1, 3)):
                burn.append(True if random.randint(0, 1) == 1 else False)
            burns[y] = burn
            y += random.randint(2, 9)
        female.burns = burns
        male.marrieAge = year
        female.marrieAge = male.marrieAge
        male.married = female
        marriedNum += 1
        #print(male.name + " and " + female.name + " married")

    print(str(marriedNum) + " couples got married")


    print("\n" + str(leftNum) + " humans left.")
    print("________________\n")

    if leftNum == 0:
        print("The apocalypse has come!")
        quit(0)

    maleDeadNum = 0
    femaleDeadNum = 0
    maleBurnNum = 0
    femaleBurnNum = 0
    marriedNum = 0

    time.sleep(1)
    year += 1
    nextYear()
    
addMale(random.randint(100, 150))
addFemale(random.randint(100, 150))

nextYearLoop()