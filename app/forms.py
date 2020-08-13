from django import forms


from .models import Mouvement,EmplacementMPTT


class InForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['dossier', 'emplacement']


    def __init__(self, *args, **kwargs):
        super(InForm, self).__init__(*args, **kwargs)
        self.fields['dossier'].disabled = True


class OutForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['dossier', 'agent']

    def __init__(self, *args, **kwargs):
        super(OutForm, self).__init__(*args, **kwargs)
        self.fields['dossier'].disabled = True

