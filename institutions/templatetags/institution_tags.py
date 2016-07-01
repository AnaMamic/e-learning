from django import template
from institutions.models import Institution
register = template.Library()

@register.inclusion_tag("institutions_list.html")
def get_institutions():
	institutions= Institution.objects.all()
	return {'institutions':institutions}
