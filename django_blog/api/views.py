from rest_framework import viewsets , permissions
from .custom_permissions import IsAuthorOrReadOnlyPermission , IsSelfUserOrAdminOrReadOnlyPermission
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import PostSerializer , UserSerializer , ProfileSerializer , ChangePasswordSerializer
from blog.models import Post
from django.contrib.auth.models import User
from rest_framework import generics

import django.contrib.auth.password_validation as pass_validation
from django.core import exceptions

from rest_framework.decorators import api_view , permission_classes
# Create your views here.  
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAuthorOrReadOnlyPermission]

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfUserOrAdminOrReadOnlyPermission]
    '''
    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(),)
        elif self.request.method == 'POST':
            return (permissions.IsAuthenticated(),)
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return (IsSelfUserOrAdminPermission(),)
        return (permissions.IsAdminUser(),)
    '''

    '''
    #The PUT method replaces all current representations of the target resource with the request payload.
    def update(self, request, pk=None , *args, **kwargs):
        print("************updateupdateupdateupdateupdateupdateupdateupdateupdate*************")

    #The PATCH method is used to apply partial modifications to a resource.
    def partial_update(self, request, pk=None , *args, **kwargs):
        print("***********8partial_updatepartial_updatepartial_updatepartial_update***************")
    '''
#An view for changing password.
class ChangePasswordView(generics.UpdateAPIView):
        
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user #give current requested user to object
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object() #get user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            #Check new_password valid
            try:
                pass_validation.validate_password(password=serializer.data.get("new_password"), user=self.object)
            except exceptions.ValidationError as e:
                response = {
                'status': 'failed',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': e.messages,
                'data': []
                }
                return Response(response)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        #if serializer not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) #POST  AFTER ADD Authenticated
@permission_classes([permissions.IsAuthenticated])
def like_post_api(request , post_id):
    post = get_object_or_404(Post.objects.all(), pk=post_id)
    user = request.user
    if(post.author == user):
        return Response({'like':'False'}, status=status.HTTP_400_BAD_REQUEST)
    if (not post.user_like.filter(id=user.id).exists()) : #if not in likers add it
        post.user_like.add(user)
        return Response({'like':'True' , 'liked':'True'}, status=status.HTTP_200_OK)
    elif(post.user_like.filter(id=user.id).exists()) : #if in likers remove it
        post.user_like.remove(user)
        return Response({'like':'True' , 'disliked':'True'}, status=status.HTTP_200_OK)