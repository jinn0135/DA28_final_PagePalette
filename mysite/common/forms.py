from django import forms
from .models import User, UserOption

class SignupForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES, widget=forms.RadioSelect)
    age = forms.ChoiceField(choices=User.AGE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        db_table = 'user'
        fields = ['email', 'pw', 'gender', 'age']

class SubscribeForm(forms.ModelForm):
    reception_time = forms.ChoiceField(choices=UserOption.TIME_CHOICES,
                                       widget=forms.RadioSelect)
    weekend = forms.ChoiceField(choices=UserOption.WEEKEND_CHOICES,
                                widget=forms.RadioSelect)
    book_service = forms.ChoiceField(choices=UserOption.BOOKSERVICE_CHOICES,
                                     widget=forms.RadioSelect)
    class Meta:
        model = UserOption
        db_table = 'option'
        fields = ['email','reception_time','weekend','book_service'
                  # 'large_category','middle_category','selected_book_isbn'
                  ]