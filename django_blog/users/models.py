from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(null=True , blank = True ,default='default.jpg', upload_to='progile_pics')
    bio = models.TextField(null=True , blank = True , max_length=500)
    location = models.CharField(null=True , blank = True , max_length=100)
    birthday = models.DateField(null=True , blank = True , auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args , **kwargs)

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
