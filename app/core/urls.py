from django.urls import path
from core import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('quiz/<int:quiz_id>', views.QuizStartView.as_view(), name='quiz-view'),
]