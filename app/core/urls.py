from django.urls import path
from core import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.MyLoginView.as_view(), name='signup'), # FIXME: 
    path('logout/', views.logout_user, name='logout'),
    path('quiz/<int:quiz_id>', views.QuizView.as_view(), name='quiz-view'),
    path('quiz/<int:quiz_id>/question/', views.QuestionView.as_view(), name='question-view'),
    path('save-answer/', views.save_answer_view, name='save-answer'),
    path('quiz/<int:quiz_id>/results', views.QuizResultsView.as_view(), name='quiz-results'),
    
]