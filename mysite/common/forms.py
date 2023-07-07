from django import forms
from .models import UserInfo, UserOption

class SignupForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=UserInfo.GENDER_CHOICES, widget=forms.Select(), required=True)
    age = forms.ChoiceField(choices=UserInfo.AGE_CHOICES, widget=forms.Select(), required=True)
    pw = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserInfo
        db_table = 'user_info'
        fields = ['email', 'pw', 'gender', 'age']
        labels = {
            'email':'이메일',
            'pw':'비밀번호',
            'gender':'성별',
            'age':'연령대',
        }

    def clean_pw(self):
        pw = self.cleaned_data.get('pw')
        if len(pw) < 8:
            raise forms.ValidationError("비밀번호는 8글자 이상이어야 합니다.")
        return pw

class SubscribeForm(forms.ModelForm):
    reception_time = forms.ChoiceField(choices=UserOption.TIME_CHOICES,
                                       widget=forms.RadioSelect, required=True)
    weekend = forms.ChoiceField(choices=UserOption.WEEKEND_CHOICES,
                                widget=forms.RadioSelect, required=True)
    book_service = forms.ChoiceField(choices=UserOption.BOOKSERVICE_CHOICES,
                                     widget=forms.RadioSelect, required=True)
    class Meta:
        model = UserOption
        db_table = 'user_option'
        fields = ['email','reception_time','weekend','book_service']