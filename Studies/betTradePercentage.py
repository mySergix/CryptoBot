import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

minWon = 48 # %
maxWon = 52 # %
if minWon > maxWon:
    minWon,maxWon = maxWon,minWon

div = 2
quan = (maxWon - minWon) * div + 1
percWonTrades = []
for i in range(quan):
    perc = minWon + i / div # %
    percWonTrades.append(perc)

initialInvestment = 15000 # u.m.
isComission = True
makerComission = 0.018 # %
maxTakeProfitPer = 10 # %

# LIMITS DEFINITION
maxPer = 15 # Maximum percentage
minPer = 0 # Minimum percentage
numDiv = 100 # Number of divisions in each % unit
perBetTrade = []
quantity = (maxPer - minPer) * numDiv
# In case of minimum percentage being null, the first trade percentage must be 0.5%
if minPer == 0:
    for i in range(quantity):
        percentage = minPer + (maxPer - minPer) * (i + 1) / quantity
        perBetTrade.append(percentage)
else:
    quantity2 = int(quantity + 1)
    for i in range(quantity2):
        percentage = minPer + (maxPer - minPer) * i / (quantity2 - 1)
        perBetTrade.append(percentage)

numTrades = 5648
numIt = 10;

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
                    profitPer = - random.uniform(0, maxTakeProfitPer) / 100
                else:
                    profitPer = random.uniform(0, maxTakeProfitPer) / 100
                    winCount += 1
                if isComission:
                    finalTrade = betTrade * profitPer * (1 - makerComission/100)
                else:
                    finalTrade = betTrade * profitPer
                currentCapital = currentCapital + finalTrade

            ROI = (currentCapital - initialInvestment) / initialInvestment * 100
            winPer = winCount / numTrades * 100
            countPos += 1
            results[countPos] = [botPerc, per * 100, round(ROI, 2), round(winPer,2)]

Results = pd.DataFrame(results, columns = ["Perc Won", "Bet Trade Perc", "ROI", "Win Perc"])
pd.set_option('display.max_rows', None, 'display.max_columns', None)

sns.set_theme(style="dark")
sns.color_palette("viridis", as_cmap=True)

figureResults, ax = plt.subplots()

for botPerc in percWonTrades:
    perBetTradeAnalysis = []
    ROIAnalysis = []
    ResultsFiltered = Results[ Results['Perc Won'] == botPerc ]

    for per in perBetTrade:
        ResultsFiltered2 = ResultsFiltered[ ResultsFiltered['Bet Trade Perc'] == per ]
        ROIMean = ResultsFiltered2["ROI"].mean()
        perBetTradeAnalysis.append(per)
        ROIAnalysis.append(ROIMean)

    sns.lineplot(perBetTradeAnalysis, ROIAnalysis, linewidth=2.0, label="{}".format(botPerc))


# sns.set_theme(style="dark")
# sns.set_palette("bright")
#
# figureResults, ax = plt.subplots()
#
# sns.lineplot(perBetTrade[], ROI[0,:], linewidth=2.0, label="ROI (%)")
#
ax.set_title("ROI vs Bet Trade %",size=14, fontweight="bold")
ax.set_ylabel("ROI (%)",size=12, fontweight='bold')
ax.set_xlabel("Bet Trade %",size=12, fontweight='bold')
ax.set_xlim(minPer, maxPer)
ax.grid()
ax.legend(shadow=True, fontsize=16)

plt.show()
