from django import forms

class SearchBox(forms.Form):
    query = forms.CharField(required=True)

class AddTrack(forms.Form):
    AddTrack = forms.BooleanField(required=False)

class JoinParty(forms.Form):
    party_id = forms.UUIDField(required=True)

class NewParty(forms.Form):
    new_party = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=True)
