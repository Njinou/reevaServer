from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet,AllUsersView, UsersByProjectView

"""

    path('projects/<int:project_id>/users/', UsersByProjectView.as_view(), name='users_by_project'),
"""
router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('tasks', TaskViewSet, basename='task')
router.register('users', AllUsersView, basename='users')

urlpatterns = router.urls
