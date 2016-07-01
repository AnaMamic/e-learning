
from django import forms
from .models import Subject


class AddSubject(forms.ModelForm):
	class Meta(object):
		model=Subject
		fields=["name"]

	def clean(self):
		cleaned_data=super(AddSubject,self).clean()
		name=cleaned_data.get('name')

		if Subject.objects.filter(name__iexact=name).exists():
			raise forms.ValidationError("This subject already exists!")

		return cleaned_data