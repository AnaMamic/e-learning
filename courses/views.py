from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from .models import Course, Chapter,Notification,Lesson,LessonFile
from django.views.generic.edit import CreateView
from .forms import CreateNewCourse, AddEditNotification,AddEditChapter, AddEditLesson, StudentForm,AddFile

from django.contrib.auth.decorators import login_required
from user_auth.views import group_required, searchbar


# Create your views here.


def home(request):
    if searchbar(request): return searchbar(request)
    return render(request,'base.html', {})


def index(request):
    if searchbar(request): return searchbar(request)
    courses_list= Course.objects.all()

    return render(request,'courses/all_courses.html',{'courses_list':courses_list})


def course_description(request,course_slug):
    if searchbar(request): return searchbar(request)
    course = get_object_or_404(Course,slug=course_slug)

    return render(request,'courses/course_description.html',{'course':course})

def about(request): 
    if searchbar(request): return searchbar(request)
    return render(request, 'about.html', {})

def contact(request): 
    if searchbar(request): return searchbar(request)
    return render(request, 'contact.html', {})




@login_required
@group_required('professor', 'student')
def my_courses(request):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    user_professor=False

    if request.user.groups.filter(name='professor').exists():
        user_professor=True
        
        try:
            courses_list=Course.objects.filter(professor=request.user)
        except Course.DoesNotExist:
            courses_list=[]
            

    else:
        try:
            courses_list=Course.objects.filter(student=request.user)
        except Course.DoesNotExist:
            courses_list=[]
    
    return render(request,'courses/my_courses.html',{'is_professor':user_professor,'courses_list':courses_list,})


@group_required('professor', 'student')
def course_detail(request,course_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course=get_object_or_404(Course, slug=course_slug)
    professor=False
    if request.user.groups.filter(name='professor').exists():
        if course.professor==request.user:
            professor=True
        else:
            raise PermissionDenied
    else:
        if not request.user.student.filter(slug = course_slug).exists():
            raise PermissionDenied
    return render(request,'courses/course_detail.html',{'course':course,'is_professor':professor})

@group_required('professor')
def create_edit_course(request,course_slug=None):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    if course_slug is not None:
        course= get_object_or_404(Course,slug=course_slug)
        if course.professor!=request.user:
            raise PermissionDenied
        cancel="courses:course_detail"
        title="Edit: "+course.name
    else:
        course=None
        cancel="courses:my_courses"
        title="New course"

    form=CreateNewCourse(request.POST or None, request.FILES or None,instance=course)
    if form.is_valid():
        new_course=form.save(commit=False)
        new_course.professor=request.user
        new_course.save()
        if course_slug is not None:
            return HttpResponseRedirect(reverse('courses:course_detail',kwargs={'course_slug':course_slug},))
        else:
            return HttpResponseRedirect(reverse('courses:my_courses'))

    return render(request,'courses/edit_add.html',{'form':form,'is_course':True,'course':course,'title':title,'cancel':cancel,'add_students':False})

@group_required('professor')
def delete_course(request,course_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course =get_object_or_404(Course, slug=course_slug)
    if course.professor!=request.user:
        raise PermissionDenied
    course.delete()
    return HttpResponseRedirect(reverse('courses:my_courses'))




@group_required('professor')
def add_edit_chapter(request, course_slug, chapter_slug=None):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course =get_object_or_404(Course, slug=course_slug)

    if course.professor!=request.user:
        raise PermissionDenied
    
    chapter = get_object_or_404(Chapter,slug=chapter_slug) if chapter_slug else None
 
    if chapter is not None and chapter.course == course:
        title="Edit chapter: %s" %(chapter)
    elif chapter is None:
        title="Add new chapter"
    else:
        raise Http404

    form = AddEditChapter(request.POST or None, instance=chapter)
    if form.is_valid():
        chapter= form.save(commit=False)
        chapter.course=course
        chapter.save()
        return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'course_slug':course_slug},))

    return render(request,'courses/edit_add.html',{'form':form,'course':course,'title':title,'cancel':"courses:course_detail",'add_students':False})



@group_required('professor')
def delete_chapter(request,course_slug,chapter_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course =get_object_or_404(Course, slug=course_slug)

    if course.professor!=request.user:
        raise PermissionDenied
    
    chapter = get_object_or_404(Chapter,slug=chapter_slug)

    if chapter.course != course:
        raise Http404

    chapter.delete()
    return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'course_slug':course_slug},))

@group_required('professor')
def create_edit_notification(request,course_slug,notification_slug=None):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course= get_object_or_404(Course,slug=course_slug)
    
    if course.professor != request.user:
        raise PermissionDenied

    notification = get_object_or_404(Notification,slug=notification_slug) if notification_slug else None

    if notification is not None and notification.course==course:
        title="Edit notification: %s" %(notification)
    elif notification is None:
        title="Create new notification"
    else:
        raise Http404

    form = AddEditNotification(request.POST or None, instance=notification)
    if form.is_valid():
        notification=form.save(commit=False)
        notification.course=course
        notification.save()
            
        return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'course_slug':course_slug},))
    return render(request,'courses/edit_add.html',{'form':form,'course':course,'title':title,'cancel':"courses:course_detail",'add_students':False})

@group_required('professor')
def delete_notification(request,course_slug,notification_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course= get_object_or_404(Course,slug=course_slug)

    if course.professor != request.user:
        raise PermissionDenied

    notification = get_object_or_404(Notification,slug=notification_slug)

    if notification.course!= course:
        raise Http404

    notification.delete()
    return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'course_slug':course_slug},))



