from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, pre_delete
from core.signals import generate_quiz_index, move_quiz_indexes


class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    @property
    def question_count(self):
        return self.questions.count()

    def __str__(self):
        return f'Quiz {self.title}'

    class Meta:
        verbose_name_plural = 'Quizzes'


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        null=True,
        related_name='questions',
        on_delete=models.SET_NULL
    )
    prompt = models.CharField(max_length=255, default='')
    quiz_index = models.IntegerField(default=1)

    class Meta:
        ordering = ("quiz_index", )
    
    def __str__(self):
        return f'{self.prompt}'
pre_save.connect(
    generate_quiz_index,
    sender=Question,
    dispatch_uid='Question.generate_quiz_index'
)
pre_delete.connect(
    move_quiz_indexes,
    sender=Question,
    dispatch_uid='Question.move_quiz_indexes'
)


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
    
    
    def __str__(self):
        return f'{self.user} {self.answer}'


class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    correct_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.correct_answers} in {self.quiz} by {self.user}'