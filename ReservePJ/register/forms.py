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
from .function import calc_end_time
import datetime
from django.db.models import Q

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.label == '予約日':
                field.widget.attrs["class"] += " date_input"
            if field.label == '予約開始時間':
                field.widget.attrs["class"] += " time_input"
    
    def clean(self):
        #フォームの入力情報を取得
        cleaned_data = super().clean()
        r_seats = cleaned_data.get('seats')
        r_day = cleaned_data.get('reserve_day')
        r_time_start = cleaned_data.get('reserve_start_time')
        r_zone = cleaned_data.get('reserve_hour_zone')
        r_time_end = calc_end_time(r_time_start,r_zone)
        #モデルから入力情報と合致するレコードがあるかをチェック
        reserve_data = Reserve.objects.filter(Q(seats=r_seats),
                                              Q(reserve_day=r_day),
                                              Q(reserve_start_time__range=(r_time_start,r_time_end))|Q(reserve_end_time__range=(r_time_start,r_time_end)),
                                              Q(reserve_flg=True))
        print(reserve_data.query)
        if reserve_data.first() is not None:
                self.add_error(None,'既に予約済です') 
        return cleaned_data

    class Meta:
        model = Reserve
        fields = ('__all__')
        exclude = ('reserve_user','reserve_flg','reserve_end_time','reserve_time','change_time',)
        labels={
            'seats':'予約席',
            'reserve_day':'予約日',
            'reserve_start_time':'予約開始時間',
            'reserve_hour_zone':'予約時間数',
            }

class ReserveUpdateForm(forms.ModelForm):
    """予約情報更新フォーム"""

    def __init__(self, *args, **kwargs):
        #[pk]にViewから渡されたpk(reserve_id)を代入
        self.pk  = kwargs.pop('reserve_id')
        super(ReserveUpdateForm,self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.label == '予約日':
                field.widget.attrs["class"] += " date_input"
            if field.label == '予約開始時間':
                field.widget.attrs["class"] += " time_input"
    

    def clean(self):
        #フォームの入力情報を取得
        cleaned_data = super().clean()
        r_id = self.pk
        r_seats = cleaned_data.get('seats')
        r_day = cleaned_data.get('reserve_day')
        r_time_start = cleaned_data.get('reserve_start_time')
        r_zone = cleaned_data.get('reserve_hour_zone')
        r_time_end = calc_end_time(r_time_start,r_zone)
        #モデルから入力情報と合致するレコードがあるかをチェック
        reserve_data = Reserve.objects.filter(Q(seats=r_seats),
                                              Q(reserve_day=r_day),
                                              Q(reserve_start_time__range=(r_time_start,r_time_end))|Q(reserve_end_time__range=(r_time_start,r_time_end)),
                                              Q(reserve_flg=True)).exclude(pk=r_id)

        print(reserve_data.query)
        if reserve_data.first() is not None:
                self.add_error(None,'既に予約済です') 
        return cleaned_data

    class Meta:
        model = Reserve
        fields = ('__all__')
        exclude = ('reserve_user','reserve_end_time','reserve_time','change_time',)
        labels={
            'seats':'予約席',
            'reserve_day':'予約日',
            'reserve_start_time':'予約開始時間',
            'reserve_hour_zone':'予約時間数',
            'reserve_flg':'予約フラグ',
            }

class ReserveChangeForm(forms.ModelForm):
    """未使用：席予約情報更新フォーム"""
    #ReserveChangeFormSetを使用してフォームセットを表示
    #即ち、複数のフォームを表示しているが表示条件（対象）を選択しないとかなり重い
    #このコードではログインユーザーIDの予約情報のみで絞っているがそれでも重い
    #そのため上記のUpdateViewで対応

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.label == '予約日':
                field.widget.attrs["class"] += " date_input"
            if field.label == '予約開始時間':
                field.widget.attrs["class"] += " time_input"

    class Meta:
        model = Reserve
        fields = ('seats','reserve_day','reserve_start_time','reserve_hour_zone','reserve_flg')
        labels={
            'seats':'予約席',
            'reserve_day':'予約日',
            'reserve_start_time':'予約開始時間',
            'reserve_hour_zone':'予約時間数',
            'reserve_flg':'キャンセルフラグ'
            }

### 未使用:modelformset_factoryはFormSetクラスを返します
ReserveChangeFormSet = forms.modelformset_factory(
    Reserve, form=ReserveChangeForm, extra=0
)