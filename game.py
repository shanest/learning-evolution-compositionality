import numpy as np
import random
import util

from sender import Sender, NegationSender, FixedNegationSender, SemiFixedSender
from receiver import * 

class Game(object):

	def __init__(self, sender, receiver, states, signals, actions, payoffs=[], stateProbs=[], recordHist=False):
		self.sender = sender
		self.receiver = receiver
		self.states = states
		self.signals = signals
		self.actions = actions
		self.payoffs = payoffs
		#state probabilities; uniform...
		self.stateProbs = util.normalize(np.ones(len(self.states)))
		self._recordHist = recordHist
		self._payHistory = []
		#maxposspay depends on diagonal being max possible 
		self._maxPossPay = sum([self.stateProbs[i]*self.payoffs[i, i] for i in self.states])

	def onePlay(self):
		#theState = util.weighted_choice(zip(self.states, self.stateProbs))
		theState = np.random.choice(self.states, p=self.stateProbs)
		theSignal = self.sender.getSignal(theState)
		theAct = self.receiver.getAction(theSignal)
		thePayoff = self.payoffs[theState, theAct]
		self.sender.getPaid(thePayoff)
		self.receiver.getPaid(thePayoff)
		if self._recordHist:
			self._payHistory.append(self.getExpectedPayoff())

	def getExpectedPayoff(self):
		theSum = 0.0
		#the below if the fully general calculation
		"""
		for s in self.states:
			for a in self.actions:
				theSum += self.payoffs[s, a] * self.stateProbs[s] * sum([self.sender.getProb(sig, s)*self.receiver.getProb(a, sig) for sig in self.signals])
		"""

		#but, when I'm using the payoffs just to capture negative reinforcement but intuitively
		#still want the identity matrix, here's the hack:
		for s in self.states:
			theSum += sum([self.sender.getProb(sig, s)*self.receiver.getProb(s, sig) for sig in self.signals])

		return theSum / len(self.states)

	def recordPayoff(self):
		self._payHistory.append(self.getExpectedPayoff())


class NGame(Game):
	
	def __init__(self, N, payoffs=[], rectype='A', stateProbs=[]):
		realN = 2*N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)] + [[N,i] for i in range(N)]
		if payoffs == []:
			payoffs = np.identity(realN)
		#Uniform sender/receiver strats to start
		self._func = util.derange(list(states))
		sender = Sender(states, signals, np.ones((len(states),len(signals))))
		if rectype=='A':
			receiver = AtomicReceiver(signals, actions, np.ones((len(signals),len(actions))))
		elif rectype=='N':
			receiver = NegationReceiver(signals, actions, np.ones((N,len(actions))), self._func)
		elif rectype=='F':
			receiver = FunctionReceiver(signals, actions, np.ones((N,len(actions))))
		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)


class NegGame(Game):

	def __init__(self, N, payoffs=[], rectype='N', stateProbs=[]):
		realN = 2*N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)] + [[N,i] for i in range(N)]
		if payoffs == []:
			payoffs = np.identity(realN)
		#Uniform sender/receiver strats to start
		self._func = util.derange(list(states))
		sender = NegationSender(states, signals, np.ones((len(states),N+1)), self._func)
		if rectype=='A':
			receiver = AtomicReceiver(signals, actions, np.ones((len(signals),len(actions))))
		elif rectype=='N':
			receiver = NegationReceiver(signals, actions, np.ones((N,len(actions))), self._func)
		elif rectype=='F':
			receiver = FunctionReceiver(signals, actions, np.ones((N,len(actions))))
		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)

class FuncGame(Game):

	def __init__(self, N, sendtype='full', rectype='F', stateProbs=[]):
		realN = 2*N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)] + [[N,i] for i in range(N)]
		payoffs = np.identity(realN)
                #a particular derangement: i ---> i+1
		self._func = np.roll(list(states), -1).tolist()

                #initialize sender and receiver to be in sig system
		if sendtype == 'full':
                	sendStrat = np.zeros((len(states),N+1))
                	for i in range(N):
                    		sendStrat[2*i, i] = 1.0
                    		sendStrat[2*i + 1, N] = 1.0
			sender = FixedNegationSender(states, signals, sendStrat, self._func)
		#in this version, sender is not negation sender
		elif sendtype == 'semi':
                	sendStrat = np.zeros((len(states),realN))
                	for i in range(N):
                    		sendStrat[2*i, i] = 1.0
		    		sendStrat[2*i + 1, N:] = 1.0
			sender = SemiFixedSender(states, signals, sendStrat)
		else:
			assert False, "Invalid sender type for FuncGame"

		if rectype=='A':
			receiver = AtomicReceiver(signals, actions, np.ones((len(signals),len(actions))))
		elif rectype=='N':
			receiver = NegationReceiver(signals, actions, np.ones((N,len(actions))), self._func)
		elif rectype=='F':
                        recStrat = np.zeros((N, len(actions)))
                        for i in range(N):
                            recStrat[i, 2*i] = 1.0
			receiver = FunctionReceiver(signals, actions, recStrat, self._func)
		Game.__init__(self, sender, receiver, states, signals, actions, payoffs)
