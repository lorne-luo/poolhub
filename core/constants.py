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
    CALCIUM_HARDNESS = 'CALCIUM_HARDNESS'
    FREE_CHLORINE = 'FREE_CHLORINE'
    TOTAL_CHLORINE = 'TOTAL_CHLORINE'
    TOTAL_BROMINE = 'TOTAL_BROMINE'
    TOTAL_ALKAINITY = 'TOTAL_ALKAINITY'
    CYANURIC_ACID = 'CYANURIC_ACID'
