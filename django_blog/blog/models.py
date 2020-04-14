from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image as PilImage
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True , blank=True , upload_to='post_images')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    user_like=models.ManyToManyField(User,related_name="likes",blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args , **kwargs)

        img = PilImage.open(self.image.path)
        
        if img.height > 500 or img.width > 700 :
            output_size = (700,500)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    
