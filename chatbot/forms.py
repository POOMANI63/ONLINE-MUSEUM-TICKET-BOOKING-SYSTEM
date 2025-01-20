from django import forms

class UserDetailsForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    age = forms.IntegerField(label="Age")
    gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    email = forms.EmailField(label="Email")
