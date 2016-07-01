from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from .models import Institution
from courses.models import Course
from .forms import AddInstitution
from user_auth.views import group_required
from user_auth.views import searchbar 

######GOTOVO######




#profesor
@group_required('professor')
def add_institution(request,course_slug=None):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course = get_object_or_404(Course,slug=course_slug) if course_slug else None
    if course is not None:
        if course.professor != request.user:
            raise PermissionDenied
        cancel='courses:edit_course'
    else:
        cancel= 'courses:create'
    form= AddInstitution(request.POST or None)
    title="Add new institution"
    if form.is_valid():
        form.save()
        if course_slug is None:
            return HttpResponseRedirect(reverse('courses:create'))
        else:
            return HttpResponseRedirect(reverse('courses:edit_course',kwargs={'course_slug':course_slug}))
    return render(request,'courses/edit_add.html',{'form':form,'course':course,'title':title,'cancel':cancel})


#svi
def institution_courses(request,institution_slug):
    if searchbar(request): return searchbar(request)
    institution = get_object_or_404(Institution,slug=institution_slug)

    courses_list= institution.course_set.all()

    return render(request,'courses/all_courses.html',{'courses_list':courses_list})

