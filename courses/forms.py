from django import forms
from .models import Course, Notification, Chapter, Lesson, LessonFile
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
import os

class CreateNewCourse(forms.ModelForm):
    class Meta(object):
        model = Course
        exclude = ['professor','student','slug']





class AddEditNotification(forms.ModelForm):
	class Meta(object):
		model=Notification
		fields=['name','text']

class AddEditChapter(forms.ModelForm):
	class Meta(object):
		model=Chapter
		fields=['name']
			

class AddEditLesson(forms.ModelForm):
	text = forms.CharField(widget=CKEditorWidget())
	class Meta(object):
		model=Lesson
		exclude = ['chapter','slug']





class StudentForm(forms.ModelForm):
	student = forms.ModelMultipleChoiceField(required=False,widget=FilteredSelectMultiple("Students", is_stacked=False),queryset=User.objects.filter(groups__name="student"))
	class Meta(object):
		model=Course
		fields= ['student',]

	class Media:
   		css = {'all': ('/static/admin/css/widgets.css',),}
   		js = ('/static/js/jsi18n.js',)

   	



class AddFile(forms.ModelForm):
	class Meta(object):
		model=LessonFile
		fields=['pdf_file']

	def clean(self):
		cleaned_data=super(AddFile,self).clean()
		if cleaned_data:
			lessonfile=cleaned_data.get('pdf_file')
			filename=lessonfile.name
			ext=os.path.splitext(filename)[1]
			if ext.lower() != '.pdf':
				raise forms.ValidationError("Not allowed filetype!")

		return cleaned_data




        
       




    

    

  


