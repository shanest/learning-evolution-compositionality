import numpy as np
import random
import util

class Receiver(object):

	def __init__(self, signals, actions, strategy, recordChoices=True, recordStrats=True):
		self.signals = signals
		self.actions = actions 
		self.strategy = strategy
		self._recordChoices = recordChoices
		self._recordStrats = recordStrats
		self._choiceHistory = []
		self._stratHistory = np.array([util.matNormalize(self.strategy)])

	def getAction(self, signal):
		raise NotImplementedError

	def getPaid(self, amount):
		raise NotImplementedError

	def getNormalizedStrategy(self):
		return util.matNormalize(self.strategy)

	def getChoiceHistory(self):
		return self._choiceHistory

	def getStratHistory(self):
		return self._stratHistory

	def getProb(self, act, sig):
		raise NotImplementedError

        def recordStrategy(self):
		self._stratHistory = np.concatenate((self._stratHistory, [self.getNormalizedStrategy()]))



class AtomicReceiver(Receiver):

	def getAction(self, signal):
		theAct = util.weighted_choice(zip(self.actions, self.strategy[sum(signal)]))
                #np.random.choice requires the weights to be probabilities; is normalizing then using this slower than weighted_choice?
                #theAct = np.random.choice(self.actions, p=util.normalize(self.strategy[sum(signal)]))
		if self._recordChoices:
			self._choiceHistory.append((signal, theAct))
		return theAct

	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
		self.strategy[sum(prevChoice[0]), prevChoice[1]] += amount
		if self._recordStrats:
                    self.recordStrategy()

	def getProb(self, act, sig):
		return self.getNormalizedStrategy()[sum(sig), act]


class NegationReceiver(Receiver):

	def __init__(self, signals, actions, strategy, func, recordChoices=True, recordStrats=True):
		Receiver.__init__(self, signals, actions, strategy, recordChoices, recordStrats)
		#define the 'negation' function as any Derangement
		#should I make this a parameter?
		self._func = func
		print(self._func)

	def getAction(self, signal):
		#using signal[-1] covers the len1/2 case uniformly
		theAct = util.weighted_choice(zip(self.actions, self.strategy[signal[-1]]))
                #theAct = np.random.choice(self.actions, p=util.normalize(self.strategy[signal[-1]]))
		if len(signal) == 1:
			self._choiceHistory.append((signal, theAct))
			return theAct
		else:
			self._choiceHistory.append((signal, self._func[theAct]))
			return self._func[theAct]
		
	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
		sig = prevChoice[0]
		if len(sig) == 1:
			self.strategy[sum(sig), prevChoice[1]] += amount
		elif len(sig) == 2:
			self.strategy[sig[1], self._func.index(prevChoice[1])] += amount
		else:
			assert False, "Got to bad place in reinforcment of NegationReceiver"
		if self._recordStrats:
                    self.recordStrategy()

	def getProb(self, act, sig):
		normStrat = self.getNormalizedStrategy()
		if len(sig) == 1:
			return normStrat[sum(sig), act]
		#P(a | [i, j]) = P(f^-1(a) | j)
		elif len(sig) == 2:
			return normStrat[sig[1], self._func.index(act)]


class FunctionReceiver(Receiver):

	def __init__(self, signals, actions, strategy, func, numFuncs=3, recordChoices=True, recordStrats=True):
		Receiver.__init__(self, signals, actions, strategy, recordChoices, recordStrats)
                self._numFuncs = numFuncs
		self._funcs = []
                self._funcHist = []
                #func is a derangement, i.e. a negation
                self._funcs.append(func)
                #range gives the identity function
                self._funcs.append(range(len(actions)))
                #zeros is constant function
                self._funcs.append(np.ones(len(actions), dtype=np.int).tolist())
                self._funcWeights = np.ones((numFuncs))
                print self.actions
		print(self._funcs)

	def getAction(self, signal):
		#using signal[-1] covers the len1/2 case uniformly
		theAct = util.weighted_choice(zip(self.actions, self.strategy[signal[-1]]))
                #theAct = np.random.choice(self.actions, p=util.normalize(self.strategy[signal[-1]]))
		if len(signal) == 1:
			self._choiceHistory.append((signal, theAct))
			return theAct
		else:
                        theFunc = util.weighted_choice(zip(range(self._numFuncs), self._funcWeights))
                        finalAct = self._funcs[theFunc][theAct]
			self._choiceHistory.append((signal, (theFunc, finalAct)))
			return finalAct
		
	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
                #print prevChoice
		sig = prevChoice[0]
                #only reinforce function choice
		if len(sig) == 1:
                        assert True
			#self.strategy[sum(sig), prevChoice[1]] += amount
		elif len(sig) == 2:
                        self._funcWeights[prevChoice[1][0]] += amount
			#self.strategy[sig[1], self._funcs[prevChoice[1][0]].index(prevChoice[1][1])] += amount
		else:
			assert False, "Got to bad place in reinforcment of NegationReceiver"
		if self._recordStrats:
                    self.recordStrategy()
                    #TODO: record funcWeights
                    self._funcHist.append(util.normalize(self._funcWeights))
		
	def getProb(self, act, sig):
		normStrat = self.getNormalizedStrategy()
		if len(sig) == 1:
			return normStrat[sum(sig), act]
		#P(a | [i, j]) = P(f^-1(a) | j)
		elif len(sig) == 2:
                        funcProbs = util.normalize(self._funcWeights)
                        tot = 0.0
                        for i in range(len(funcProbs)):
                            #need to make sure act is in range of func b/c of constant one
                            if act in self._funcs[i]:
                                tot += funcProbs[i] * normStrat[sig[1], self._funcs[i].index(act)]
                        return tot
			#return normStrat[sig[1], self._func.index(act)]
