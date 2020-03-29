from django.shortcuts import get_object_or_404, reverse, redirect, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import CreateBlogForm, EditBlogForm, DeleteConfirmationForm
from .models import Blog_view

def index(request):
    blogs = Blog_view.objects.all().order_by('-pub_date')
    return render(request, 'blog/index.html', {'blogs' : blogs})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log in the user too !
            return redirect("blog:login")
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form' : form})

def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return HttpResponseRedirect(reverse('blog:profile', args=(user.id,)))
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form' : form})

@login_required(login_url='/blog/login/')
def profile(request, user_id):
    if(user_id == request.user.id):
        user = get_object_or_404(User, pk=user_id)
        blogs = user.blog_view_set.all().order_by('-pub_date')
        return render(request, 'blog/profile.html', {"user" : user, 'blogs' : blogs})
    else:
        return HttpResponse("Bad Request")

@login_required(login_url='/blog/login/')
def personalblog(request, user_id, blog_id):
    if(user_id == request.user.id):
        user = get_object_or_404(User, pk=user_id)
        blog = get_object_or_404(Blog_view, pk=blog_id)
        return render(request, 'blog/blogwitheditoption.html', {'user' : user, 'blog' : blog})
    else:
        return HttpResponse("Bad Request")

@login_required(login_url='/blog/login/')
def createblog(request, user_id):
    if(user_id == request.user.id):
        user = get_object_or_404(User, pk=user_id)
        if(request.method == 'POST'):
            form = CreateBlogForm(request.POST)
            if(form.is_valid()):
                blogTitle = form.cleaned_data['blogTitle']
                blogContent = form.cleaned_data['blogContent']
                blogAuthor = user
                blogPub_date = timezone.now()
                newblog = Blog_view(blog_title = blogTitle, pub_date = blogPub_date, author = blogAuthor, textcontent = blogContent)
                newblog.save()
                return HttpResponseRedirect(reverse('blog:profile', args=(user.id,)))
        else:
            form = CreateBlogForm()

        return render(request, 'blog/createblog.html', {'user' : user, 'form' : form})
    else:
        return HttpResponse("Bad Request")

@login_required(login_url='/blog/login/')
def editblog(request, user_id, blog_id):
    if(user_id == request.user.id):
        user = get_object_or_404(User, pk=user_id)
        oldblog = get_object_or_404(Blog_view, pk=blog_id)
        predata = {'blogTitle' : oldblog.blog_title, 'blogContent' : oldblog.textcontent,}
        if(request.method == 'POST'):
            form = EditBlogForm(request.POST, initial = predata)
            if(form.is_valid()):
                blogTitle = form.cleaned_data['blogTitle']
                blogContent = form.cleaned_data['blogContent']
                blogEditDate = timezone.now()
                oldblog.blog_title = blogTitle
                oldblog.pub_date = blogEditDate
                oldblog.textcontent = blogContent
                oldblog.save()
                return HttpResponseRedirect(reverse('blog:personalblog', args=(user.id,oldblog.id,)))
        else:
            form = EditBlogForm(initial=predata)

        return render(request, 'blog/editblog.html', {'user' : user, 'form' : form, 'oldblog' : oldblog})
    else:
        return HttpResponse("Bad Request")

@login_required(login_url='/blog/login/')
def deleteblog(request, user_id, blog_id):
    if(user_id == request.user.id):
        user = get_object_or_404(User, pk=user_id)
        blog = get_object_or_404(Blog_view, pk=blog_id)
        if(request.method == 'POST'):
            form = DeleteConfirmationForm(request.POST)
            if(form.is_valid()):
                try:
                    decision = request.POST['Choose']
                except(KeyError, decision.DoesNotExist):
                    return render(request, 'blog/deleteblog.html', {'user' : user, 'form' : form, 'blog': blog, 'error_message': "You didn't select a choice.",})
                else:
                    if(decision == '1'):
                        blog.delete()
                        return HttpResponseRedirect(reverse('blog:profile', args=(user.id,)))
                    else:
                        return HttpResponseRedirect(reverse('blog:personalblog', args=(user.id, blog.id,)))
        else:
            form = DeleteConfirmationForm()
        return render(request, 'blog/deleteblog.html', {'user' : user, 'form' : form, 'blog' : blog})
    else:
        return HttpResponse("Bad Request")

def getblog(request, blog_id):
    blog = get_object_or_404(Blog_view, pk=blog_id)
    return render(request, 'blog/blogs.html', {'blog' : blog})

def allblogs(request):
    blogs = Blog_view.objects.all().order_by('-pub_date')
    return render(request, 'blog/allblogs.html', {'blogs' : blogs})

@login_required(login_url='/blog/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

@login_required(login_url='/blog/login/')
def home(request):
    return HttpResponseRedirect(reverse('blog:profile', args=(request.user.id,)))
