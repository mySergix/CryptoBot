# This class defines the sizers for the backtrading.

# Python libraries
from backtrader.sizers import PercentSizer

class FullMoney(PercentSizer):

    '''
    Setting the percentage of money to invest in a trade.

        @param PercentSizer: percentage of money to be invested.

        @return none
    '''

    params = (
        ("percents", 100),
    )
