import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

percWonTrades = 52; # %
initialInvestment = 15000; # u.m.
isComission = True
makerComission = 0.018; # %
maxTakeProfitPer = 10 # %

# STUDY LIMITS DEFINITION
maxPer = 50 # Maximum percentage
minPer = 0 # Minimum percentage
numDiv = 2 # Number of divisions in each % unit
quantity = (maxPer - minPer) * numDiv
numTrades = 100000
numIt = 1

perBetTrade = []

for i in range(quantity):
    percentage = (maxPer - minPer) * (i + 1) / quantity
    perBetTrade.append(percentage)

ROI = []
ROI = pd.DataFrame(ROI, columns=['Return'])
winPer = []
winPer = pd.DataFrame(winPer, columns=['Win Percentage'])
betTradeCount = 0

for per in perBetTrade:
    betTradeCount += 1
    for i in range(numIt):
        currentCapital = initialInvestment
        winCount = 0

        for j in range(numTrades):
            if isComission:
                betTrade = currentCapital * per * (1 - makerComission/100)
            else:
                betTrade = currentCapital * per;
            winLossNum = random.uniform(0, 100)
            if winLossNum > percWonTrades:
                profitPer = - random.uniform(0, maxTakeProfitPer)
            else:
                profitPer = random.uniform(0, maxTakeProfitPer)
                winCount += 1
            if isComission:
                finalTrade = betTrade * (1 + profitPer) * (1 - makerComission/100)
            else:
                finalTrade = betTrade * (1 + profitPer)
            currentCapital = currentCapital + finalTrade
        print(betTradeCount)
        ROI['Return'][int(betTradeCount)] = (currentCapital - initialInvestment) / initialInvestment * 100
        winPer['Win Percentage'][betTradeCount] = winCount / numTrades * 100

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

print(ROI)
print(perBetTrade)
