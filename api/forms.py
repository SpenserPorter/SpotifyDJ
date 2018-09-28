from django import forms

class SearchBox(forms.Form):
    query = forms.CharField(required=True)
