from django.urls import path

from app.goal.views import GoalCreateApiView, GoalDetailApiView, GoalGeneratePlanApiView

urlpatterns = [
    # Authentication
    path('', GoalCreateApiView.as_view(), name='goal-create'),
    path('<int:pk>', GoalDetailApiView.as_view(), name='goal-detail'),

    path('<int:pk>/generate-plan', GoalGeneratePlanApiView.as_view(), name='goal-generate-plan'),

]
