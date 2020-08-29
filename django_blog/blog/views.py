from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import ListView , DetailView ,CreateView , UpdateView , DeleteView
from django.contrib.auth.models import User
from .models import Post , Comment
from users.models import Profile
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


from .forms import PostView , CommentForm

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
    
    def get(self, request, *args, **kwargs):
        #for search
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
    comment_form_class = CommentForm

    '''def get(self, request , *args, **kwargs):
        return super(PostDetailView, self).get(request, *args, **kwargs)'''

    def post(self, request, *args, **kwargs):

        #this is for comment on post
        if 'submit_comment' in request.POST:
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.writer = self.request.user
                comment.post = self.get_object()
                comment.save()
        
        #this is for reply a comment
        if 'submit_reply' in request.POST:
            parent = Comment.objects.get(pk=self.request.POST.get('parent_id'))
            comment_form = self.comment_form_class(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.writer = self.request.user
                comment.post = self.get_object()
                comment.parent = parent #!
                comment.save()
        
        return super(PostDetailView, self).get(request, *args, **kwargs)

    '''def form_valid(self, form):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        comment_form = form.save(commit=False)
        comment_form.writer = self.request.user
        comment_form.post = self.self.get_object()
        comment_form.save()
        return super(PostDetailView, self).form_valid(form)'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form_class
        return context

#for like or dislike a commnet
def like_dislike_comments(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method=='POST':
            comment = Comment.objects.get(id = request.POST.get('pk'))
            if request.POST.get('like'): #delete from dislike and add to likes
                if comment.comment_dislike.filter(id=user.id).exists():
                    comment.comment_dislike.remove(user)
                if not comment.comment_like.filter(id=user.id):
                    comment.comment_like.add(user)
                    return JsonResponse({'status':'liked' , 'liked':comment.comment_like.count() , 'disliked':comment.comment_dislike.count()})
                else: #if user liked Alredy and requset for like again so unlike it
                    comment.comment_like.remove(user)
                    return JsonResponse({'status':'unliked' , 'liked':comment.comment_like.count() , 'disliked':comment.comment_dislike.count()})

            elif request.POST.get('dislike'): #delete from like and add to dislikes
                if comment.comment_like.filter(id=user.id).exists():
                    comment.comment_like.remove(user)
                if not comment.comment_dislike.filter(id=user.id):
                    comment.comment_dislike.add(user)
                    return JsonResponse({'status':'disliked' , 'liked':comment.comment_like.count() , 'disliked':comment.comment_dislike.count()})
                else: #if user disliked Alredy and requset for dislike again so undislike it.
                    comment.comment_dislike.remove(user)
                    return JsonResponse({'status':'undisliked' , 'liked':comment.comment_like.count() , 'disliked':comment.comment_dislike.count()})
                
            #return like number and dislike number with JSON    
            return JsonResponse({'status':'error' , 'liked':comment.comment_like.count() , 'disliked':comment.comment_dislike.count()})
    else: #if user not authenticated
        return JsonResponse({'status':'error' , 'liked':'not login' , 'disliked':'not login'})

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
