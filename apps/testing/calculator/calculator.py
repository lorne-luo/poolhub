import math
from apps.testing.calculator.target import get_target
from apps.testing.dataclasses import ChemistrySolution, Product, Action
from core.constants import Chemistry, TARGET_RANGE, POOL_TYPE_POOL, PRODUCT_TYPE, ActionType
from core.unit import Unit
from core.unit import litre_to_gallon, oz_to_g, oz_to_ml


def calculate(volume, ph, ta, ch, cya, salt, borate, temp, surface, chlorine_source, pool_type=POOL_TYPE_POOL):
    target = get_target(pool_type, surface, chlorine_source)

    ph_solution = calc_ph(volume, ph, target[Chemistry.PH]['ideal'], ta_now=100, borate_now=borate)


def calc_ph(volume, ph_now, ph_target, ta_now=100, borate_now=0):
    """volume in litre"""
    borate_now = borate_now or 0
    delta = ph_target - ph_now

    delta = delta * litre_to_gallon(volume)
    temp = (ph_now + ph_target) / 2
    adj = (192.1626 + -60.1221 * temp + 6.0752 * temp * temp + -0.1943 * temp * temp * temp) * (ta_now + 13.91) / 114.6
    delta = delta * adj

    extra = (-5.476259 + 2.414292 * temp + -0.355882 * temp * temp + 0.01755 * temp * temp * temp) * borate_now
    extra *= delta

    if ph_now < ph_target:
        # too low
        result = (delta / 218.68) + (extra / 218.68)
        soda_ash_weight = result * 28.3495

        return ChemistrySolution(
            chemistry=Chemistry.PH.value,
            options=[
                [
                    # add pH Up (also known as Soda Ash or Sodium Carbinate) in grams
                    # Always in granula form.
                    # People rearly refer the product as Soda Ash or Sodium Carbinate.
                    # Always contain 100% Sodium Carbinate.
                    Product(PRODUCT_TYPE.SODA_ASH, math.ceil(soda_ash_weight), Unit.GRAM)
                ],
            ]
        )
    else:
        # too high
        temp = (delta + extra) / -240.15
        muriatic_acid_concentration = 1  # 31.45% - 20° Baume
        hydrochloric_acid_concentration = 31.45 / 32.5

        # muriatic acid, ml
        muriatic_acid_volume = temp * muriatic_acid_concentration * 29.5735

        # hydrochloric acid, ml
        hydrochloric_acid_volume = temp * hydrochloric_acid_concentration * 29.5735

        # muriatic acid, g
        dry_acid_weight = (delta + extra) / -178.66 * 28.3495
        dry_acid_volume = dry_acid_weight * 0.6657

        # print('muriatic_acid_volume', muriatic_acid_volume)
        # print('dry_acid_weight', dry_acid_weight)
        # print('dry_acid_volume', dry_acid_volume)

        return ChemistrySolution(
            chemistry=Chemistry.PH.value,
            options=[
                [
                    # always add 32.5% Pool Acid in ml or litre.
                    # In Australia, everyone refer to the acid as pool acid.
                    # Always contains 32.5% Hydrochloric Acid
                    # Always in liquid form.
                    Product(PRODUCT_TYPE.POOL_ACID, math.ceil(hydrochloric_acid_volume), Unit.ML)
                ],
            ]
        )


def calc_ta(volume, now, target):
    now = int(now)
    target = int(target)

    if target == now:
        return None

    factor = 28.3495 / 4259.15
    if target < now:
        # too high
        # todo combine with ph calculation
        return ChemistrySolution(
            chemistry=Chemistry.TA.value,
            options=[
                [
                    # Not many people use and know the product
                    Action(type=ActionType.CONSAULT_POOLSHOP,
                           remark='To lower TA you reduce pH to 7.0-7.2 with acid and then aerate to increase pH.')
                ],
            ]
        )
    else:
        # too low
        # add pH Buffer (also known Alkilinity Enhancer, Baking Soda or Sodium BiCarbinate) in grams
        # Always in granular form
        # Always contains 100% SOdium BiCarbinate
        baking_soda_weight = (target - now) * litre_to_gallon(volume * factor)  # unit g
        # print(baking_soda_weight)

        return ChemistrySolution(
            chemistry=Chemistry.TA.value,
            options=[
                [
                    # add pH Up (also known as Soda Ash or Sodium Carbinate) in grams
                    # Always in granula form.
                    # People rearly refer the product as Soda Ash or Sodium Carbinate.
                    # Always contain 100% Sodium Carbinate.
                    Product(PRODUCT_TYPE.PH_BUFFER, math.ceil(baking_soda_weight), Unit.GRAM)
                ],
            ]
        )


