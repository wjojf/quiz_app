from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

from core.models import Quiz, Question, Answer, UserAnswer, UserResult
from core.utils import get_last_question, create_user_result, user_quiz_answers


#################
# AUTHENTICATION #
#################

class MyLoginView(LoginView):
    template_name: str = 'login.html'


def logout_user(request):
    logout(request)
    return redirect('home')

###############
# Quiz Views #
###############

class HomeView(ListView):
    model = Quiz
    context_object_name = 'quizzes'
    template_name = 'core/index.html'


class QuizView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Quiz
    pk_url_kwarg = 'quiz_id'
    context_object_name = 'quiz'
    template_name = 'core/quiz_start.html'


##################
# Question Views #
##################

class QuestionView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Question
    template_name: str = 'core/question.html'
    pk_url_kwarg: str = 'quiz_id'
    context_object_name: str = 'question'

    def get_object(self, *args, **kwargs):
        try:
            print(self.kwargs.get(self.pk_url_kwarg))
            quiz_obj = Quiz.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
            return get_last_question(quiz_obj, self.request.user)
        except Exception:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        if not context[self.context_object_name]:
            context['quiz_id'] = self.kwargs.get(self.pk_url_kwarg)
            context['finished'] = True
            return context
        context['question_answers'] = context['question'].answers.all()
        return context


@login_required(login_url='login')
def save_answer_view(request):
    if request.method != "POST":
        return redirect('home')
    
    if 'user_answer' not in request.POST:
        return redirect('home')
    
    try:
        answer_obj = Answer.objects.select_related('question__quiz').get(id=int(request.POST['user_answer']))
        user_ans_obj = UserAnswer.objects.create(
            user=request.user,
            answer=answer_obj
        )
        user_ans_obj.save()
        return redirect('question-view', quiz_id=answer_obj.question.quiz.id)
    
    except Exception:
        return redirect('home')


class QuizResultsView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = UserResult
    pk_url_kwarg: str = 'quiz_id'
    template_name = 'core/quiz_results.html'
    context_object_name = 'results'


    def get_queryset(self, *args, **kwargs):
        if self.pk_url_kwarg not in self.kwargs:
            return  
        try:
            quiz_obj = Quiz.objects.get(id=self.kwargs[self.pk_url_kwarg])
            return UserResult.objects.filter(user=self.request.user, quiz=quiz_obj)
        except Exception:
            return 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['quiz_obj'] = None
        try:
            context['quiz_obj'] = Quiz.objects.get(id=self.kwargs[self.pk_url_kwarg])
        except Exception:
            pass
        return context


    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        quiz_obj = self.get_context_data()['quiz_obj']
        create_user_result(quiz_obj, request.user)
        return super().get(request, *args, **kwargs)
