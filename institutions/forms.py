

from django import forms
from .models import Institution




class AddInstitution(forms.ModelForm):
	class Meta(object):
		model=Institution
		fields=["name"]

	def clean(self):
		cleaned_data=super(AddInstitution,self).clean()
		name=cleaned_data.get('name')

		if Institution.objects.filter(name__iexact=name).exists():
			raise forms.ValidationError("This institution already exists!")

		return cleaned_data





