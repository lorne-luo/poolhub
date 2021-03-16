import math
from apps.testing.calculator.target import get_target
from core.constants import Chemistry, TARGET_RANGE, POOL_TYPE_POOL
from core.unit import litre_to_gallon, oz_to_g, oz_to_ml


def calculate(PH, TA, CH, CYA, Salt, Borate, Temp, surface, chlorine_source, pool_type=POOL_TYPE_POOL):
    target = get_target(pool_type, surface, chlorine_source)


def calculate_ph(volume, ph_now, ph_target, ta_from=100, borate_from=0):
    """volume in litre"""
    borate_from = borate_from or 0
    delta = ph_target - ph_now

    delta = delta * litre_to_gallon(volume)
    temp = (ph_now + ph_target) / 2
    adj = (192.1626 + -60.1221 * temp + 6.0752 * temp * temp + -0.1943 * temp * temp * temp) * (ta_from + 13.91) / 114.6
    delta = delta * adj

    extra = (-5.476259 + 2.414292 * temp + -0.355882 * temp * temp + 0.01755 * temp * temp * temp) * borate_from
    extra *= delta

    if ph_now < ph_target:
        # too low
        result = (delta / 218.68) + (extra / 218.68)
        ph_up = result * 28.3495
        return math.ceil(ph_up)
    else:
        # too high
        result = (delta + extra) / -240.15
        muriatic_acid_volume = (delta + extra) / -240.15 * 29.5735  # muriatic acid， ml
        dry_acid_weight = (delta + extra) / -178.66 * 28.3495  # muriatic acid， g
        dry_acid_volume = dry_acid_weight * 0.6657

        print('muriatic_acid_volume', muriatic_acid_volume)
        print('dry_acid_weight', dry_acid_weight)
        print('dry_acid_volume', dry_acid_volume)
        return math.ceil(dry_acid_weight)


def calculate_ta(volume, now, target):
    now = int(now)
    target = int(target)

    if target == now:
        return None

    factor = 28.3495 / 4259.15
    if target < now:
        # todo instruction
        return 'To lower TA you reduce pH to 7.0-7.2 with acid and then aerate to increase pH.'
    else:
        weight = (target - now) * litre_to_gallon(volume * factor)  # unit g

        return math.ceil(weight)


def calc_fc(volume, now, target):
    now = int(now)
    target = int(target)

    if target == now:
        return None

    bleach_concentration = 0.06 * 100
    if now < target:
        temp = (target - now) * litre_to_gallon(volume) / 482.202 * 6 / bleach_concentration
        return temp * 29.5735
    else:
        # todo other instruction to reduce FC
        pass


def calc_ch(volume, now, target):
    now = int(now)
    target = int(target)

    if target == now:
        return None

    if now < target:
        temp = (target - now) * litre_to_gallon(volume) / 6754.11
        calcium_chloride_weight = temp * 28.3495  # unit g
        calcium_chloride_volume = temp * 0.7988 * 29.5735  # unit ml

        print(calcium_chloride_weight)
        print(calcium_chloride_volume)

        temp = (target - now) * litre_to_gallon(volume) / 5098.82

        calcium_chloride_dihydrate_weight = temp * 28.3495  # unit g
        calcium_chloride_dihydrate_volume = temp * 1.148 * 29.5735  # unit ml

        print(calcium_chloride_dihydrate_weight)
        print(calcium_chloride_dihydrate_volume)
        return math.ceil(calcium_chloride_weight)
    else:
        # todo other instruction to reduce FC
        ch_fill = 0
        if target < ch_fill:
            return f'Make sure you can replace with the water CH lower than {target}'
        else:
            replace_percent = math.ceil(100 - ((target - ch_fill) / (now - ch_fill)) * 100)
            # replace_percent = replace_percent / 100
            return f'Replace {replace_percent}% water with new water, with CH of {replace_percent}'


def calc_cya(volume, now, target):
    if now < target:
        # too low
        temp = (target - now) * litre_to_gallon(volume) / 7489.51

        stabilizer_weight = oz_to_g(temp)
        stabilizer_volume = oz_to_ml(temp * 1.042)

        temp = (target - now) * litre_to_gallon(volume) / 2890
        liquid_stabilizer_volume = oz_to_ml(temp)

        print(
            f'Add {math.ceil(stabilizer_weight)} g by weight or {math.ceil(stabilizer_volume)} ml by volume of stabilizer')
        print(f'or add {math.ceil(liquid_stabilizer_volume)} ml of liquid stabilizer.')
        return math.ceil(stabilizer_weight)
    else:
        # too high
        refill_percent = 100 - (target / now) * 100
        print(f'To lower CYA you replace {refill_percent}% of the water with new water.')
        return math.ceil(refill_percent)


def calc_salt(volume, now, target):
    if now < target:
        # too low
        temp = (target - now) * litre_to_gallon(volume) / 7468.64 * 0.0283495
        salt_kg = temp

        print(f'Add {salt_kg} kg of salt.')
        return math.ceil(salt_kg)
    else:
        # too high
        replace_percent = 100 - (target / now) * 100
        print(f'To lower Salt you replace {replace_percent}% of the water with new water.')
        return math.ceil(replace_percent)


def calc_borate(volume, now, target):
    bormuls = [849.271, 1309.52, 1111.69]
    if now < target:
        # too low, add borax
        temp = (target - now) * litre_to_gallon(volume)

        broax_concentration = 849.271
        borax_g = oz_to_g(temp / broax_concentration)
        borax_ml = oz_to_ml(temp / broax_concentration * 0.9586)
        borax_muriatic_acid_ml = oz_to_ml(temp / broax_concentration * 0.4765)
        print(f'Add {borax_g} g by weight or {borax_ml} ml by volume of Borax')
        print(f'and {borax_muriatic_acid_ml} ml of 31.45% muriatic acid to compensate for the pH increase.')

        boric_acid_concentration = 1309.52
        boric_acid_g = oz_to_g(temp / boric_acid_concentration)
        boric_acid_ml = oz_to_ml(temp / boric_acid_concentration * 1.075)
        print(f'Add {boric_acid_g} g by weight or {boric_acid_ml} ml by volume of Borax')

        tetraborate_pentahydrate_concentration = 1111.69
        tetraborate_pentahydrate_g = oz_to_g(temp / tetraborate_pentahydrate_concentration)
        tetraborate_pentahydrate_ml = oz_to_ml(temp / tetraborate_pentahydrate_concentration * 0.5296)
        tetraborate_pentahydrate_muriatic_acid_ml = oz_to_ml(temp / tetraborate_pentahydrate_concentration * 0.624)
        print(f'Add {tetraborate_pentahydrate_g} g by weight or {tetraborate_pentahydrate_ml} ml by volume of Borax')
        print(
            f'and {tetraborate_pentahydrate_muriatic_acid_ml} ml of 31.45% muriatic acid to compensate for the pH increase.')

        return math.ceil(borax_g)
    else:
        # too high
        replace_percent = 100 - (target / now) * 100
        print(f'To lower Borate you replace {replace_percent}% of the water with new water.')
        print('Note: The pH should be tested and adjusted as needed after increasing the borate level.')
        return math.ceil(replace_percent)
