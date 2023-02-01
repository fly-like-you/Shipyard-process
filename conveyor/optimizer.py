import random
import time
import copy

import numpy as np

from conveyor import util

MAX_ITERATION = 30000
EARLYSTOP = 0
PATIENCE = int(MAX_ITERATION * 0.01)

class Optimizer:
	def __init__(self, iterations = MAX_ITERATION, earlyStop = EARLYSTOP, patience = PATIENCE):
		self.iterations = iterations
		self.earlyStop = earlyStop
		self.patience = patience

		self.logs = []

class RandomSearch(Optimizer):
	def __init__(self, iterations = MAX_ITERATION, earlyStop = EARLYSTOP, patience= PATIENCE):
		super().__init__(iterations, earlyStop, patience)

	def run(self, conveyorSchedule):
		conveyorSchedule = copy.deepcopy(conveyorSchedule)
		self.logs.append({
			"iteration": 0,
			"performance": conveyorSchedule.getTotalWorkTime(),
			"time": 0
		})

		bestIndex = 0
		bestSchedule = conveyorSchedule
		patienceCount = 0
		for i in range(self.iterations):
			t1 = time.time()

			workIndex = np.arange(conveyorSchedule.nWork)
			np.random.shuffle(workIndex)
			conveyorSchedule.workArray = conveyorSchedule.workArray[workIndex]
			conveyorSchedule.updateConveyorState()

			t2 = time.time()

			self.logs.append({
				"iteration": i+1,
				"performance": conveyorSchedule.getTotalWorkTime(),
				"time": t2-t1
			})

			if self.logs[bestIndex]["performance"] > self.logs[i+1]["performance"]:
				bestIndex = i+1
				bestSchedule = copy.deepcopy(conveyorSchedule)

			if self.earlyStop > 1 - self.logs[i+1]["performance"]/self.logs[bestIndex]["performance"]:
				patienceCount += 1
				if patienceCount == self.patience:
					break
			else:
				patienceCount = 0
		self.bestIndex = bestIndex				
		self.bestSchedule = bestSchedule


class TwoOPT(Optimizer):
	def __init__(self, iterations = MAX_ITERATION, earlyStop = EARLYSTOP, patience= PATIENCE):
		super().__init__(iterations, earlyStop, patience)

	def run(self, conveyorSchedule):
		conveyorSchedule = copy.deepcopy(conveyorSchedule)
		self.logs.append({
			"iteration": 0,
			"performance": conveyorSchedule.getTotalWorkTime(),
			"time": 0
		})

		bestIndex = 0
		bestSchedule = conveyorSchedule
		patienceCount = 0
		for i in range(self.iterations):
			t1 = time.time()

			workIndex = np.arange(conveyorSchedule.nWork)
			np.random.shuffle(workIndex)
			conveyorSchedule.workArray = conveyorSchedule.workArray[workIndex]
			conveyorSchedule.updateConveyorState()

			while True:
				conveyorScheduleTotalWorkTime = conveyorSchedule.getTotalWorkTime()
				beforeConveyorScheduleTotalWorkTime = conveyorScheduleTotalWorkTime
				for j in range(conveyorSchedule.nWork-1):
					conveyorSchedule.swap(j, j+1)
					tmpConveyorScheduleTotalWorkTime = conveyorSchedule.getTotalWorkTime()

					if conveyorScheduleTotalWorkTime > tmpConveyorScheduleTotalWorkTime:
						conveyorScheduleTotalWorkTime = tmpConveyorScheduleTotalWorkTime
					else:
						conveyorSchedule.swap(j, j+1)
				if beforeConveyorScheduleTotalWorkTime == conveyorScheduleTotalWorkTime:
					break

			t2 = time.time()

			self.logs.append({
				"iteration": i+1,
				"performance": conveyorSchedule.getTotalWorkTime(),
				"time": t2-t1
			})

			if self.logs[bestIndex]["performance"] > self.logs[i+1]["performance"]:
				bestIndex = i+1
				bestSchedule = copy.deepcopy(conveyorSchedule)

			if self.earlyStop > 1 - self.logs[i+1]["performance"]/self.logs[bestIndex]["performance"]:
				patienceCount += 1
				if patienceCount == self.patience:
					break
			else:
				patienceCount = 0
		self.bestIndex = bestIndex				
		self.bestSchedule = bestSchedule

