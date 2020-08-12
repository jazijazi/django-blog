from rest_framework import serializers
from blog.models import Post
from users.models import Profile
from django.contrib.auth.models import User
import datetime
from django.db import transaction


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'user':{"read_only":True , "required":True}} 

class UserSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(source='profile.image')
    #bio = serializers.CharField(source='profile.bio') 
    #location = serializers.CharField(source='profile.location')
    #birthday = serializers.DateField(source='profile.birthday')

    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ("id","username","password","first_name","last_name","email",
                                                                        "is_superuser",
                                                                        "is_staff",
                                                                        "is_active",
                                                                        "profile",
                                                                        #"image",
                                                                        #"bio" ,
                                                                        #"location",
                                                                        #"birthday" ,
                                                                        )
        #fields = '__all__'
        extra_kwargs = {'password':{"write_only":True , "required":True},
                        'is_superuser':{"read_only":True , "required":False},
                        'is_staff':{"read_only":True , "required":False},
                        'is_active':{"read_only":True , "required":False},
                        }

    @transaction.atomic
    def create(self , validated_data):
        profile_data = validated_data.pop('profile') #get profile datas
        user = User.objects.create_user(**validated_data) #create user
        #user.profile.objects.update(**profile_data) 
        

        if not profile_data['image']:  #if image profile is empty replace none with default image
            profile_data['image'] = "default.jpg"
            

        #because we use signals profile created when user create Now we just set profile data to this profile
        for attr, value in profile_data.items():
            setattr(user.profile, attr, value)
            user.profile.save()

        user.save()

        return user

    def update(self, instance, validated_data):
        #pop password field So Nobody can change password in put or patch method
        if validated_data.get('password'):
            password = validated_data.pop('password')

        if validated_data.get('profile'):
            profile_data = validated_data.pop('profile') #get profile data
            profile = instance.profile

            if not profile_data['image']: #if image profile is empty replace none with default image
                profile_data['image'] = "default.jpg"

            for attr, value in profile_data.items(): #update profile
                setattr(profile, attr, value)
                profile.save()




        '''
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        '''

        

        return super(UserSerializer, self).update(instance, validated_data) #update user
        
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ProfileUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'date_posted':{"read_only":True , "required":True} , 
                        'user_like':{"read_only":True , "required":False}}

    def create(self, validated_data):
        #user_like = validated_data.pop('user_like')
        post = Post.objects.create(author = self.context['request'].user ,
                                date_posted=datetime.datetime.now() ,
                                **validated_data
                                )
        #for user in user_like :
        #    post.user_like.add(user)
        post.save()
        return post