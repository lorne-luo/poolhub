from django.forms import RadioSelect


class ButterflyRadioSelect(RadioSelect):
    template_name = 'widgets/butterfly_radio.html'
    option_template_name = 'widgets/butterfly_radio_option.html'
