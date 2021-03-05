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


# chemistry name
class Chemistry(Enum):
    PH = 'PH'
    CALCIUM_HARDNESS = 'CalciumHardness'
    FREE_CHLORINE = 'FreeChlorine'
    TOTAL_CHLORINE = 'TotalChlorine'
    TOTAL_BROMINE = 'TotalBromine'
    TOTAL_ALKAINITY = 'TotalAlkainity'
    CYANURIC_ACID = 'CyanuricAcid'
