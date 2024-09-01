# Author: Sakthi Santhosh
# Created on: 17/01/2024
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["HEAD", "OPTIONS"]:
            return True

        return obj.task_group.owner == request.user
