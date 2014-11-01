import numpy as np
import itertools as it
import random
import matplotlib.pyplot as plt

from game import Game, NGame, NegGame

NUMTRIALS = 100
NUMITERS = 10000
#RECTYPE = 'A'

def writeList(theList, fn):
	thefile = open(fn, 'w')
	for item in theList:
		print>>thefile, item
	
for N in [7]:

	print 'MOVING TO N =' + str(N)

	for RECTYPE in ['N']:

		print 'MOVING TO RECTYPE ' + RECTYPE

		for i in range(NUMTRIALS):

			game = NegGame(N, RECTYPE)

			OUTROOT='data/exp1_'
			"""
			OUTPAY=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_exppay.txt'
			OUTSEND=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_sendstrat'
			OUTREC=OUTROOT+'N'+str(N)+'_rec'+RECTYPE+'_trial'+str(i)+'_recstrat'
			"""
			OUTPAY=OUTROOT+'N'+str(N)+'_neggame_trial'+str(i)+'_exppay.txt'
			OUTSEND=OUTROOT+'N'+str(N)+'_neggame_trial'+str(i)+'_sendstrat'
			OUTREC=OUTROOT+'N'+str(N)+'_neggame_trial'+str(i)+'_recstrat'

			for j in range(NUMITERS):
				game.onePlay()

			writeList(game._payHistory, OUTPAY)
			print game._payHistory[-1]
			#save Sender/Rec strategies in .npy format
			np.save(OUTSEND, game.sender._stratHistory[-1])
			np.save(OUTREC, game.receiver._stratHistory[-1])
			#for options about text output,
			#see: http://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
			#issue is how to read back in properly
