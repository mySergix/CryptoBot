# Computes a combinatory without repetition
def combWithoutRep(n, r):

    c = [i for i in range(r)]
    cIni = c.copy()

    comb = [c.copy()]
    i = 0

    while i < len(c) - 1:

        if c[i] == c[i+1] - 1:

            i += 1

            if i == len(c) - 1:

                if c[i] < n - 1:

                    c[i] += 1
                    i -= 1

                    while i > -1:

                        c[i] = cIni[i]
                        i -= 1

                    comb.append(c.copy())
                    i = 0
        else:
            c[i] += 1
            i -= 1

            while i > -1:

                c[i] = cIni[i]
                i -= 1

            comb.append(c.copy())
            i = 0

    return comb
