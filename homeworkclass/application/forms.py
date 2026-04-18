from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
import datetime as dt


class AssignmentCreation(forms.Form):
    name = forms.CharField()
    grade_importance = forms.IntegerField(
        min_value=1,
        max_value=3,
        widget=forms.NumberInput(
            attrs={
                "class": "bg-white rounded-xl p-1 text-lg border text-slate-900 m-1 dark:text-slate-200 dark:bg-slate-800"
            }
        ),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "w-full p-3 rounded-xl border border-slate-200 bg-white dark:bg-slate-900 outline-none resize-none ",
            }
        ),
    )
    time_to_end = forms.DateField(
        initial=dt.date.today,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    upload_after_time = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "scale-150 m-1"}),
    )

    class Meta:
        fields = [
            "name",
            "grade_importance",
            "describtion",
            "time_to_end",
            "upload_after_time",
        ]


class UploadFile(forms.Form):
    uploaded_file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "peer inset-0 absolute w-full h-full opacity-0 cursor-pointer"
            }
        ),
    )

    class Meta:
        fields = ["uploaded_file"]


class CreateUser(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]
