
from django import forms


class SearchCompoundForm(forms.Form):

    query = forms.CharField(label='Search for a compound ...', max_length=100)

    def clean_query(self):
    	data = self.cleaned_data['query']
    	return data