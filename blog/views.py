
from multiprocessing import context
from unicodedata import category
from urllib import request
from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from .models import Author, Blog, Profile, User,Comment, Category
from .forms import RegisterForm,ProfileForm,UserUpdateForm, CommentPostForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.urls import reverse
from taggit.models import Tag
from django.http import HttpResponse  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str   
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode    
from .token import account_activation_token 
from django.core.mail import EmailMessage 

# Create your views here.
def index(request): 
	category = Category.objects.all()   
	tags = Tag.objects.all()
	blog = get_object_or_404(Blog, id=4)
	blogs = Blog.objects.all().order_by('published_date').exclude(id=4)[:3]
	return render(request,'index.html', {'blogs' : blogs,'categorise' : category,'tags': tags,'index_blog':blog,})
""" 
class UserCreate(CreateView):
	model = User """

def user_register(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
            # save form in the memory not in database  
			user = form.save(commit=False)
			user.is_active = False 
			user.save()
			 # to get the domain of the current site  
			current_site = get_current_site(request)
			email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
			link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
			email_subject = 'Activate your account'
			activate_url = 'http://127.0.0.1:8000'+link
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [to_email],
                )
			email.send()
			return HttpResponse('Account successfully created. Please confirm your email address to complete the registration')
			#return render(request, 'registration/register.html')
			#login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			#p_form.user_id = request.user.id
			#p_form.save()
			#messages.success(request, "Registration successful." )
			#return redirect("/")
		else:
			messages.error(request, "Oops! something went worng please correct it" )
	context = {
		"register_form":form
		}
	return render (request, "registration/register.html", context)

def activate(request,uidb64,token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid) 
		p_form = Profile()
		p_form.user_id = uid
		p_form.save()

	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save() 
		login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
		messages.success(request, "Thank you for your email confirmation." )
		return redirect("/")  
	else:
		return HttpResponse('Activation link is invalid!')  

@login_required
def user_profile(request, id):

	# fetch the object related to passed id
	obj1 = get_object_or_404(User, id = id)
	obj2 =Profile.objects.filter(user_id = id)
	if not obj2.exists():
		social_user = Profile()
		social_user.user_id = id
		social_user.save()

	obj2 = get_object_or_404(Profile, user_id = id)
		
	# pass the object as instance in form
	r_form = UserUpdateForm(instance = obj1)
	p_form = ProfileForm(instance=obj2)
	old_img = obj2.image
	if request.method == 'POST':
		p_form = ProfileForm(request.POST, request.FILES or None, instance=obj2)
		if r_form.is_valid and p_form.is_valid:
			current_user = request.user
			current_user.first_name =request.POST['first_name']
			current_user.last_name = request.POST['last_name']
			current_user.save()

			p_form.save()
			if old_img.name != 'profile_pictures/default.jpg':
				os.remove(old_img.path)
			messages.success(request, 'Your Profile Update successfully')
		else:
			messages.error(request, "Oops! something went worng please correct it" )
	context = {
		"register_form":r_form,
		"profile_form":p_form
		}
	return render(request, 'registration/profile.html', context)

def blogDetailView(request,slug):
	blog = get_object_or_404(Blog, slug=slug)
	form = CommentPostForm()
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = CommentPostForm(request.POST)
			if form.is_valid:
				comm_inst = Comment()
				comm_inst.title = request.POST['title']
				comm_inst.comment = request.POST['comment']
				comm_inst.commenter = User(request.user.id)
				comm_inst.blog = blog
				comm_inst.save()
		else:
			messages.warning(request, "You need to login. Please login !" )
			return redirect("login")
	blogs = Blog.objects.filter(category = blog.category).exclude(id=blog.id)[:6]
	form = CommentPostForm()
	context = {
		'blog' : blog,
		'form' : form,
		'blog_list' : blogs,
		}
	return render(request, 'blog/blog_detail.html', context)



class BlogListView(generic.ListView):
    model = Blog
    queryset = Blog.objects.filter(status='l')

class AuthorListView(generic.ListView):
    model = Author
    
class AuthorDetailView(generic.DetailView):
    model = Author	

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    blogs = Blog.objects.filter(tags__in=[tag])
    return render(request, 'blog/blog_list.html', {'blog_list':blogs, 'tag':tag})

def category(request, slug):
	category = get_object_or_404(Category, slug=slug)
	blogs = Blog.objects.filter(category__in=[category])
	return render(request, 'blog/blog_list.html', {'blog_list':blogs})