@group_required('professor')
def add_edit_lesson(request, course_slug,chapter_slug,lesson_slug=None):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course = get_object_or_404(Course,slug=course_slug)

    if course.professor != request.user:
        raise PermissionDenied


    chapter=get_object_or_404(Chapter,slug=chapter_slug)

    if chapter.course != course:
        raise Http404

    if lesson_slug is not None:
        lesson = get_object_or_404(Lesson,slug=lesson_slug)
        if lesson.chapter != chapter:
            raise Http404
        title= "Edit lesson: %s" %(lesson)
        cancel="courses:lesson"
        
    else:
        lesson = None
        title= "Add new lesson"
        cancel="courses:course_detail"

    form =  AddEditLesson(request.POST or None,instance=lesson)

    if form.is_valid():
        lesson= form.save(commit=False)
        lesson.chapter=chapter
        lesson.save()

        return HttpResponseRedirect(reverse('courses:lesson', kwargs={'course_slug':course_slug,'chapter_slug':chapter_slug,'lesson_slug':lesson.slug,},))

    return render(request,'courses/edit_add.html',{'form':form,'course':course,'title':title,'cancel':cancel,'lesson':lesson,'add_students':False})

@group_required('professor')
def delete_lesson(request,course_slug,chapter_slug,lesson_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course = get_object_or_404(Course,slug=course_slug)

    if course.professor != request.user:
        raise PermissionDenied

    chapter=get_object_or_404(Chapter,slug=chapter_slug)

    if chapter.course != course:
        raise Http404

    lesson = get_object_or_404(Lesson,slug=lesson_slug)

    if lesson.chapter != chapter:
        raise Http404

    lesson.delete()

    return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'course_slug':course_slug},))


@group_required('professor', 'student')
def lesson_detail(request,course_slug,chapter_slug,lesson_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course = get_object_or_404(Course,slug=course_slug)


    user_professor=False
    

    if request.user.groups.filter(name='professor').exists():
        user_professor=True
        if course.professor != request.user:
            raise PermissionDenied
    else:
        if not request.user.student.filter(slug = course_slug).exists():
            raise PremissionDenied

    chapter=get_object_or_404(Chapter,slug=chapter_slug)

    if chapter.course != course:
        raise Http404

    lesson = get_object_or_404(Lesson,slug=lesson_slug)

    if lesson.chapter != chapter:
        raise Http404

    try:
        files_list=LessonFile.objects.filter(lesson=lesson)
    except Course.DoesNotExist:
        files_list=[]

    return render(request,'courses/lesson_detail.html',{'course':course,'lesson':lesson,'is_professor':user_professor,'pdffiles':files_list})


@group_required('professor')
def course_student(request,course_slug):
    if searchbar(request): return searchbar(request)
    if not request.user.is_active: 
            return render(request, 'courses/notactive.html', {})
    course=get_object_or_404(Course,slug=course_slug)

    if course.professor != request.user:
        raise PermissionDenied

    form = StudentForm(request.POST or None,instance=course)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'course_slug':course_slug},))
    
    return render(request,'courses/edit_add.html',{'form':form,'course':course,'cancel':"courses:course_detail",'add_students':True,'cancel':"courses:course_detail",'title':"Students"})


def can_add_see_file(request,course_slug,chapter_slug,lesson_slug,file_slug,professor):
    course=get_object_or_404(Course,slug=course_slug)

    if professor:
        if course.professor != request.user:
            raise PermissionDenied
    else:
        if not request.user.student.filter(slug = course_slug).exists():
            raise PermissionDenied

    chapter=get_object_or_404(Chapter,slug=chapter_slug)

    if chapter.course != course:
        raise Http404

    lesson = get_object_or_404(Lesson,slug=lesson_slug)

    if lesson.chapter != chapter:
        raise Http404

    if file_slug!="":
        lesson_file= get_object_or_404(LessonFile,slug=file_slug)
        if lesson_file.lesson!=lesson:
            raise Http404
        else:
            return lesson_file
    else:
        return {'course':course,'chapter':chapter,'lesson':lesson}



@group_required('professor')
def add_file(request,course_slug,chapter_slug,lesson_slug):
    elements=can_add_see_file(request,course_slug,chapter_slug,lesson_slug,"",True)

    form = AddFile(request.POST or None,request.FILES or None)
    if form.is_valid():
        lessonfile=form.save(commit=False)
        lessonfile.lesson =elements['lesson']
        lessonfile.save()
        return HttpResponseRedirect(reverse('courses:lesson', kwargs={'course_slug':course_slug,'chapter_slug':chapter_slug,'lesson_slug':lesson_slug,},))

    return render(request,'courses/edit_add.html',{'form':form,'course':elements['course'],'title':"Add lesson file",'cancel':"courses:lesson",'lesson':elements['lesson'],'add_students':False})


@group_required('professor')
def delete_file(request,course_slug,chapter_slug,lesson_slug,file_slug):
    lessonFile=can_add_see_file(request,course_slug,chapter_slug,lesson_slug,file_slug,True)
    lessonFile.delete()
    return HttpResponseRedirect(reverse('courses:lesson', kwargs={'course_slug':course_slug,'chapter_slug':chapter_slug,'lesson_slug':lesson_slug,},))


@group_required('professor', 'student')
def show_pdf_file(request,course_slug,chapter_slug,lesson_slug,file_slug):
    professor=False
    if request.user.groups.filter(name='professor').exists():
        professor=True

    lessonFile=can_add_see_file(request,course_slug,chapter_slug,lesson_slug,file_slug.lower(),professor)

    file_data=open(lessonFile.pdf_file.path,'rb').read()
    return HttpResponse(file_data, content_type="application/pdf")

