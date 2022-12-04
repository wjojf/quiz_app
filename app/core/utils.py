from core.models import Quiz, UserAnswer, Question
from django.contrib.auth import get_user_model
from datetime import datetime as dt
from datetime import timedelta as td 
User=get_user_model()


def quiz_is_started(quiz_obj: Quiz, user: User) -> bool:
    _24_hours_ago = dt.now() - td(hours=24)
    # reset if last answer was more than 24 hours ago

    user_quiz_answers = UserAnswer.objects.select_related('user', 'answer__question').filter(
        user=user,
        answer__question__quiz=quiz_obj
    )

    if not user_quiz_answers:
        return False
    
    last_quiz_answer = user_quiz_answers.first()
    last_quiz_answer_time = last_quiz_answer.created_at
    
    return last_quiz_answer_time >= _24_hours_ago


def get_last_question(quiz_obj: Quiz, user:User) -> Question:
    user_quiz_answers = UserAnswer.objects.select_related('user', 'answer__question').filter(
        user=user,
        answer__question__quiz=quiz_obj
    )

    # If there are no previous answers 
    if not user_quiz_answers:
        return Question.objects.select_related('quiz').filter(
            quiz=quiz_obj
        ).first()
