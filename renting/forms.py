from django import forms


class SearchForm(forms.Form):
    name = forms.CharField(max_length=34, required=False)
    capacity_from = forms.IntegerField(required=False)
    capacity_to = forms.IntegerField(required=False)
    has_projector = forms.BooleanField(widget=forms.CheckboxInput, required=False)
