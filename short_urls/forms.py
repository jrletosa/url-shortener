from django import forms

class UrlForm(forms.Form):
	long_url = forms.URLField(max_length=1024, 
        widget=forms.TextInput(attrs={'class' : 'form-control'}))