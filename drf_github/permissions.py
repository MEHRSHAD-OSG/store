from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "permission denied, you're not the owner"

    def has_permission(self, request, view):
        # for before login
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        # after login
        # obj => questions
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
