from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        user_projects = self.queryset.filter(owner=request.user)
        total_tasks = Task.objects.filter(project__owner=request.user).count()
        completed_tasks = Task.objects.filter(
            project__owner=request.user, status='done'
        ).count()
        overdue_tasks = Task.objects.filter(
            project__owner=request.user, due_date__lt=now()
        ).count()

        return Response({
            "total_projects": user_projects.count(),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": f"{(completed_tasks / total_tasks) * 100:.2f}%" if total_tasks else "N/A",
            "overdue_tasks": overdue_tasks,
        })
    
    def get_queryset(self):
        # Restrict projects to the ones owned by the current user
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict tasks to projects owned by the current user
        return self.queryset.filter(project__owner=self.request.user)