def calc_fc(volume, now, target):
    now = int(now)
    target = int(target)

    if target == now:
        return None

    liquid_chlorine_concentration = 12.5  # %, australia normally use 12.5% liquid chlorine
    trichlor_factor = 6854.95
    dichlor_factor = 4149.03
    cal_hypo_70_factor = 5199.52

    if now < target:
        # too low
        cal_hypo_70_weight = (target - now) * litre_to_gallon(volume) / cal_hypo_70_factor
        cal_hypo_70_weight = math.ceil(oz_to_g(cal_hypo_70_weight))

        liquid_chlorine_ml = (target - now) * litre_to_gallon(volume) / 482.202 * 6 / liquid_chlorine_concentration
        liquid_chlorine_ml = math.ceil(oz_to_ml(liquid_chlorine_ml))

        trichlor_weight = (target - now) * litre_to_gallon(volume) / trichlor_factor
        print(math.ceil(oz_to_ml(trichlor_weight)))
        dichlor_weight = (target - now) * litre_to_gallon(volume) / dichlor_factor
        print(math.ceil(oz_to_ml(dichlor_weight)))

        # todo If not enough and a chlorinator pool, crank up chlorine production.
        return ChemistrySolution(
            chemistry=Chemistry.FC.value,
            options=[
                [
                    # option 1:  Liquid Chlorine in ml
                    # Always cotnains 12.5% Sodium Chloride
                    # todo Always in litres
                    # Almost no one calls it bleach in Australia.
                    Product(PRODUCT_TYPE.LIQUID_CHLORINE, liquid_chlorine_ml, Unit.ML)
                ],
                [
                    # option 2: 70% Cal-Hypo in grams
                    # Always in granular form.
                    # Always contain 70% or close Calcium Hypochloride
                    Product(PRODUCT_TYPE.CAL_HYPO_70P, cal_hypo_70_weight, Unit.GRAM)
                ],
                [
                    # option 3: Trichlor in grams
                    # Aways in granular form in Australia
                    Product(PRODUCT_TYPE.TRICHLOR, trichlor_weight, Unit.GRAM)
                ],
                [
                    # option 4: Dichlor in grams
                    # Aways in granular form in Australia
                    Product(PRODUCT_TYPE.DICHLOR, dichlor_weight, Unit.GRAM)
                ]
            ]
        )

    else:
        # too high, add chlorine remover.
        return ChemistrySolution(
            chemistry=Chemistry.FC.value,
            options=[
                [
                    # Not many people use and know the product
                    Action(type=ActionType.CONSAULT_POOLSHOP)
                ],
            ]
        )


def calc_ch(volume, now, target):
    now = int(now)
    target = int(target)

    if target == now:
        return None

    if now < target:
        # too low
        temp = (target - now) * litre_to_gallon(volume) / 6754.11
        calcium_chloride_weight = temp * 28.3495  # unit g
        calcium_chloride_volume = temp * 0.7988 * 29.5735  # unit ml
        calcium_chloride_weight = math.ceil(calcium_chloride_weight)
        calcium_chloride_volume = math.ceil(calcium_chloride_volume)
        print(calcium_chloride_weight)
        print(calcium_chloride_volume)

        temp = (target - now) * litre_to_gallon(volume) / 5098.82

        calcium_chloride_dihydrate_weight = temp * 28.3495  # unit g
        calcium_chloride_dihydrate_volume = temp * 1.148 * 29.5735  # unit ml

        print(calcium_chloride_dihydrate_weight)
        print(calcium_chloride_dihydrate_volume)

        return ChemistrySolution(
            chemistry=Chemistry.CH.value,
            options=[
                [
                    # add Hardness Enhancer (namely Calcium Enhancer and Calcium Chloride) in grans
                    # Always in granular form, always contains 100% Calcium Chloride
                    Product(PRODUCT_TYPE.CALCIUM_CHLORIDE, calcium_chloride_weight, Unit.GRAM),
                ],
                [
                    Product(PRODUCT_TYPE.CALCIUM_CHLORIDE, calcium_chloride_volume, Unit.ML)
                ]
            ]
        )
    else:
        # too high
        ch_fill = 0
        if target < ch_fill:
            return f'Make sure you can replace with the water CH lower than {target}'
        else:
            replace_percent = math.ceil(100 - ((target - ch_fill) / (now - ch_fill)) * 100)

            # replace_percent = replace_percent / 100
            return ChemistrySolution(
                chemistry=Chemistry.CH.value,
                options=[
                    [
                        # dump and refill water.
                        Action(type=ActionType.REPLACE_WATER,
                               value=replace_percent,
                               remark=f'Replace {replace_percent}% of the water with new water, with CH of {ch_fill}')
                    ],
                ]
            )


def calc_cya(volume, now, target):
    if now < target:
        # too low
        temp = (target - now) * litre_to_gallon(volume) / 7489.51

        stabilizer_weight = oz_to_g(temp)
        stabilizer_volume = oz_to_ml(temp * 1.042)
        stabilizer_weight=math.ceil(stabilizer_weight)
        stabilizer_volume=math.ceil(stabilizer_volume)

        temp = (target - now) * litre_to_gallon(volume) / 2890
        liquid_stabilizer_volume = oz_to_ml(temp)

        print(
            f'Add {math.ceil(stabilizer_weight)} g by weight or {math.ceil(stabilizer_volume)} ml by volume of stabilizer')
        print(f'or add {math.ceil(liquid_stabilizer_volume)} ml of liquid stabilizer.')

        return ChemistrySolution(
            chemistry=Chemistry.CYA.value,
            options=[
                [
                    # add Stabiliser (also known as Sunscreen CYA or Cyanuric Acid) in grams
                    # Almost always in granular form
                    # People hardly known the product as CYA or Cyanuric Acid, more popular known as Stabiliser
                    Product(PRODUCT_TYPE.STABILISER, stabilizer_weight, Unit.GRAM),
                ],
                [
                    # Liquid form product is expensive and hard to find.
                    Product(PRODUCT_TYPE.STABILISER, stabilizer_volume, Unit.ML)
                ]
            ]
        )
    else:
        # too high
        refill_percent = 100 - (target / now) * 100
        # print(f'To lower CYA you replace {refill_percent}% of the water with new water.')
        return ChemistrySolution(
            chemistry=Chemistry.CYA.value,
            options=[
                [
                    # dump and refill water.
                    Action(type=ActionType.REPLACE_WATER,
                           value=math.ceil(refill_percent),
                           remark=f'To lower CYA you replace {refill_percent}% of the water with new water.')
                ],
            ]
        )


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
