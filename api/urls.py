# Author: Sakthi Santhosh
# Created on: 09/01/2023
from rest_framework.routers import DefaultRouter

from api.views import (
    InviteeViewSet,
    SubTaskViewSet,
    TagViewSet,
    TaskViewSet,
    TaskGroupViewSet
)


router = DefaultRouter()

router.register(r"invitees", InviteeViewSet, basename="invitee")
router.register(r"sub-tasks", SubTaskViewSet, basename="sub-task")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"task-groups", TaskGroupViewSet, basename="task-group")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = router.urls
