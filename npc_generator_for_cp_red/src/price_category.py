#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum


class PriceCategory(Enum):
    CHEAP = 0
    EVERYDAY = 1
    COSTLY = 2
    PREMIUM = 3
    EXPENSIVE = 4
    VERY_EXPENSIVE = 5
    LUXURY = 6
    SUPER_LUXURY = 7

    @staticmethod
    def from_price(price: int):  # -> PriceCategory:
        if price <= 10:
            return PriceCategory.CHEAP
        elif price <= 20:
            return PriceCategory.EVERYDAY
        elif price <= 50:
            return PriceCategory.COSTLY
        elif price <= 100:
            return PriceCategory.PREMIUM
        elif price <= 500:
            return PriceCategory.EXPENSIVE
        elif price <= 1000:
            return PriceCategory.VERY_EXPENSIVE
        elif price <= 5000:
            return PriceCategory.LUXURY
        else:
            return PriceCategory.SUPER_LUXURY

    def get_default_price(self) -> int:
        match self:
            case PriceCategory.CHEAP:
                return 10
            case PriceCategory.EVERYDAY:
                return 20
            case PriceCategory.COSTLY:
                return 50
            case PriceCategory.PREMIUM:
                return 100
            case PriceCategory.EXPENSIVE:
                return 500
            case PriceCategory.VERY_EXPENSIVE:
                return 1000
            case PriceCategory.LUXURY:
                return 5000
            case PriceCategory.SUPER_LUXURY:
                return 10000
