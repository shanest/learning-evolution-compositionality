import numpy as np
import random
import util

from sender import Sender, NegationSender
from receiver import * 

class Game(object):

	def __init__(self, sender, receiver, states, signals, actions, payoffs, stateProbs=[], recordHist=True):
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
		for s in self.states:
			for a in self.actions:
				theSum += self.payoffs[s, a] * self.stateProbs[s] * sum([self.sender.getProb(sig, s)*self.receiver.getProb(a, sig) for sig in self.signals])
		return theSum


class NGame(Game):
	
	def __init__(self, N, rectype='A', stateProbs=[]):
		realN = 2*N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)] + [[N,i] for i in range(N)]
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

	def __init__(self, N, rectype='N', stateProbs=[]):
		realN = 2*N
		states = range(realN)
		actions = range(realN)
		signals = [[i] for i in range(N)] + [[N,i] for i in range(N)]
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
