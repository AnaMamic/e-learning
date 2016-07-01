from django.shortcuts import render
from .models import CustomUser
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from .mail_data import * 
from courses.models import Course
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def group_required(*group_names):    
        ### treba biti clan neke od poslanih grupa    
        def in_groups(u):       
                if u.is_authenticated():            
                        if bool(u.groups.filter(name__in=group_names)):
                                return True        
                        return False    
        return user_passes_test(in_groups)


### searchbar da moze radit u svakom viewu
def searchbar(request=None): 
    queryset_list = Course.objects.all() 
    query = request.GET.get("q")
    if query: 
        queryset_list = queryset_list.filter(name__icontains=query)
        paginator = Paginator(queryset_list, 12)
        page = request.GET.get('page')
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        context = {
            "object_list": queryset,
            "title": "Index"
        }

        return render(request, "courses/search_results.html", context)




def CustomUserRegistration(request):
	if searchbar(request): return searchbar(request)
	if request.user.is_authenticated(): 
		return HttpResponseRedirect('/')
	if request.method == 'POST': 
		form = RegistrationForm(request.POST)
		if form.is_valid(): 
			user = User.objects.create_user(username=form.cleaned_data.get('username'),
				email = form.cleaned_data.get('email'), 
				password = form.cleaned_data.get('password'), 
				first_name = form.cleaned_data.get('first_name'),
				last_name = form.cleaned_data.get('last_name'),
				) 
			cstm_usr = CustomUser(user=user, professor=form.cleaned_data.get('professor'))
			if cstm_usr.professor == True: 
				### neaktivan dok ne posalje podatke 
				user.is_active = False
				user.save()
				cstm_usr.save()
				send_mail(mail_subject, mail_message, mail_sender, [user.email], fail_silently=False)
				user.groups.add(Group.objects.get(name='professor'))
				#return HttpResponseRedirect('/')
				return render(request, 'registration_complete_professor.html', {})
			else: 
				user.save()
				user.groups.add(Group.objects.get(name='student'))
				#return HttpResponseRedirect('/')
				return render(request, 'registration_complete_student.html', {})
		else: 
			return render(request, 'register.html', {"form": form})
	else: 
		### nista ni ne salje 
		### salji praznu formu 
		form = RegistrationForm()
		return render(request, 'register.html', {"form": form})

def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')



def LoginRequest(request): 
	if searchbar(request): return searchbar(request)
	if request.user.is_authenticated(): 
		return HttpResponseRedirect('/')
	if request.method == 'POST': 
		form = LoginForm(request.POST)
		if form.is_valid(): 
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			cstm_usr = authenticate(username=username, password=password)
			if cstm_usr is not None: 
				login(request, cstm_usr)
				return HttpResponseRedirect('/')
			else: 
				return render(request, 'login.html', {"form": form})
		else: 
			return render(request, 'login.html', {"form": form})
	else: 
		form = LoginForm()
		return render(request, 'login.html', {"form": form})