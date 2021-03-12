from core.constants import Chemistry, TARGET_RANGE


def calculate_ph(current_ph, ta, volume):
    """volume in litre"""
    target=TARGET_RANGE[Chemistry.PH.value]['mean']

    delta = target - current_ph
    if abs(delta) <= 0.2:
        return None, None

    delta = delta * (volume / 3.78541)
    temp = (current_ph + target) / 2
    adj = (192.1626 + -60.1221 * temp + 6.0752 * temp * temp + -0.1943 * temp * temp * temp) * (ta + 13.91) / 114.6
    delta = delta * adj

    if current_ph < target:
        # too low
        result = delta / 218.68
        result = result * 28.3495 + 0.5
    else:
        # too high
        result = (delta / -240.15)
        result = result * 0.0283595 + 0.5
    return result


def CSI(PH,TA,CH,CYA,Salt,Borate,Temp):
{
	if PH<6or PH>9or isNaN(PH)):
        return("PH Err")

	if document.F.Units.selectedIndexnot =1) Temp=(parseInt(Temp)-32)*5/9
	else Temp=parseInt(Temp)

	CarbAlk = TA - 0.38772*CYA/(1+Math.pow(10,6.83-PH)) -
		4.63*Borate/(1+Math.pow(10,9.11-PH))
	extra_NaCl = Salt - 1.1678*CH
	if extra_NaCl<0) extra_NaCl=0
	Ionic = (1.5*CH+1*TA)/50045 + extra_NaCl/58440
	CSI = PH-11.677 + Math.log(CH)/Math.LN10 + Math.log(CarbAlk)/Math.LN10 -
		2.56*Math.sqrt(Ionic)/(1+1.65*Math.sqrt(Ionic)) -
		1412.5/(Temp+273.15) + 4.7375
	return(Math.floor(CSI*100+0.5)/100)
	}
	}
	}
	}
	}
