from copy import deepcopy

from core.constants import Chemistry, POOL_TYPE_SPA, CHLORINE_SOURCE_BLEACH, CHLORINE_SOURCE_SWG, \
    CHLORINE_SOURCE_TRICHLOR, POOL_SURFACE_PLASTER, POOL_SURFACE_VINYL

SPA_TARGET = {
    Chemistry.PH: {
        'min': 7.4,
        'max': 7.8,
    },
    Chemistry.CH: {  # ppm
        'min': 120,
        'max': 200,
    },
    Chemistry.FC: {  # ppm
        'min': 1,
        'max': 6,
    },
    Chemistry.TA: {  # ppm
        'min': 50,
        'max': 80,
    },
    Chemistry.TC: {  # ppm
        'min': 0,
        'max': 2,
    },
    Chemistry.CYA: {  # ppm
        'min': 20,
        'max': 40,
    }
}

TRADITIONAL_POOL_TARGET = {
    Chemistry.PH: {
        'min': 7.2,
        'max': 7.8,
    },
    Chemistry.CH: {  # ppm
        'min': 220,
        'max': 320,
    },
    Chemistry.FC: {  # ppm
        'min': 3,
        'max': 7,
    },
    Chemistry.TA: {  # ppm
        'min': 80,
        'max': 120,
    },
    # Chemistry.TB: {  # ppm, SPA only
    #     'min': 80,
    #     'max': 120,
    # },
    Chemistry.TC: {  # ppm
        'min': 0,
        'max': 2,
    },
    Chemistry.CYA: {  # ppm
        'min': 30,
        'max': 60,
    },
    Chemistry.SALT: {  # ppm
        'min': 3500,
        'max': 4500,
    }
}


def get_target(pool_type, surface, chlorine_source):
    if pool_type == POOL_TYPE_SPA:
        return SPA_TARGET

    target = deepcopy(TRADITIONAL_POOL_TARGET)
    if chlorine_source == CHLORINE_SOURCE_BLEACH:
        target[Chemistry.TA]['min'] = 70
        target[Chemistry.TA]['max'] = 90
    elif chlorine_source == CHLORINE_SOURCE_SWG:
        target[Chemistry.TA]['min'] = 60
        target[Chemistry.TA]['max'] = 80
        target[Chemistry.CYA]['min'] = 70
        target[Chemistry.CYA]['max'] = 80
    elif chlorine_source == CHLORINE_SOURCE_TRICHLOR:
        target[Chemistry.TA]['min'] = 100
        target[Chemistry.TA]['max'] = 120

    if surface == POOL_SURFACE_PLASTER:
        target[Chemistry.CH]['min'] = 250
        target[Chemistry.CH]['max'] = 350
    elif surface == POOL_SURFACE_VINYL:
        target[Chemistry.CH]['min'] = 50
        target[Chemistry.CH]['max'] = 300

    # calculate idea value for all chemistry
    for che, values in target.items():
        if 'ideal' not in values:
            values['ideal'] = (values['min'] + values['max']) / 2

    return target
