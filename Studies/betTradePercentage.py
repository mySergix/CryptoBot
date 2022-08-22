import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import combinatory

minWon = 50 # %
maxWon = 50 # %
if minWon > maxWon:
    minWon,maxWon = maxWon,minWon

div = 2
quan = (maxWon - minWon) * div + 1
percWonTrades = []
for i in range(quan):
    perc = minWon + i / div # %
    percWonTrades.append(perc)

initialInvestment = 15000 # u.m.
isComission = False
makerComission = 0.018 # %
maxTakeProfitPer = 10 # %

# LIMITS DEFINITION
maxPer = 6 # Maximum percentage
minPer = 5 # Minimum percentage
numDiv = 2 # Number of divisions in each % unit
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

numTrades = 20
numIt = 10

results = []
# results = [ [0, 0, 0, 0] for i in range(len(percWonTrades) * len(perBetTrade) * numIt)]
countPos = -1

for botPerc in percWonTrades:

    numWins = numTrades * botPerc / 100

    # Checking if numWins is an integer
    if not numWins.is_integer():
        raise Exception("numWins must be an integer value. numWins = numTrades * botPerc / 100 ")

    # posWins is the list which contains the possible index winning combinations
    posWins = combinatory.combWithoutRep(numTrades, int(numWins))

    for i in range(len(posWins)):

        per = 0.2
        currentCapital = initialInvestment

        print(posWins[i])

        for j in range(numTrades):
            if isComission:
                betTrade = currentCapital * per * (1 - makerComission/100)
            else:
                betTrade = currentCapital * per;

            if j in posWins[i]:
                profitPer = 0.75
            else:
                profitPer = - 0.75

            if isComission:
                finalTrade = betTrade * profitPer * (1 - makerComission/100)
            else:
                finalTrade = betTrade * profitPer
            currentCapital = currentCapital + finalTrade
        print(currentCapital)

        ROI = (currentCapital - initialInvestment) / initialInvestment * 100
        results.append([botPerc, per * 100, round(ROI,5)])

print(results)

# for botPerc in percWonTrades:
#
#     # Combinatory without repetition
#     r = int(numTrades*botPerc/100)
#     numIt = math.factorial(numTrades) / (math.factorial(r) * math.factorial(numTrades - r))
#     print(len(combinaciones(comb, r))
#
#     for per in perBetTrade:
#         per = per / 100 # unitary percentage
#
#         for i in range(numIt):
#             currentCapital = initialInvestment
#             winCount = 0
#
#             for j in range(numTrades):
#                 if isComission:
#                     betTrade = currentCapital * per * (1 - makerComission/100)
#                 else:
#                     betTrade = currentCapital * per;
#                 winLossNum = random.uniform(0, 100)
#                 if winLossNum > botPerc:
#                     profitPer = - random.uniform(0, maxTakeProfitPer) / 100
#                 else:
#                     profitPer = random.uniform(0, maxTakeProfitPer) / 100
#                     winCount += 1
#                 if isComission:
#                     finalTrade = betTrade * profitPer * (1 - makerComission/100)
#                 else:
#                     finalTrade = betTrade * profitPer
#                 currentCapital = currentCapital + finalTrade
#
#             ROI = (currentCapital - initialInvestment) / initialInvestment * 100
#             winPer = winCount / numTrades * 100
#             countPos += 1
#             results[countPos] = [botPerc, per * 100, round(ROI, 2), round(winPer,2)]
#
# Results = pd.DataFrame(results, columns = ["Set Win Perc", "Bet Trade Perc", "ROI", "Real Win Perc"])
# pd.set_option('display.max_rows', None, 'display.max_columns', None)
# print(Results)
#
# sns.set_theme(style="dark")
# sns.color_palette("viridis", as_cmap=True)
#
# figureResults, ax = plt.subplots()
#
# ###### STUDIES ######
# # STUDY ROI vs BET TRADE vs PERCENTAGE WON --> 1
# # STUDY ROI vs WIN PERCENTAGE vs PERCENTAGE WON for every BET TRADE --> 2
#
# studyNum = 2
#
# if studyNum == 1:
#     for botPerc in percWonTrades:
#         perBetTradeAnalysis = []
#         ROIAnalysis = []
#         ResultsFiltered = Results[ Results['Set Win Perc'] == botPerc ]
#
#         for per in perBetTrade:
#             ResultsFiltered2 = ResultsFiltered[ ResultsFiltered['Bet Trade Perc'] == per ]
#             ROIMean = ResultsFiltered2["ROI"].mean()
#             perBetTradeAnalysis.append(per)
#             ROIAnalysis.append(ROIMean)
#
#         sns.lineplot(perBetTradeAnalysis, ROIAnalysis, linewidth=2.0, label="{}".format(botPerc))
#
#     ax.set_title("ROI vs Bet Trade %", size=14, fontweight="bold")
#     ax.set_ylabel("ROI (%)", size=12, fontweight='bold')
#     ax.set_xlabel("Bet Trade %", size=12, fontweight='bold')
#     ax.set_xlim(minPer, maxPer)
#     ax.grid()
#     ax.legend(shadow=True, fontsize=16)
#
#     plt.show()
#
# elif studyNum == 2:
#     for per in perBetTrade:
#         ResultsFiltered = Results [ Results [ 'Bet Trade Perc'] == per ]
#
#         ResultsFiltered2 = ResultsFiltered.groupby('')
#
#         sns.lineplot(ResultsFiltered['Real Win Perc'], ResultsFiltered['ROI'], linewidth=2.0, label="{}".format(per))
#         ax.set_title("ROI vs Real Win (%)", size=14, fontweight="bold")
#         ax.set_ylabel("ROI (%)", size=12, fontweight='bold')
#         ax.set_xlabel("Real Win (%)", size=12, fontweight='bold')
#         ax.set_xlim(minWon - 2, maxWon + 2)
#         ax.grid()
#         ax.legend(shadow=True, fontsize=16)
#
#         plt.show()
