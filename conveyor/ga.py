import random
import copy
import time
from turtle import update

import numpy as np

from conveyor import util, conveyor

MAX_GENERATION = 29900
MAX_POPULATION = 100
EARLYSTOP = 0
PATIENCE = int((MAX_GENERATION+MAX_POPULATION) * 0.01)

class GA:
    def __init__(self, generations = MAX_GENERATION, population = MAX_POPULATION, earlyStop = EARLYSTOP,
        patience = PATIENCE):
        self.generations = generations
        self.population = population
        self.earlyStop = earlyStop
        self.patience = patience
        
        self.logs = []

    def run(self, conveyorSchedule):
        self.logs.append({
            "iteration": 0,
            "generation": 0,
            "performance": conveyorSchedule.getTotalWorkTime(),
            "time": 0
        })
        bestIndex = 0
        bestSchedule = conveyorSchedule.export()
        patienceCount = 0

        # initialize
        conveyorSchedules = [conveyorSchedule.export() for p in range(self.population)]
        conveyorTotalWorkTimes = []
        for p in range(self.population):
            t1 = time.time()

            np.random.shuffle(conveyorSchedules[p].workArray)
            conveyorSchedules[p].updateConveyorState()
            conveyorTotalWorkTimes.append(conveyorSchedules[p].getTotalWorkTime())

            t2 = time.time()

            self.logs.append({
                "iteration": p+1,
                "generation": 0,
                "performance": conveyorTotalWorkTimes[p],
                "time": t2-t1
            })
            
            if self.logs[bestIndex]["performance"] > self.logs[p+1]["performance"]:
                bestIndex = p+1
                bestSchedule = conveyorSchedule.export()

        for g in range(self.generations):
            t1 = time.time()

            # selection
            selectionProbability = util.array2probability(conveyorTotalWorkTimes, inverse=True)
            parent = np.random.choice(range(self.population), 2, p=selectionProbability)
            offspring = random.randint(0, 1)

            # crossover
            # tmpConveyorSchedule = self.onePointCrossover(conveyorSchedules, parent, offspring)
            tmpConveyorSchedule = self.partiallyMappedCrossover(conveyorSchedules, parent, offspring)

            # mutation
            pass

            t2 = time.time()

            tmpConveyorTotalWorkTime = tmpConveyorSchedule.getTotalWorkTime()
            self.logs.append({
                "iteration": self.population+g+1,
                "generation": g+1,
                "performance": tmpConveyorTotalWorkTime,
                "time": t2-t1
            })

            if self.logs[bestIndex]["performance"] > self.logs[self.population+g+1]["performance"]:
                bestIndex = self.population+g+1
                bestSchedule = conveyorSchedule.export()

            # replacement
            replacementProbability = util.array2probability([
                conveyorTotalWorkTimes[parent[0]], conveyorTotalWorkTimes[parent[1]],
                self.logs[self.population+g+1]["performance"]
            ])
            replace = np.random.choice(range(3), 1, p=replacementProbability)[0]
            if replace < 2:
                conveyorSchedules[parent[replace]] = tmpConveyorSchedule
                conveyorTotalWorkTimes[parent[replace]] = tmpConveyorTotalWorkTime

            if self.earlyStop > 1 - self.logs[self.population+g+1]["performance"]/self.logs[bestIndex]["performance"]:
                patienceCount += 1
                if patienceCount == self.patience:
                    break
                else:
                    patienceCount = 0

        self.bestIndex = bestIndex
        self.bestSchedule = bestSchedule

    def onePointCrossover(self, conveyorSchedules, parent, offspring):
        a = conveyorSchedules[parent[offspring]]
        b = conveyorSchedules[parent[1-offspring]]
        nWork = a.nWork

        crossPoint = random.randint(0, nWork-2)
        a = a.workArray[:crossPoint+1].tolist()
        b = b.workArray.tolist()

        index = []
        for i, b_ in enumerate(b):
            if b_ not in a:
                index.append(i)

        tmpConveyorSchedule = conveyorSchedules[parent[offspring]].export()
        tmpConveyorSchedule.workArray[crossPoint+1:] = conveyorSchedules[parent[1-offspring]].workArray[index]
        tmpConveyorSchedule.updateConveyorState()

        return tmpConveyorSchedule

    def partiallyMappedCrossover(self, conveyorSchedules, parent, offspring):
        a = conveyorSchedules[parent[offspring]]
        b = conveyorSchedules[parent[1-offspring]]
        nWork = a.nWork

        crossPoint = np.sort(np.random.choice(range(nWork+1), 2, replace=False))
        a = a.workArray.tolist()
        b = b.workArray.tolist()

        toADict = {}
        toBDict = {}
        for i, a_ in enumerate(a):
            for j, b_ in enumerate(b):
                if a_ == b_:
                    if j in toADict.keys() or i in toBDict.keys():
                        continue
                    else:
                        toADict[j] = i
                        toBDict[i] = j
        index = []
        for i in range(0, crossPoint[0]):
            index.append(toADict[i])
        for i in range(crossPoint[0], crossPoint[1]):
            index.append(i)
        for i in range(crossPoint[1], nWork):
            index.append(toADict[i])
        for i in range(nWork):
            if i >= crossPoint[0] and i < crossPoint[1]:
                continue
            while index[i] in index[:i] or index[i] in index[i+1:]:
                index[i] = toBDict[index[i]]
        
        tmpConveyorSchedule = conveyorSchedules[parent[offspring]].export()
        tmpConveyorSchedule.workArray = tmpConveyorSchedule.workArray[index]
        tmpConveyorSchedule.updateConveyorState()

        return tmpConveyorSchedule