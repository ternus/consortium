# coding=utf-8
"""
Utility methods.
"""
from hexgrid.game_settings import CURRENCY_SINGULAR, \
    CURRENCY_PLURAL, CURRENCY_SYMBOL

def currency(amount):
    """
    Format currency properly.
    """
    if CURRENCY_SYMBOL:
        return "%s%d" % (CURRENCY_SYMBOL, int(amount))
    elif amount == 1:
        return "%d %s" % (int(amount), CURRENCY_SINGULAR)
    else:
        return "%d %s" % (int(amount), CURRENCY_PLURAL)