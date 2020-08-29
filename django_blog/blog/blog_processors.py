from users.models import Profile
from .models import Post

def user(request): #add to setting
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user = request.user)[0]
    else :
        profile = None 
    
    return{'g_profile':profile}

def last_posts(request):
    post = Post.objects.all().order_by('-date_posted')[:5]
    return {'g_last_posts':post}