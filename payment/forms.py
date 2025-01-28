from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):

    Full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}))
    Email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    address_1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}))
    address_2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}))
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    state = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}))
    country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
    class Meta:
        model = ShippingAddress
        fields = ['Full_name','Email','address_1','address_2','city','state','zipcode','country']
        exclude = ['user']
        