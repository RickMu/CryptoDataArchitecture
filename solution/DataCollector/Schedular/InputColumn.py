#All the columns that are needed when inputting into DataSet class.
#If missing however shouldn't be a concern at this stage
from enum import Enum
class InputColumns(Enum):
    TIME= 'time',
    PRICE = 'price',
    VOLUME = 'volume',
    BUY_VOL = 'buy_vol',
    SELL_VOL= 'sell_vol',
