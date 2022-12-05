from django.contrib.auth import get_user_model
from datetime import datetime as dt
from datetime import timedelta as td 
from core.models import Quiz, UserAnswer, Question
User=get_user_model()


def get_last_question(quiz_obj: Quiz, user:User) -> Question:
    
    quiz_questions = Question.objects.select_related('quiz').filter(quiz=quiz_obj)
    if not quiz_questions:
        return 

    user_quiz_answers = UserAnswer.objects.select_related('user', 'answer__question').filter(
        user=user,
        answer__question__quiz=quiz_obj
    ).order_by('answer__question__quiz_index')

    # If there are no previous answers 
    if not user_quiz_answers:
        return quiz_questions.first()# return the first one, as question are ordered 
    
    last_quiz_index = user_quiz_answers.last().answer.question.quiz_index # TODO:
    
    # if quiz was already passed: restart
    if last_quiz_index == quiz_obj.question_count:
        return quiz_questions.first()

    #return i + 1 where i is quiz_index of last answered 
    try:
        return Question.objects.get(
            quiz=quiz_obj,
            quiz_index=last_quiz_index+1,
        )
    except Exception:
        return  # No more questions

    
def calculate_results(*user_answers):
    if not user_answers:
        return 
    
    n_a = len(user_answers)
    c_a = 0

    for u_a in user_answers:
        if u_a.answer.correct:
            c_a += 1
    
    return {
        "n_questions": n_a,
        "correct_answers": c_a,
        "percentage": (c_a / n_a) * 100
    }
