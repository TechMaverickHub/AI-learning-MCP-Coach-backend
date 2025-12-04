from django.urls import path

from app.goal.views import GoalCreateApiView, GoalDetailApiView

urlpatterns = [
    # Authentication
    path('', GoalCreateApiView.as_view(), name='goal-create'),
    path('<int:pk>', GoalDetailApiView.as_view(), name='goal-detail'),

]
