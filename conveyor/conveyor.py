import random
import time
from tkinter import W

import numpy as np

class ConveyorSchedule:
	def __init__(self):
		pass

	def initConveyorSchedule(self, nWork=10, nProcess=6, mode="random"):
		self.workList, self.workType = self.generateConveyorSchedule(nWork, nProcess, mode)
		self.workArray = np.array([wL["time"] for wL in self.workList])
		self.nWork, self.nProcess = self.workArray.shape
		self.updateConveyorState()
		_, self.nSequence = self.conveyor.shape

	def generateConveyorSchedule(self, nWork=10, nProcess=6, mode="random"):
		minimumTime, maximumTime = 10, 300
		probabilityTimeWeightsReset = 0.05

		workList = []
		workType = {}
		workTypeCursor = 0
		for i in range(nWork):
			if i == 0 or random.random() < probabilityTimeWeightsReset:
				timeWeights = [random.randint(minimumTime, maximumTime) for j in range(nProcess)]
				workTypeName = "%x"%(workTypeCursor)
				workType[workTypeName] = {"time":timeWeights, "sort":[[] for j in range(nProcess-1)]}
				workTypeCursor += 1
			
			work = {}
			work["type"] = workTypeName
			work["time"] = []
			for timeWeight in timeWeights:
				tmpTime = np.random.normal(timeWeight, np.log(timeWeight))
				work["time"].append(tmpTime if tmpTime > 0 else 0)
			workList.append(work)
		
		return workList, workType

	def swap(self, a, b):
		self.conveyor[a, a:a+self.nProcess], self.conveyor[b, b:b+self.nProcess] = self.workArray[b], self.workArray[a]  		
		self.workArray[[a,b]] = self.workArray[[b,a]]

	def updateConveyorState(self):
		self.conveyor, self.conveyorMask = self.getConveyorMatrix()

	def getConveyorMatrix(self):
		conveyor = np.zeros((self.nWork, self.nProcess+(self.nWork-1)))
		conveyorMask = np.zeros((self.nWork, self.nProcess+(self.nWork-1)))

		index = np.zeros((self.nWork, self.nProcess)).astype(np.int32)
		processIndex = np.arange(self.nProcess)
		workIndex = np.arange(self.nWork)
		index += processIndex
		index += workIndex.reshape(-1, 1)

		conveyor[workIndex.reshape(-1,1), index] += self.workArray
		conveyorMask[workIndex.reshape(-1, 1), index] += 1
		
		return conveyor, conveyorMask

	def getTotalWorkTime(self):
		return sum(np.amax(self.conveyor, axis=0))  		

	def export(self):
		conveyorSchedule = ConveyorSchedule()
		conveyorSchedule.workList, conveyorSchedule.workType = self.workList, self.workType
		conveyorSchedule.workArray = self.workArray.copy()
		conveyorSchedule.nWork, conveyorSchedule.nProcess = self.nWork, self.nProcess
		conveyorSchedule.conveyor, conveyorSchedule.conveyorMask = self.conveyor.copy(), self.conveyorMask.copy()
		_, conveyorSchedule.nSequence = self.conveyor.shape

		return conveyorSchedule
