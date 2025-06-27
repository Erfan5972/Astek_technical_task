from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from astek_technical_task.api.serializers import PaginationParamsSerializer
from astek_technical_task.scheduler.constants import PREDEFINED_TASKS_TAG
from astek_technical_task.scheduler.serializers import PredefinedTaskSerializer, ListSerializerPredefinedTask
from astek_technical_task.scheduler.selectors import get_all_predefined_tasks
from astek_technical_task.scheduler.services import create_predefined_task
from astek_technical_task.scheduler.types import PredefinedTaskInterface
from astek_technical_task.api.pagination import get_paginated_response, LimitOffsetPagination


class PredefinedTaskListCreateAPI(APIView):
    """
    API View to list all predefined tasks and allow admins to create new ones.
    """
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: ListSerializerPredefinedTask()},
        parameters=[PaginationParamsSerializer],
        tags=PREDEFINED_TASKS_TAG,
        summary="List Predefined Tasks",
        description="Returns a list of all predefined tasks. Admin only.",
    )
    def get(self, request):
        """
        GET: List all predefined tasks (admin only).
        """
        tasks = get_all_predefined_tasks()
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            request=request,
            serializer_class=PredefinedTaskSerializer,
            queryset=tasks,
            view=self
        )

    @extend_schema(
        request=PredefinedTaskSerializer,
        responses={201: PredefinedTaskSerializer},
        tags=PREDEFINED_TASKS_TAG,
        summary="Create Predefined Task",
        description="Creates a new predefined task. Admin only.",
    )
    def post(self, request):
        """
        POST: Create a new predefined task (admin only).
        """
        serializer = PredefinedTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            interface = PredefinedTaskInterface(**serializer.data)
            task = create_predefined_task(interface)
            serializer = PredefinedTaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': f'servcer error: {e}'})