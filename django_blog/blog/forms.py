from django import forms
from .models import Post

class PostView(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','image']

        widgets = {'image': forms.FileInput(attrs={'id': 'postimageform'}) }
