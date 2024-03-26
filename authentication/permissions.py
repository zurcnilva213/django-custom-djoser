from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from .models import User


class CashOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.cash > 0:
            return True
        else:
            raise PermissionDenied("You don't have enough cash to perform this action.")


class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == User.ADMIN or obj.pk == user.pk


class AdminOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.role == User.ADMIN


class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.role == User.ADMIN
