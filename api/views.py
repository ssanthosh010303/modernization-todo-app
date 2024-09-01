# Author: Sakthi Santhosh
# Created on: 09/01/2024
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import Invitee, SubTask, Tag, Task, TaskGroup
from api.paginations import StandardResultsSetPagination
from api.permissions import IsOwner
from api.serializers import (
    InviteeSerializer,
    SubTaskSerializer,
    TagSerializer,
    TaskRetrieveSerializer,
    TaskSerializer,
    TaskGroupRetrieveSerializer,
    TaskGroupSerializer
)


class InviteeViewSet(ModelViewSet):
    queryset = Invitee.objects.all()
    serializer_class = InviteeSerializer
    filter_backends = [SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ["first_name", "last_name", "=email"]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ["=name"]


class SubTaskViewSet(ModelViewSet):
    queryset = SubTask.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = SubTaskSerializer

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            method="GET",
            detail="Listing is not allowed for this resource.",
            code="action_prohibited"
        )


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaskRetrieveSerializer
        else:
            return TaskSerializer

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            method="GET",
            detail="Listing is not allowed for this resource.",
            code="action_prohibited"
        )


class TaskGroupViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ["name", "owner__first_name", "owner__last_name", "=owner__email"]

    def get_queryset(self):
        return TaskGroup.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaskGroupRetrieveSerializer
        else:
            return TaskGroupSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
