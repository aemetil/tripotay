from allauth.account.forms import SignupForm, LoginForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Non itilizatè oswa imèl',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Modpas ou',
        })


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Non itilizatè',
            'email': 'imèl@example.com',
            'password1': 'Kreye yon modpas solid',
            'password2': 'Repete modpas la',
        }
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]
