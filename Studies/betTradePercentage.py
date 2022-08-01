import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

maxWon = 60 # %
minWon = 45 # %
div = 2
quan = (maxWon - minWon) * div + 1
percWonTrades = [minWon + i / 2 for i in range(quan)] # %

initialInvestment = 15000 # u.m.
isComission = True
makerComission = 0.018 # %
maxTakeProfitPer = 10 # %

# LIMITS DEFINITION
maxPer = 50 # Maximum percentage
minPer = 0 # Minimum percentage
numDiv = 2 # Number of divisions in each % unit
quantity = (maxPer - minPer) * numDiv
perBetTrade = [(maxPer - minPer) * (i + 1) / quantity for i in range(quantity)]

numTrades = 10
numIt = 2;

results = [ [0, 0, 0, 0] for i in range(len(percWonTrades) * len(perBetTrade) * numIt)]
countPos = -1

for botPerc in percWonTrades:

    for per in perBetTrade:
        per = per / 100 # unitary percentage

        for i in range(numIt):
            currentCapital = initialInvestment
            winCount = 0

            for j in range(numTrades):
                if isComission:
                    betTrade = currentCapital * per * (1 - makerComission/100)
                else:
                    betTrade = currentCapital * per;
                winLossNum = random.uniform(0, 100)
                if winLossNum > botPerc:
                    profitPer = - random.uniform(0, maxTakeProfitPer)
                else:
                    profitPer = random.uniform(0, maxTakeProfitPer)
                    winCount += 1
                if isComission:
                    finalTrade = betTrade * (1 + profitPer) * (1 - makerComission/100)
                else:
                    finalTrade = betTrade * (1 + profitPer)
                currentCapital = currentCapital + finalTrade

            ROI = (currentCapital - initialInvestment) / initialInvestment * 100
            winPer = winCount / numTrades * 100
            countPos += 1
            results[countPos] = [botPerc, per * 100, round(ROI, 2), winPer]

Results = pd.DataFrame(results, columns = ["Perc Won", "Bet Trade Perc", "ROI", "Win Perc"])
pd.set_option('display.max_rows', None, 'display.max_columns', None)
print(Results)

sns.set_theme(style="dark")
sns.set_palette("bright")

#figureResults, ax = plt.subplots()

#sns.lineplot(perBetTrade[], ROI[0,:], linewidth=2.0, label="ROI (%)")

#ax.set_title("ROI vs Bet Trade %",size=14, fontweight="bold")
#ax.set_ylabel("ROI (%)",size=12, fontweight='bold')
#ax.set_xlabel("Bet Trade %",size=12, fontweight='bold')
#ax.set_xlim(minPer, maxPer)
#ax.grid()
#ax.legend(shadow=True, fontsize=16)

#plt.show()
