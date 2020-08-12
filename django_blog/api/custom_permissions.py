from rest_framework import permissions
from rest_framework.permissions import  SAFE_METHODS
class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Check User is Author of a Post for edit-delete or can readOnly
    """
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        
        if request.user == obj.author or request.method in self.SAFE_METHODS:
            return True
        else:
            return False

class IsSelfUserOrAdminOrReadOnlyPermission(permissions.BasePermission):

    #If user is authenticated cant post (create other user) *except staff user*
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'POST' and not request.user.is_staff:
            return False
        else:
            return True

    #Check *requsted user*  is  *self user*  or  *staff user*  for edit user data or can read only
    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_staff or request.method in SAFE_METHODS:
            return True
        else:
            return False