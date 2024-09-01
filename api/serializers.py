# Author: Sakthi Santhosh
# Created on: 09/01/2023
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField
)

from api.models import Invitee, SubTask, Tag, Task, TaskGroup


# Model: Invitee
class InviteeSerializer(ModelSerializer):
    class Meta:
        model = Invitee
        fields = "__all__"


# Model: Tag
class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data):
        tag_instance, created = Tag.objects.get_or_create(
            name=validated_data.get("name", None)
        )

        if not created:
            print(
                f"Warning: A tag named \"{validated_data['name']}\" already "
                "exists, skipped its creation."
            )
        return tag_instance


# Model: SubTask
class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"


class SubTaskListSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = ["title"]


# Model: Task
class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskListSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title"]


class TaskRetrieveSerializer(ModelSerializer):
    sub_tasks = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


# Model: TaskGroup
class TaskGroupSerializer(ModelSerializer):
    class Meta:
        model = TaskGroup
        exclude = ["owner"]


class TaskGroupRetrieveSerializer(ModelSerializer):
    tasks = TaskListSerializer(many=True)

    class Meta:
        model = TaskGroup
        exclude = ["owner"]
