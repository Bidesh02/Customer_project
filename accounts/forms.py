from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Issue

class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('name', 'email', 'age', 'gender', 'phone_number', 'date_of_birth')
        labels = {
            'name': 'User Name'
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.CUSTOMER
        if commit:
            user.save()
        return user

class ControllerSignUpForm(UserCreationForm):
    invite_code = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Invite Code'}),
        help_text="Required to register as a Controller."
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'name')

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        if code != 'ADMIN2026':
            raise forms.ValidationError("Invalid invite code. You are not authorized.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.CONTROLLER
        if commit:
            user.save()
        return user

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your issue here...'}),
        }
