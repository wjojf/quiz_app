from django.contrib.auth import get_user_model
from core.models import Quiz, UserAnswer, Question, UserResult
User=get_user_model()


def user_quiz_answers(quiz_id, user):
    return UserAnswer.objects.select_related('answer__question__quiz').filter(
        answer__question__quiz__id=quiz_id,
        user=user,
    )

def calculate_results(*user_answers):
    if not user_answers:
        return 
    
    n_a = len(user_answers)
    c_a = 0

    for u_a in user_answers:
        if u_a.answer.correct:
            c_a += 1
    
    return {
        "correct_answers": c_a,
        "percentage": (c_a / n_a) * 100
    }


def create_user_result(quiz_obj: Quiz, user:User) -> UserResult:
    user_quiz_answers = UserAnswer.objects.select_related('user', 'answer__question').filter(
        user=user,
        answer__question__quiz=quiz_obj
    ).order_by('answer__question__quiz_index')

    if not user_quiz_answers:
        return 
    
    last_answer = user_quiz_answers.last()
    if last_answer.answer.question.quiz_index != \
            last_answer.answer.question.quiz.question_count:
        return 
    
    result_stats = calculate_results(*user_quiz_answers)

    if not result_stats:
        return

    try:
        result_obj = UserResult.objects.create(
            user=user,
            quiz=quiz_obj,
            correct_answers=result_stats['correct_answers'],
                correct_percentage=result_stats['percentage']
        )
        result_obj.save()
        # delete current answers
        for u_a in user_quiz_answers:
            u_a.delete()
        return result_obj
    except Exception as e:
        print(e)
        return    

    
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
    
    last_quiz_index = user_quiz_answers.last().answer.question.quiz_index 
    
    # if quiz was already passed: create result obj, 
    if last_quiz_index == quiz_obj.question_count:
        create_user_result(*user_quiz_answers)
        return quiz_questions.first()

    #return i + 1 where i is quiz_index of last answered 
    try:
        return Question.objects.get(
            quiz=quiz_obj,
            quiz_index=last_quiz_index+1,
        )
    except Exception:
        return  # No more questions