class UniformDeviation(Optimizer):
	def __init__(self, iterations = MAX_ITERATION, earlyStop = EARLYSTOP, patience= PATIENCE):
		super().__init__(iterations, earlyStop, patience)

	def run(self, conveyorSchedule):
		conveyorSchedule = copy.deepcopy(conveyorSchedule)
		self.logs.append({
			"iteration": 0,
			"performance": conveyorSchedule.getTotalWorkTime(),
			"time": 0
		})
		processCountSum = np.sum(conveyorSchedule.conveyorMask, axis=0)

		bestIndex = 0
		bestSchedule = conveyorSchedule
		patienceCount = 0
		conveyorScheduleTotalWorkTime = conveyorSchedule.getTotalWorkTime()
		for i in range(self.iterations):
			t1 = time.time()

			processSum = np.sum(conveyorSchedule.conveyor, axis=0)
			processMean = processSum/processCountSum

			processDeviation = np.copy(conveyorSchedule.conveyor)
			for j in range(conveyorSchedule.nSequence):
				processDeviation[conveyorSchedule.conveyorMask[:, j]>0, j] -= processMean[j]
			processDeviation = np.absolute(processDeviation)				

			processDeviationSum = np.sum(processDeviation, axis=0)
			processDeviationMean = util.nan2zero(processDeviationSum/processCountSum)

			sequenceProbability = util.array2probability(processDeviationMean)
			sequenceChoice = np.random.choice(conveyorSchedule.nSequence, 1, p=sequenceProbability)[0]

			workIndex = [j for j, cm in enumerate(conveyorSchedule.conveyorMask[:, sequenceChoice]) if cm == 1]
			if len(workIndex) == 1:
				workChoice = workIndex[0]
			else:
				workProbability = util.array2probability(processDeviation[conveyorSchedule.conveyorMask[:, sequenceChoice]>0, sequenceChoice])
				workChoice = np.random.choice(workIndex, 1, p=workProbability)[0]
			
			errorCollect = []
			for j in range(conveyorSchedule.nWork):
				error = sum(np.absolute(processMean[j:j+conveyorSchedule.nProcess] - conveyorSchedule.workArray[workChoice]))
				error_ = sum(np.absolute(processMean[workChoice:workChoice+conveyorSchedule.nProcess] - conveyorSchedule.workArray[j]))
				errorCollect.append(error+error_)
			swapProbability = util.array2probability(errorCollect, inverse=True)
			swapChoice = np.random.choice(range(conveyorSchedule.nWork), 1, p=swapProbability)[0]

			conveyorSchedule.swap(workChoice, swapChoice)

			tmpConveyorScheduleTotalWorkTime = conveyorSchedule.getTotalWorkTime()

			if conveyorScheduleTotalWorkTime > tmpConveyorScheduleTotalWorkTime:
				conveyorScheduleTotalWorkTime = tmpConveyorScheduleTotalWorkTime
			else:
				conveyorSchedule.swap(workChoice, swapChoice)

			t2 = time.time()

			self.logs.append({
				"iteration": i+1,
				"performance": conveyorSchedule.getTotalWorkTime(),
				"time": t2-t1
			})

			if self.logs[bestIndex]["performance"] > self.logs[i+1]["performance"]:
				bestIndex = i+1
				bestSchedule = copy.deepcopy(conveyorSchedule)

			if self.earlyStop > 1 - self.logs[i+1]["performance"]/self.logs[bestIndex]["performance"]:
				patienceCount += 1
				if patienceCount == self.patience:
					break
			else:
				patienceCount = 0
		self.bestIndex = bestIndex				
		self.bestSchedule = bestSchedule

class UniformDeviationHalf(Optimizer):
	def __init__(self, iterations = MAX_ITERATION, earlyStop = EARLYSTOP, patience= PATIENCE):
		super().__init__(iterations, earlyStop, patience)

	def run(self, conveyorSchedule):
		conveyorSchedule = copy.deepcopy(conveyorSchedule)
		self.logs.append({
			"iteration": 0,
			"performance": conveyorSchedule.getTotalWorkTime(),
			"time": 0
		})
		processCountSum = np.sum(conveyorSchedule.conveyorMask, axis=0)

		bestIndex = 0
		bestSchedule = conveyorSchedule
		patienceCount = 0
		conveyorScheduleTotalWorkTime = conveyorSchedule.getTotalWorkTime()
		for i in range(self.iterations):
			t1 = time.time()

			processSum = np.sum(conveyorSchedule.conveyor, axis=0)
			processMean = processSum/processCountSum

			workChoice = np.random.choice(np.arange(conveyorSchedule.nWork), 1)[0]
			
			errorCollect = []
			for j in range(conveyorSchedule.nWork):
				error = sum(np.absolute(processMean[j:j+conveyorSchedule.nProcess] - conveyorSchedule.workArray[workChoice]))
				error_ = sum(np.absolute(processMean[workChoice:workChoice+conveyorSchedule.nProcess] - conveyorSchedule.workArray[j]))
				errorCollect.append(error+error_)
			swapProbability = util.array2probability(errorCollect, inverse=True)
			swapChoice = np.random.choice(range(conveyorSchedule.nWork), 1, p=swapProbability)[0]

			conveyorSchedule.swap(workChoice, swapChoice)

			tmpConveyorScheduleTotalWorkTime = conveyorSchedule.getTotalWorkTime()

			if conveyorScheduleTotalWorkTime > tmpConveyorScheduleTotalWorkTime:
				conveyorScheduleTotalWorkTime = tmpConveyorScheduleTotalWorkTime
			else:
				conveyorSchedule.swap(workChoice, swapChoice)

			t2 = time.time()

			self.logs.append({
				"iteration": i+1,
				"performance": conveyorSchedule.getTotalWorkTime(),
				"time": t2-t1
			})

			if self.logs[bestIndex]["performance"] > self.logs[i+1]["performance"]:
				bestIndex = i+1
				bestSchedule = copy.deepcopy(conveyorSchedule)

			if self.earlyStop > 1 - self.logs[i+1]["performance"]/self.logs[bestIndex]["performance"]:
				patienceCount += 1
				if patienceCount == self.patience:
					break
			else:
				patienceCount = 0
		self.bestIndex = bestIndex				
		self.bestSchedule = bestSchedule