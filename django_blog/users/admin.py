from django.contrib import admin
from .models import Profile
from django.utils.html import format_html
# Register your models here.

#admin.site.register(Profile)
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user','email','image_tag')
    def image_tag(self , obj):
        return format_html("<img width=50 height=50 src='{}' >".format(obj.image.url))
    image_tag.short_description = "profile image"
    def email(self , obj):
        return format_html("<p style=color:darkblue;>{}<p>".format(obj.user.email))
        return 