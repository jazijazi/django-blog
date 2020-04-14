from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import ListView , DetailView ,CreateView , UpdateView , DeleteView
from django.contrib.auth.models import User
from .models import Post
from users.models import Profile

from .forms import PostView

# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request , 'blog/home.html' , context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

def like_post(request):
    user = request.user
    if request.method=='POST' and request.is_ajax() :
        post = Post.objects.get(id = request.POST.get('pk'))
        if(post.author == user):
            return JsonResponse({'like':'False'})
        if (not post.user_like.filter(id=user.id).exists()) : #if not in likers add it
            post.user_like.add(user)
            return JsonResponse({'liked':'True'})
        elif(post.user_like.filter(id=user.id).exists()) : #if in likers remove it
            post.user_like.remove(user)
            return JsonResponse({'disliked':'True'})

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)

        user = get_object_or_404(User , username=self.kwargs.get('username'))
        profile = Profile.objects.filter(user = user)[0]
        
        context['profile'] = profile
        return context
    
    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')    
        

class PostDetailView(DetailView):
    model = Post
    #for default templates => <app>/<model>_<ViewType>
    #for default context name => object

class PostCreateView(LoginRequiredMixin , CreateView):
    model = Post
    #fields = ['title','content','image']
    #default template is <model>_form because is shared with updateView
    form_class = PostView
    #for set author field with current login user
    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model = Post
    fields = ['title','content','image']
    #default template is <model>_form because is shared with createView
    
    #for set author field with current login user
    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #for check current user == auther of this post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin , DeleteView):
    model = Post
    success_url = '/'
    
    #for check current user == auther of this post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
   return render(request , 'blog/about.html' , {'title':'about'}) 
