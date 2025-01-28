from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now


from django.contrib.auth.models import User
from .models import Project, Task


from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
import re


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



class AllUsersView(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset

    def validate_password(self, password):
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one number."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return "Password must contain at least one special character."
        return None
    
    def create(self, request, *args, **kwargs):
        
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate mandatory fields
        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password
        password_error = self.validate_password(password)
        if password_error:
            return Response({"error": password_error}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Hash the password
            user.set_password(password)
            user.save()

            # Response with created user details
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)