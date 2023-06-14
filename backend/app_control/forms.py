from app_control.utils import correios_postagem, correios_sedex
from .models import Devolucao, NotaDevolucao
from django import forms
from django.utils import timezone


class DevolucaoForm(forms.ModelForm):
    notas_devolucao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=True)
    email_choices = [
        ('mnascimento@dermage.com.br', 'mnascimento@dermage.com.br'),
        ('aguasclaras@dermage.com.br', 'aguasclaras@dermage.com.br'),
        ('aracaju@dermage.com.br', 'aracaju@dermage.com.br'),
        ('belem@dermage.com.br', 'belem@dermage.com.br'),
        ('belohorizonte@dermage.com.br', 'belohorizonte@dermage.com.br'),
        ('boavista@dermage.com.br', 'boavista@dermage.com.br'),
        ('asanorte2@dermage.com.br', 'asanorte2@dermage.com.br'),
        ('asasul@dermage.com.br', 'asasul@dermage.com.br'),
        ('barrashoppingsul@dermage.com.br', 'barrashoppingsul@dermage.com.br'),
        ('campinascambui@dermage.com.br', 'campinascambui@dermage.com.br'),
        ('campinascentro@dermage.com.br', 'campinascentro@dermage.com.br'),
        ('campinasguanabara@dermage.com.br', 'campinasguanabara@dermage.com.br'),
        ('campogrande@dermage.com.br', 'campogrande@dermage.com.br'),
        ('curitiba2@dermage.com.br', 'curitiba2@dermage.com.br'),
        ('caxiasdosul@dermage.com.br', 'caxiasdosul@dermage.com.br'),
        ('florianopolis@dermage.com.br', 'florianopolis@dermage.com.br'),
        ('fortaleza@dermage.com.br', 'fortaleza@dermage.com.br'),
        ('goiania@dermage.com.br', 'goiania@dermage.com.br'),
        ('ipatinga@dermage.com.br', 'ipatinga@dermage.com.br'),
        ('itaperuna@dermage.com.br', 'itaperuna@dermage.com.br'),
        ('joaopessoa@dermage.com.br', 'joaopessoa@dermage.com.br'),
        ('londrina@dermage.com.br', 'londrina@dermage.com.br'),
        ('maceio@dermage.com.br', 'maceio@dermage.com.br'),
        ('maraba@dermage.com.br', 'maraba@dermage.com.br'),
        ('mossoro@dermage.com.br', 'mossoro@dermage.com.br'),
        ('natal@dermage.com.br', 'natal@dermage.com.br'),
        ('brasiliaparkshopping@dermage.com.br',
         'brasiliaparkshopping@dermage.com.br'),
        ('canoas@dermage.com.br', 'canoas@dermage.com.br'),
        ('petropolis@dermage.com.br', 'petropolis@dermage.com.br'),
        ('portoalegre@dermage.com.br', 'portoalegre@dermage.com.br'),
        ('iguatemipoa@dermage.com.br', 'iguatemipoa@dermage.com.br'),
        ('recife@dermage.com.br', 'recife@dermage.com.br'),
        ('ribeiraopreto@dermage.com.br', 'ribeiraopreto@dermage.com.br'),
        ('rioverde@dermage.com.br', 'rioverde@dermage.com.br'),
        ('salvador@dermage.com.br', 'salvador@dermage.com.br'),
        ('santarem@dermage.com.br', 'santarem@dermage.com.br'),
        ('santamaria@dermage.com.br', 'santamaria@dermage.com.br'),
        ('sjrp@dermage.com.br', 'sjrp@dermage.com.br'),
        ('teresina@dermage.com.br', 'teresina@dermage.com.br'),
        ('teresopolis@dermage.com.br', 'teresopolis@dermage.com.br'),
        ('uberlandia1@dermage.com.br', 'uberlandia1@dermage.com.br'),
        ('vilavelha@dermage.com.br', 'vilavelha@dermage.com.br'),
        ('vitoria@dermage.com.br', 'vitoria@dermage.com.br'),
        ('saoluis1@dermage.com.br', 'saoluis1@dermage.com.br'),
        ('uberaba@dermage.com.br', 'uberaba@dermage.com.br'),
        ('brasiliasudoeste@dermage.com.br', 'brasiliasudoeste@dermage.com.br'),
        ('manaus@dermage.com.br', 'manaus@dermage.com.br'),
        ('voltaredonda@dermage.com.br', 'voltaredonda@dermage.com.br')
    ]
    email = forms.ChoiceField(choices=email_choices)

    class Meta:
        model = Devolucao
        fields = ['codigo_postagem', 'notas_devolucao',
                  'data', 'email']
        widgets = { 
            'data': forms.DateInput(attrs={'type': 'date'}),
            'notas_devolucao': forms.Textarea(attrs={'rows': 4}),
                   }

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

        devolucao.status = correios_postagem(
            self.cleaned_data.get("codigo_postagem"))
        devolucao.codigo_sedex = correios_postagem(
            self.cleaned_data.get("codigo_postagem"))
        print('status e sedex', devolucao.status, devolucao.codigo_sedex)
        if commit:
            devolucao.save()
        return devolucao
