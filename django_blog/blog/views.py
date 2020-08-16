from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import ListView , DetailView ,CreateView , UpdateView , DeleteView
from django.contrib.auth.models import User
from .models import Post
from users.models import Profile
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

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
    paginate_by = 1
    
    def get(self, request, *args, **kwargs):
        if request.GET.get("q"):
            search_word =  request.GET.get("q")
            self.queryset = Post.objects.filter(Q(title__icontains = search_word) |
                        Q(content__icontains = search_word) ).distinct()

        return super(PostListView, self).get(request, *args, **kwargs)

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
        create_post_email(self.request.user , form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)

#send a email when user create a new post
def create_post_email(user , title):
    if user.email :
        subject = 'You Create a POST !'
        from_email ='mydjangoapp@gmail.com'
        to = user.email
        context = {'user': user.email,'post_name': title}
        html_content = render_to_string('blog/create_post_email.html', context)
        plain_message = strip_tags(html_content)
        try:
            send_mail(subject , plain_message , from_email , [to] , fail_silently=False , html_message=html_content)
        except Exception as e:
            print("\n****Error in sending email for create a post****\n")
            print(e)
            print("\n****Error in sending email for create a post****\n")

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model = Post
    fields = ['title','content']
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
