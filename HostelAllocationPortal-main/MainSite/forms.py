from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError
import datetime

YEARS= [x for x in range(2022,2023)]

class UserForm(UserCreationForm):
    password1 = forms.CharField(min_length=8, max_length=30, widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'same as your roll no.',
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'student_name',
            'father_name',
            'enrollment_no',
            'course',
            'dob',
            'gender']


class SelectionFormFloor(forms.Form):
    preference1 = forms.ChoiceField(choices=[(x, x) for x in range(101, 111)])
    preference2 = forms.ChoiceField(choices=[(x, x) for x in range(101, 111)])
    preference3 = forms.ChoiceField(choices=[(x, x) for x in range(101, 111)])
    preference4 = forms.ChoiceField(choices=[(x, x) for x in range(101, 111)])
    preference5 = forms.ChoiceField(choices=[(x, x) for x in range(101, 111)])

class UploadForm(forms.Form):
    aadharCard = forms.CharField()
    photoId = forms.CharField()
    feeReciept = forms.CharField()


class VerificationForm(forms.Form):
    def __init__(self, students ,*args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        for student in students:
            if student.documnets_aproved == False:
                self.fields[student.enrollment_no] = forms.BooleanField(required=False)


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=False))


class DateInput(forms.DateInput):
    input_type = 'date'


class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    reason = forms.CharField(max_length=100, help_text='100 characters max.',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter Reason here'}))
    class Meta:
        model = Leave
        fields = [
            'start_date',
            'end_date',
            'reason']
class RepairForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['repair']


class RebateForm(forms.Form):
    rebate = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
