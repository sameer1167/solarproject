from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):

    Full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),required=True)
    Email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}),required=True)
    address_1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}),required=True)
    address_2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}))
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),required=True)
    state = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),required=True)
    zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),required=True)
    country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),required=True)
    class Meta:
        model = ShippingAddress
        fields = ['Full_name','Email','address_1','address_2','city','state','zipcode','country']
        exclude = ['user']
        


class PaymentForm(forms.Form):
    card_number = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}),required=True)
    card_holder_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cardholder Name'}),required=True)
    expiry_date = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'MM/YY'}),required=True)
    cvv = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV'}),required=True)
    