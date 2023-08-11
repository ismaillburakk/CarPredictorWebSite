from django import forms
from .models import Arac

class AracForm(forms.ModelForm):
    class Meta:
        model = Arac
        fields = ['Marka', 'Seri', 'Model', 'Yıl', 'Kilometre', 'VitesTipi', 'YakıtTipi', 'KasaTipi', 'MotorHacmi', 'MotorGücü', 'Çekiş', 'OrtYakıtTüketimi', 'YakıtDeposu']