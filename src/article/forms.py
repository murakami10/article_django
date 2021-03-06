import bootstrap_datepicker_plus as datetimepicker
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from .models import Article
from .models import ArticleCategory
from .models import Tag
from .models import User

UserModel = get_user_model()


class EmailAuthenticationForm(forms.Form):

    email = forms.EmailField(
        max_length=254, widget=forms.EmailInput(attrs={"autofocus": True}),
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


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "ユーザネーム"}


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "メールアドレス"}
        widgets = {
            "email": forms.EmailInput,
        }


class SingUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")
        labels = {"username": "ユーザ名"}


class PostArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ("author",)
        labels = {
            "title": "タイトル",
            "summary": "要約",
            "content": "内容",
            "publish_date": "投稿予定日",
            "category": "カテゴリー",
        }

        widgets = {
            "summary": forms.Textarea(attrs={"cols": 50}),
            "tag": forms.CheckboxSelectMultiple,
        }

    public = forms.BooleanField(label="記事を公開", initial=False, required=False,)

    tag = forms.ModelMultipleChoiceField(
        label="タグ",
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all(),
        required=False,
    )

    error_messages = {"future_date": "過去の日付になっています."}

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get("publish_date")

        if not self.is_future_date(publish_date):
            raise forms.ValidationError(
                self.error_messages["future_date"], code="future_date",
            )
        return publish_date

    def is_future_date(self, date):
        return date > timezone.now()

    @classmethod
    def form_with_prapare_article_data(cls, post: dict):
        params = {}
        for key in post.keys():
            params[key] = post[key]

        form = PostArticleForm(initial=params)
        return form


class PrepareArticleForm(forms.Form):

    title = forms.CharField(label="タイトル", max_length=255)
    summary = forms.CharField(
        label="要約", max_length=255, widget=forms.Textarea(attrs={"cols": 50})
    )
    publish_date = forms.DateTimeField(
        label="投稿日付",
        widget=datetimepicker.DateTimePickerInput(
            format="%Y-%m-%d %H:%M:%S",
            options={"locale": "ja", "dayViewHeaderFormat": "YYYY年 MMMM",},
        ),
    )
    category = forms.ModelChoiceField(
        label="カテゴリー", queryset=ArticleCategory.objects.all()
    )

    tag = forms.ModelMultipleChoiceField(
        label="タグ",
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all(),
        required=False,
    )

    error_messages = {"future_date": "過去の日付になっています."}

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get("publish_date")

        if not self.is_future_date(publish_date):
            raise forms.ValidationError(
                self.error_messages["future_date"], code="future_date",
            )
        return publish_date

    def is_future_date(self, date):
        return date > timezone.now()


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ("author",)
        labels = {
            "title": "タイトル",
            "summary": "要約",
            "content": "内容",
            "publish_date": "投稿予定日",
            "category": "カテゴリー",
        }
        widgets = {
            "summary": forms.Textarea(attrs={"cols": 50}),
        }

    public = forms.BooleanField(label="記事を公開", required=False,)

    tag = forms.ModelMultipleChoiceField(
        label="タグ",
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all(),
        required=False,
    )


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = "__all__"
        labels = {
            "name": "カテゴリ",
        }

        error_messages = {
            "name": {"unique": "すでにそのカテゴリは存在してます."},
        }


class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        labels = {
            "name": "タグ",
        }

        error_messages = {
            "name": {"unique": "すでにそのタグは存在してます."},
        }
