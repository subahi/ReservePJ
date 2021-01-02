from django import forms
from django.forms import models, modelformset_factory
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from .widgets import FileInputWithPreview
from reserve.models import Reserve
import bootstrap_datepicker_plus as datetimepicker
from django.forms.widgets import SplitDateTimeWidget 

User = get_user_model()


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email','last_name', 'first_name','image','profile',)
        widgets = {
            'image': FileInputWithPreview,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.label == 'プロフィール画像':
                field.widget.attrs["class"] += " preview-marker"

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('image','last_name', 'first_name','profile',)
        widgets = {
            'image': FileInputWithPreview,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.label == 'プロフィール画像':
                field.widget.attrs["class"] += " preview-marker"

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class DateInput(forms.DateInput):
    input_type = 'date'

class ReserveForm(forms.ModelForm):
    """席予約フォーム"""
    reserve_date = forms.SplitDateTimeField(label = "予約日時",
                                            widget=forms.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))
    class Meta:
        model = Reserve
        fields = ('__all__')
        exclude = ('reserve_user','reserve_flg','reserve_time','change_time',)
        labels={
            'seats':'予約席',
            'reserve_hour_zone':'予約時間数',
            }

#予約情報一覧表示、更新
class ReserveChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Reserve
        fields = ('seats','reserve_date','reserve_hour_zone','reserve_flg')


### modelformset_factoryはFormSetクラスを返します
ReserveChangeFormSet = forms.modelformset_factory(
    Reserve, form=ReserveChangeForm, extra=0
)