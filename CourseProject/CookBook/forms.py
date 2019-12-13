from django import forms
from django.forms import ModelForm

# Форма для ввода данных по регистрации
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

# Используемые модели БД
from .models import CBUser, Recipe, Comment

"""Регистрация пользователя по сети"""


class RegisterUserForm(forms.ModelForm):
    """Объявление полей для создания электронной почты"""
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль(повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        """Выполняем валидацию пароля, введенного в первое поле, с применением доступных
        валидаторов пароля"""
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        """Проверка на совпадение обоих паролей"""
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # user.is_active = True                                     # В книжке False
        # user.is_activated = True                                  # В книжке False
        if commit:
            user.save()
        return user

    class Meta:
        model = CBUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


"""Форма изменения пользовательских данных"""


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = CBUser
        fields = ('username', 'email', 'first_name', 'last_name')


"""Класс-форма для создания рецепта"""


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


'''Коммент'''


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'body')
        widgets = {'user': forms.HiddenInput}


class SmallSearchForm(forms.Form):
    keyword = forms.CharField(required=True, max_length=30, label='')
