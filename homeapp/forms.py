from django import forms
from homeapp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import login,logout,authenticate
from homeapp.models import Address,Membership


class UserAdminCreationForm(forms.ModelForm):
    '''
    form for creating new users
    '''
    password1 = forms.CharField(label='Password',widget= forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)
    class Meta:
        model= CustomUser
        fields=('email','password1','lastname','firstname')

    def clean_password2(self):
        #check to make sure the two passwords enter matches

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
# this form is for custom user admin, since we are not using the default django authentification system


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = CustomUser
        fields = ('email', 'active', 'admin','firstname','lastname')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter a password','class':'input--style-4'}))
    password2 = forms.CharField(label = 'Confirm password',widget=forms.PasswordInput(attrs={'placeholder':'Confirm password','class':'input--style-4'}))

    class Meta:

        model = CustomUser
        widgets={
            'gender':forms.Select(attrs={'class':'input-text'}),
            'number':forms.NumberInput(attrs={'placeholder':'Enter Number','class':'input-text'}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter your email','class':'input-text'}),
            'lastname':forms.TextInput(attrs={'placeholder':'Enter your lastname ','class':'input-text'}),
            'firstname':forms.TextInput(attrs={'placeholder':'Enter your firstname ','class':'input-text'}),
            
        }
        exclude= ('slug','created','me')
        fields = ('gender','number','email', 'firstname','lastname')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs    = CustomUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email Taken')
        return  email
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords donot match')

        return password2


# setting up user adddress 

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        widgets={
            'address1':forms.TextInput(attrs={'class':'input-text'}),
            'address2':forms.TextInput(attrs={'class':'input-text'}),
            'town':forms.TextInput(attrs={'class':'input-text'}),
            'region':forms.TextInput(attrs={'class':'input-text'}),
        }
        exclude=('created','user')
        fields=('address1','address2','town','region')


class Membershipform(forms.ModelForm):
    class Meta:
        model=Membership
        widgets={
            'membership':forms.Select(attrs={'class':'input-select'}),
            'sellingmethod':forms.Select(attrs={'class':'input-select'}),
            'affilates':forms.Select(attrs={'class':'input-select'}),
        }
        exlude=('user','created')
        fields=('membership','affilates','sellingmethod')


class LoginForm(forms.Form):
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'email','placeholder':'Enter your Email','autofocus':'True'}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'email','placeholder':'Enter your password'}))
    def clean_password(self):
        username=self.cleaned_data.get('email')
        passw=self.cleaned_data.get('password')
        print(passw)
        user = authenticate(username=username,password=passw)
        if not user or not user.is_active:
            raise forms.ValidationError("Username or Password incorrect")
        
        return passw

