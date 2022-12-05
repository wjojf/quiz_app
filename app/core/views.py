from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect

from core.models import Quiz, Question, Answer, UserAnswer
from core.utils import get_last_question


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

    def get(self, request, *args, **kwargs):
        print(self.get_queryset())
        return super().get(request, *args, **kwargs)


class QuizView(DetailView):
    model = Quiz
    pk_url_kwarg = 'quiz_id'
    context_object_name = 'quiz'
    template_name = 'core/quiz_start.html'


##################
# Question Views #
##################

class QuestionView(DetailView):
    model = Question
    template_name: str = 'core/question.html'
    pk_url_kwarg: str = 'quiz_id'
    context_object_name: str = 'question'

    def get_object(self, *args, **kwargs):
        try:
            print(kwargs.get(self.pk_url_kwarg))
            quiz_obj = Quiz.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
            return get_last_question(quiz_obj, self.request.user)
        except Exception:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        if not context[self.context_object_name]:
            context['finished'] = True
            return context
        context['question_answers'] = context['question'].answers.all()
        return context


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
    except Exception as e:
        print(e)
        return redirect('home')


class QuizResultsView(DetailView):
    pass 