from django import forms


from .models import Mouvement,EmplacementMPTT, Agent


class InForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['dossier', 'emplacement']


    def __init__(self, *args, **kwargs):
        super(InForm, self).__init__(*args, **kwargs)
        self.fields['dossier'].disabled = True
        print(kwargs)


class OutForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['dossier', 'agent']

    def __init__(self, *args, **kwargs):
        super(OutForm, self).__init__(*args, **kwargs)
        self.fields['dossier'].disabled = True
        print(kwargs)
        sens=kwargs['initial']['sens']
        if sens!='out':
            self.fields['agent'].queryset= Agent.objects.filter(categorie_agent__description=sens)