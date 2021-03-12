from enum import Enum

AU_STATE_NSW = 'NSW'
AU_STATE_VIC = 'VIC'
AU_STATE_QLD = 'QLD'
AU_STATE_TAS = 'TAS'
AU_STATE_WA = 'WA'
AU_STATE_ACT = 'ACT'
AU_STATE_NT = 'NT'

AU_STATE_CHOICES = (
    (AU_STATE_NSW, AU_STATE_NSW),
    (AU_STATE_VIC, AU_STATE_VIC),
    (AU_STATE_QLD, AU_STATE_QLD),
    (AU_STATE_TAS, AU_STATE_TAS),
    (AU_STATE_WA, AU_STATE_WA),
    (AU_STATE_ACT, AU_STATE_ACT),
    (AU_STATE_NT, AU_STATE_NT),
)

UNKNOWN = 'UNKNOWN'

# CHLORINE SOURCE
CHLORINE_SOURCE_BLEACH = 'BLEACH'
CHLORINE_SOURCE_SWG = 'SWG'  # salt water, generator
CHLORINE_SOURCE_TRICHLOR = 'TRICHLOR'

CHLORINE_SOURCE_CHOICES = (
    (CHLORINE_SOURCE_BLEACH, CHLORINE_SOURCE_BLEACH),
    (CHLORINE_SOURCE_SWG, CHLORINE_SOURCE_SWG),
    (CHLORINE_SOURCE_TRICHLOR, CHLORINE_SOURCE_TRICHLOR),
)

# Pool surface
POOL_SURFACE_PLASTER = 'PLASTER'
POOL_SURFACE_VINYL = 'VINYL'
POOL_SURFACE_FIBERGLASS = 'FIBERGLASS'
POOL_SURFACE_CHOICES = (
    (POOL_SURFACE_PLASTER, POOL_SURFACE_PLASTER),
    (POOL_SURFACE_VINYL, POOL_SURFACE_VINYL),
    (POOL_SURFACE_FIBERGLASS, POOL_SURFACE_FIBERGLASS),
)

POOL_TYPE_POOL = 'POOL'
POOL_TYPE_SPA = 'SPA'
POOL_TYPE_CHOICES = (
    (POOL_TYPE_POOL, POOL_TYPE_POOL),
    (POOL_TYPE_SPA, POOL_TYPE_SPA),
)

# CHEMISTRY NAME
class Chemistry(Enum):
    PH = 'PH'
    CH = 'CalciumHardness'  # total hardness
    FC = 'FreeChlorine'
    TC = 'TotalChlorine'
    TB = 'TotalBromine'
    TA = 'TotalAlkainity'
    CYA = 'CyanuricAcid'  # Cyanuric Acid，CYA/Stabiliser
    SALT = 'Salt'


TARGET_RANGE = {
    Chemistry.PH.value: {
        'min': 7.2,
        'mean': 7.4,
        'max': 7.6,
    },
    Chemistry.CH.value: {  # ppm
        'min': 150,
        'mean': 200,
        'max': 250,
    },
    Chemistry.FC.value: {  # ppm
        'min': 2,
        'mean': 3,
        'max': 4,
    },
    Chemistry.TA.value: {  # ppm
        'min': 80,
        'mean': 100,
        'max': 120,
    },
    # Chemistry.TOTAL_BROMINE.value: {  # ppm, SPA only
    #     'min': 80,
    #     'mean': 100,
    #     'max': 120,
    # },
    Chemistry.TC.value: {  # ppm
        'min': 0,
        'mean': 1,
        'max': 2,
    },
    Chemistry.CYA.value: {  # ppm
        'min': 40,
        'mean': 70,
        'max': 100,
    },
    Chemistry.SALT.value: {  # ppm
        'min': 3500,
        'mean': 4000,
        'max': 4500,
    }
}
