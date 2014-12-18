import numpy as np
import random
import util

class Sender(object):

	def __init__(self, states, signals, strategy, recordChoices=True, recordStrats=True):
		self.states = states
		self.signals = signals
		self.strategy = strategy
		self._recordChoices = recordChoices
		self._recordStrats = recordStrats
		self._choiceHistory = []
		self._stratHistory = np.array([util.matNormalize(self.strategy)])

	def getSignal(self, state):
		theSig = util.weighted_choice(zip(self.signals, self.strategy[state]))
		#theSig = np.random.choice(self.signals, p=util.normalize(self.strategy[state]))
		if self._recordChoices:
			self._choiceHistory.append((state, theSig))
		return theSig

	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
		self.strategy[prevChoice[0], sum(prevChoice[1])] += amount
		if self._recordStrats:
                    self.recordStrategy()

	def getNormalizedStrategy(self):
		return util.matNormalize(self.strategy)

	def getChoiceHistory(self):
		return self._choiceHistory

	def getStratHistory(self):
		return self._stratHistory

	def getProb(self, sig, state):
		return self.getNormalizedStrategy()[state, sum(sig)]

        def recordStrategy(self):
		self._stratHistory = np.concatenate((self._stratHistory, [self.getNormalizedStrategy()]))


class NegationSender(Sender):

	def __init__(self, states, signals, strategy, func, recordChoices=True, recordStrats=True):
		self.states = states
		self.signals = signals
		self.strategy = strategy
		self.func = func
		self._recordChoices = recordChoices
		self._recordStrats = recordStrats
		self._choiceHistory = []
		self._stratHistory = np.array([util.matNormalize(self.strategy)])
		self._N = len(self.signals)/2
		self._baseSig = self.signals[:self._N]+[[self._N]]

	def getSignal(self, state):
		theSig = list(util.weighted_choice(zip(self._baseSig, self.strategy[state])))
		if theSig == [self._N]:
			#the [-1] is at the very end just because the result of choice will be of the form [i]
			theSig.append(util.weighted_choice(zip(self._baseSig[:-1], self.strategy[self.func.index(state)][:-1]))[-1])
		if self._recordChoices:
			self._choiceHistory.append((state, theSig))
		return theSig

	def getProb(self, sig, state):
		normStrat = self.getNormalizedStrategy()
		if len(sig) == 1:
			return normStrat[state, sum(sig)]
		elif len(sig) == 2:
                        #print normStrat[self.func.index(state)][:-1]
			return normStrat[state, sig[0]] * util.normalize(normStrat[self.func.index(state)][:-1])[sig[1]]

	def getPaid(self, amount):
		prevChoice = self._choiceHistory[-1]
		prevSig = prevChoice[1]
		if len(prevSig) == 1:
			self.strategy[prevChoice[0], sum(prevChoice[1])] += amount
		elif len(prevSig) == 2:
			self.strategy[prevChoice[0], prevChoice[1][0]] += amount
			self.strategy[self.func.index(prevChoice[0]), prevChoice[1][1]] += amount
		if self._recordStrats:
                    self.recordStrategy()

class FixedNegationSender(NegationSender):

    def __init__(self, states, signals, strategy, func, recordChoices=True, recordStrats=False):
        NegationSender.__init__(self, states, signals, strategy, func, recordChoices=True, recordStrats=False)

    def getPaid(self, amount):
	if self._recordStrats:
            self.recordStrategy()


