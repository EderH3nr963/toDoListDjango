from django import forms

class ForgotPasswordStep1Form(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Digite seu email'
        })
    )

class ForgotPasswordStep2Form(forms.Form):
    verification_code = forms.CharField(
        label='Código de Verificação',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Digite o código enviado'
        })
    )

class ForgotPasswordStep3Form(forms.Form):
    new_password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Digite sua nova senha'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Confirme sua nova senha'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem')
        
        return cleaned_data 