from django import forms

from receita.core.models import Comment



class CNPJForm(forms.Form):
    cnpj = forms.CharField(label='CNPJ', max_length=18, min_length=14)

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        if not cnpj.isdigit():
            raise forms.ValidationError('CNPJ só pode conter números.')
        return cnpj


class CommentForm(forms.ModelForm):
    text = forms.CharField(label=False, widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ('text',)