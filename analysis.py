import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def writeAverages():

    Apays = [[], [], [], [], [], []]
    Npays = [[], [], [], [], [], []]
    finalA = [[], [], [], [], [], []]
    finalN = [[], [], [], [], [], []]
    avgA = []
    avgN = []

    for N in [2,3,4,5,6,7]:

        for i in range(100):

            Apays[N-2].append(np.loadtxt('data/exp1_N'+str(N)+'_recA_trial'+str(i)+'_exppay.txt'))
            Npays[N-2].append(np.loadtxt('data/exp1_N'+str(N)+'_neggame_trial'+str(i)+'_exppay.txt'))
            #Npays.append(np.loadtxt('data/exp1_N'+str(N)+'_recN_trial'+str(i)+'_exppay.txt'))

        finalA[N-2] = map(lambda x: x[-1], Apays[N-2])
        finalN[N-2] = map(lambda x: x[-1], Npays[N-2])
        avgA.append(np.mean(finalA[N-2]))
        avgN.append(np.mean(finalN[N-2]))
        np.savetxt('data/exp1_N'+str(N)+'_recA_finalexps.txt', finalA[N-2])
        np.savetxt('data/exp1_N'+str(N)+'_neggame_finalexps.txt', finalN[N-2])

    avgdiff = map(lambda x: avgN[x] - avgA[x], range(len(avgA)))
    np.savetxt('data/exp1_avg_recA.txt', avgA)
    np.savetxt('data/exp1_avg_neg.txt', avgN)
    np.savetxt('data/exp1_avg_negMINUSrecA.txt', avgdiff)
	

def saveLinearRegression():

    avgdiff = np.loadtxt('data/exp1_avg_negMINUSrecA.txt')
    np.savetxt('data/exp1_avgdiff_linreg.txt', stats.linregress([2,3,4,5,6,7], avgdiff))

def plotLinearRegression():

    avgdiff = np.loadtxt('data/exp1_avg_negMINUSrecA.txt')
    slope, intercept, rval, pval, err = np.loadtxt('data/exp1_avgdiff_linreg.txt')
    x = [2,3,4,5,6,7]
    xx = np.linspace(1,8,200)
    theline = map(lambda x: intercept + slope*x, xx)
    plt.plot(x, avgdiff, 'bo')
    plt.plot(xx, theline, 'r')
    plt.show()
