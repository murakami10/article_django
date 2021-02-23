from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import views
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class EmailAuthenticationForm(forms.Form):

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label=_("Password"), strip=False, widget=forms.PasswordInput
    )

    error_messages = {
        "invalid_login": "Eメールアドレス または パスワードに誤りがあります.",
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.email_filed = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.email_filed.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"email": self.email_filed.verbose_name},
                )
            else:
                self.confirm_login_allowd(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowd(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"], code="inactive"
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
