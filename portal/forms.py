from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Resume


# ================= REGISTER FORM =================
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [ 'email', 'username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        
        # Check for special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(char in special_chars for char in password):
            raise forms.ValidationError("Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?).")
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Only check password match if both fields are present and password passed individual validation
        if password and confirm_password and password == confirm_password:
            return cleaned_data
        elif password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()  # recommended
        user.set_password(self.cleaned_data["password"])  # 🔥 HASH PASSWORD
        if commit:
            user.save()
        return user


# ================= PROFILE FORM =================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [ ]


# ================= RESUME FORM =================
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume_file']