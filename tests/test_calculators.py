from apps.testing.calculator import *
from apps.testing.calculator.calculator import calc_ta, calc_ph, calc_ch, calc_cya, calc_salt, calc_borate, \
    calc_fc
from apps.testing.dataclasses import Action
from core.constants import PRODUCT_TYPE, Chemistry, ActionType
from core.unit import *


def test_ph_too_low():
    solution = calc_ph(10000, 7.0, 7.5, 100, 0)
    assert solution.chemistry==Chemistry.PH.value
    assert len(solution.options) == 1
    assert solution.options[0][0].value == 266
    assert solution.options[0][0].type == PRODUCT_TYPE.SODA_ASH


def test_ph_too_high():
    solution = calc_ph(10000, 7.9, 7.5, 100, 0)
    assert solution.chemistry==Chemistry.PH.value
    assert len(solution.options) == 1
    assert solution.options[0][0].value == 90
    assert solution.options[0][0].type == PRODUCT_TYPE.POOL_ACID


def test_ta_too_low():
    solution = calc_ta(10000, 100, 110)
    assert solution.chemistry==Chemistry.TA.value
    assert len(solution.options) == 1
    assert solution.options[0][0].value == 176
    assert solution.options[0][0].type == PRODUCT_TYPE.PH_BUFFER

def test_ta_too_high():
    solution = calc_ta(10000, 100, 90)
    assert solution.chemistry==Chemistry.TA.value
    assert len(solution.options) == 1
    assert isinstance(solution.options[0][0], Action)
    assert solution.options[0][0].type, ActionType.CONSAULT_POOLSHOP

def test_ch():
    assert 111 == calc_ch(10000, 250, 260)

    ch = calc_ch(10000, 260, 250)
    assert '4%' in ch


def test_cya():
    assert 100 == calc_cya(10000, 30, 40)
    assert 20 == calc_cya(10000, 50, 40)


def test_salt():
    assert 41 == calc_salt(10000, 0, 4000)
    assert 25 == calc_salt(10000, 4000, 3000)


def test_borate():
    assert 89 == calc_borate(10000, 1, 2)
    assert 34 == calc_borate(10000, 3, 2)


def test_fc_too_low():
    solution = calc_fc(10000, 3, 4)
    assert solution.chemistry==Chemistry.FC.value
    assert len(solution.options) == 4


def test_fc_too_high():
    solution = calc_fc(10000, 4, 3)
    assert solution.chemistry==Chemistry.FC.value
    assert len(solution.options) == 1
    assert isinstance(solution.options[0][0], Action)
    assert solution.options[0][0].type, ActionType.CONSAULT_POOLSHOP
