from django.views.generic import ListView, DetailView
from core.models import Quiz, Question, Answer, UserAnswer
from core.utils import quiz_is_started


class HomeView(ListView):
    model = Quiz
    context_object_name = 'quizzes'
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        print(self.get_queryset())
        return super().get(request, *args, **kwargs)


class QuizStartView(DetailView):
    model = Quiz
    pk_url_kwarg = 'quiz_id'
    context_object_name = 'quiz'
    template_name = 'core/quiz_start.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['quiz_is_started'] = quiz_is_started(
            quiz_obj=self.get_object(),
            user=self.request.user
        )

        return context