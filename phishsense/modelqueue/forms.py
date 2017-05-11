from django import forms

class URLForm(forms.Form):
	analysis_url = forms.URLField(label='Analysis URL', required=True)

