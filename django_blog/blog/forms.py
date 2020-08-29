from django import forms
from .models import Post , Comment 

class PostView(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']

        #widgets = {'image': forms.FileInput(attrs={'id': 'postimageform'}) }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body' ,]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3, })
        #pass