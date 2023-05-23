from app_control.utils import correios_scraper
from .models import Devolucao, NotaDevolucao
from django import forms
from django.utils import timezone


class DevolucaoForm(forms.ModelForm):
    notas_devolucao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=True)
    data_devolucao = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'value': timezone.now().strftime('%Y-%m-%d')}))
    email_choices = [
        ('email1@example.com', 'email1@example.com'),
        ('email2@example.com', 'email2@example.com'),
        ('email3@example.com', 'email3@example.com'),
    ]
    email = forms.ChoiceField(choices=email_choices)
    """ status = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)
    print() """

    class Meta:
        model = Devolucao
        fields = ['codigo_sedex', 'notas_devolucao',
                  'data_devolucao', 'email']

    def save(self, commit=True):
        notas = self.cleaned_data.get('notas_devolucao')
        devolucao = super().save(commit=False)
        if commit:
            devolucao.save()  # Salva a instância pai primeiro
        if notas:
            notas_list = notas.split('\n')
            for nota in notas_list:
                nota_devolucao = NotaDevolucao(
                    devolucao=devolucao, nota=nota.strip())
                nota_devolucao.save()
       
        devolucao.status = correios_scraper(self.cleaned_data.get("codigo_sedex"))
        if commit:
            devolucao.save()
        return devolucao
