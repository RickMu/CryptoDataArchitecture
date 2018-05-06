from enum import Enum

class ComputedColumn(Enum):
    RSI = 1<<0
    MOMENTUM = 1<<1
    MOMENTUM_SUM = 1<<2
    MOMENTUM_AVG = 1<<3
    MOMENTUM_WILLR = 1<<4
    PRICE_STOK = 1<<5
    PRICE_STOD = 1<<6
    PRICE_AVG = 1<<7
    WILLR_VOL = 1<<8
    VOL_WILLD = 1<<9
    VOL_SUM = 1<<10
    MOMENTUM_VOL = 1<<11
    BUY_MINUS_SELL = 1<<12
    WILLR_BUY_MINUS_SELL = 1<<13
    BUY_MINUS_SELL_VOL_SUM = 1<<14
    STOK_MOMENTUM_VOL = 1<<15
    MOMENTUM_BUY_MINUS_SELL_VOL_SUM = 1<<16

class OriginalColumn(Enum):
    PRICE_MEAN = 1<<0
    PRICE_MAX =  1<<1
    PRICE_MIN = 1<<2
    VOLUME = 1<<3
    BUY_VOL = 1<<4
    SELL_VOL =  1<<5
    TIME = 1 << 6