from apps.testing.calculator import *
from apps.testing.calculator.calculator import calculate_ta, calculate_ph, calc_ch, calc_cya
from core.unit import *


def test_ph_too_low():
    value = calculate_ph(10000, 7.0, 7.5, 100, 0)
    assert value == 266

    value = calculate_ph(10000, 6.9, 7.4, 100, 0)
    assert value == 315


def test_ph_too_high():
    value = calculate_ph(10000, 7.9, 7.5, 100, 0)
    assert value == 120


def test_ta():
    value = calculate_ta(1000, 100, 110)
    assert value == 18


def test_ch():
    assert 111 == calc_ch(10000, 250, 260)

    ch = calc_ch(10000, 260, 250)
    assert '4%' in ch


def test_cya():
    assert 100 == calc_cya(10000, 30, 40)
    assert 20 == calc_cya(10000, 50, 40)
