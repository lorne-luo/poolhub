from enum import Enum


class UnitType(Enum):
    METRIC = 'METRIC'
    IMPERIAL = 'IMPERIAL'


class Unit:
    GRAM = 'GRAM'
    KG = 'KG'
    LITRE = 'LITRE'
    ML = 'ML'



def weight_to_volume(weight):
    return weight * 0.7988


def oz_to_ml(oz):
    return oz * 29.5735


def oz_to_g(oz):
    return oz * 28.3495


def litre_to_gallon(litre):
    return litre/3.78541
