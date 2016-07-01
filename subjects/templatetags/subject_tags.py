from django import template
from subjects.models import Subject
register = template.Library()

@register.inclusion_tag("subjects_list.html")
def get_subjects():
	subjects= Subject.objects.all()
	return {'subjects':subjects}