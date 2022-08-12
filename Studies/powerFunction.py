import numpy as np

class powerFunction(numTrades, percWonTrades):

    r = numTrades * percWonTrades / 100

    c = np.linspace(0, r-1, r)
    cIni = c
    comb = c
    i = 0

    while i < length(c):

        if c[i] == c(i+1) - 1:

            i += 1

            if i == length(c):

                if c[i] < numTrades - 1:

                    c[i] += 1
                    i -= 1

                    while i > -1:

                        c[i] = cIni[i]
                        i -= 1

                    comb
                    i = 1
