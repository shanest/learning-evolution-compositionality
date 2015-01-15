import numpy as np
import itertools as it
import random
import matplotlib.pyplot as plt

from game import Game, NGame, NegGame, FuncGame

#NUMTRIALS = 10
#NUMITERS = 100
#RECTYPE = 'A'

def writeList(theList, fn):
	thefile = open(fn, 'w')
	for item in theList:
		print>>thefile, item

def runExperiment(gameTypes, reinforcementValues, numtrials, numiters, Nvals, outroot, recordPayoff=200):

	for N in Nvals:

		print 'MOVING TO N =' + str(N)

		for gameType in gameTypes:

			print 'MOVING TO GAMETYPE: ' + gameType

			for i in range(numtrials):

				fulloutroot = outroot+'N'+str(N)+'_'+gameType+'_'+str(reinforcementValues)[1:-1].replace(' ','')+'_trial'+str(i)
				outpay = fulloutroot+'_exppay.txt'
				outsend = fulloutroot+'_sendstrat'
				outrec = fulloutroot+'_recstrat'

				#TODO: payoffs here! refactor Game code and then initialize
				payoffs = np.identity(2*N)*reinforcementValues[0]
				if reinforcementValues[1] != 0:
					for row in range(len(payoffs)):
						for col in range(len(payoffs[0])):
							if row != col:
								payoffs[row][col] += reinforcementValues[1]

				if gameType == 'atomic':
					game = NGame(N, payoffs)
				elif gameType == 'negation':
					game = NegGame(N, payoffs)
				elif gameType == 'semi-fixed':
					game = FuncGame(N, sendtype='semi')
				else:
					assert False, "Invalid game type specified"

				for j in range(numiters):

					game.onePlay()

					if j % recordPayoff == 0:
						game.recordPayoff()

				print game._payHistory[-1]
				writeList(game._payHistory, outpay)
				np.save(outsend, game.sender._stratHistory[-1])
				np.save(outrec, game.receiver._stratHistory[-1])

#runExperiment(['atomic', 'negation'], [1, -1], 100, 10000, [2,3,4,5,6,7], 'data/exp3_')
#runExperiment(['atomic', 'negation'], [2, -1], 100, 10000, [2,3,4,5,6,7], 'data/exp3_')
#runExperiment(['atomic', 'negation'], [3, -1], 100, 10000, [2,3,4,5,6,7], 'data/exp3_')
runExperiment(['semi-fixed'], [1, 0], 100, 10000, [2,3,4,5,6,7], 'data/exp5_')



"""
for N in [2,3,4,5,6,7]:

	print 'MOVING TO N =' + str(N)

	for RECTYPE in ['F']:

		print 'MOVING TO RECTYPE ' + RECTYPE

		for i in range(NUMTRIALS):

			game = FuncGame(N, RECTYPE)

			OUTROOT='data/exp2_'

			#OUTPAY=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_exppay.txt'
			#OUTSEND=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_sendstrat'
			#OUTREC=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_recstrat'

			OUTPAY=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_exppay.txt'
			OUTSEND=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_sendstrat'
			OUTREC=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_recstrat'
			OUTFUNC=OUTROOT+'N'+str(N)+'_funcgame_constneg_trial'+str(i)+'_recfunc'

			for j in range(NUMITERS):
				game.onePlay()

			writeList(game._payHistory, OUTPAY)
			print game._payHistory[-1]
                        print game.receiver._funcHist[-1]
			#save Sender/Rec strategies in .npy format
			np.save(OUTSEND, game.sender._stratHistory[-1])
			np.save(OUTREC, game.receiver._stratHistory[-1])
                        np.save(OUTFUNC, game.receiver._funcHist)
			#for options about text output,
			#see: http://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
			#issue is how to read back in properly
"""

