from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image as PilImage
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    #content = models.TextField()
    #content = RichTextField()
    content = RichTextUploadingField()
    #image = models.ImageField(null=True , blank=True , upload_to='post_images') #add ckeditor so we need this anymore
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User ,related_name='author', on_delete=models.CASCADE)
    user_like=models.ManyToManyField(User,related_name="likes",blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    #add ckeditor so we need this anymore
    """ 
    def save(self, *args, **kwargs):
        super().save(*args , **kwargs)

        if self.image : #beecause image maybe null
            img = PilImage.open(self.image.path)
        
            if img.height > 500 or img.width > 700 :
                output_size = (700,500)
                img.thumbnail(output_size)
                img.save(self.image.path)
    """
    
class Comment(models.Model):
    writer = models.ForeignKey(User , on_delete=models.CASCADE , related_name='commentor')
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='comments')
    body = models.TextField(max_length=200, help_text="Add your comment")
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE , null=True, blank=True, related_name='replies')
    comment_like=models.ManyToManyField(User,related_name="user_comment_likes",blank=True)
    comment_dislike=models.ManyToManyField(User,related_name="user_comment_dislikes",blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.writer.username)