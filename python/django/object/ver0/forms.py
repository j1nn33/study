from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


from .models import Vch

class VchForm(forms.ModelForm):

    class Meta:
        model = Vch
        fields = ('number_vch',
                  'okrug',
                  'oblast',
                  'town',
                  'vch_info',
                  'manager',
                  'name',
                  'serial',
                  'serial_number',
                  'warranty',
                  'izdel_info',
                  'server_standart',
                  'arm_standart',
                  'laptop_standart',
                  'switch_standart',
                  'supp_standart',
                  'server_add',
                  'arm_add',
                  'laptop_add',
                  'switch_add',
                  'supp_add',
                  'server_total',
                  'arm_total',
                  'switch_total',
                  'laptop_total',
                  )


