from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    times_taken = models.IntegerField(default=0, editable=False)

    @property
    def question_count(self):
        return self.questions.count()


    def __str__(self):
        return f'Quiz {self.title}'


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        null=True,
        related_name='questions',
        on_delete=models.SET_NULL
    )
    prompt = models.CharField(max_length=255, default='')

    class Meta:
        ordering = ("id", )
    
    def __str__(self):
        return f'{self.prompt}'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255, default="")
    correct = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.text}'


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', 'answer')