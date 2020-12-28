
from django import forms
from register.models import User
from .models import *

class ReserveForm(forms.ModelForm):
    """席予約フォーム"""

    class Meta:
        model = Reserve
        fields = ('seats','reserve_user','reserve_date',)

