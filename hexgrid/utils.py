# coding=utf-8
from game_settings import *

def get_currency(amount):
    if CURRENCY_SYMBOL:
        return CURRENCY_SYMBOL
    elif amount == 1:
        return CURRENCY_SINGULAR
    else:
        return CURRENCY_PLURAL