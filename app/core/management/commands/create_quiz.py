from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Quiz, Question, Answer
User = get_user_model()


class Command(BaseCommand):
    QUIZ = {
        "title": "Test Quiz",
    }
    
    QUESTIONS = [
        {
            "quiz_id": 1,
            "prompt": "What is OOP?"
        },
        {   "quiz_id": 1,
            "prompt": "How do you reverse a list in Python?",
        }, 
        {
            "quiz_id": 1,
            "prompt": "What is Python?",
        },
    ]
    
    ANSWERS = [
        {
            "question_id": 1,
            "text": "Programming Concept",
            "correct": True,
        }, 
        {
            "question_id": 1,
            "text": "Or Or Poop",
        }, 
        {
            "question_id": 1,
            "text": "Other",
        }, 
        {
            "question_id": 2,
            "text": "list.Reversed()",
        }, 
        {
            "question_id": 2,
            "text": "list[::-1]",
            "correct":True,
        }, 
        {
            "question_id": 2,
            "text": "list.UpSideDown()",
        }, 
        {
            "question_id": 3,
            "text": "A turtle",
        },
        {
            "question_id": 3,
            "text": "A Programming Language",
            "correct": True,
        },
        {
            "question_id": 3,
            "text": "Something awful",
        },
    ]

    def handle(self, *args, **options):
        try:
            ADMIN_USER = User.objects.get(username="admin")
        except Exception:
            print("Cannot find the Admin user")
            return 
        
        quiz_obj, created = Quiz.objects.get_or_create(
            author=ADMIN_USER,
            **self.QUIZ
        )
        quiz_obj.save()
        
        print(f'[LOG] Created {quiz_obj}')

        quiz_questions = [q_d for q_d in self.QUESTIONS if q_d["quiz_id"]==quiz_obj.id]
        for quiz_question in quiz_questions:
            question_obj, created = Question.objects.get_or_create(
                quiz=quiz_obj,
                **{k:v for k,v in quiz_question.items() if k != "quiz_id"}
            )
            question_obj.save()
            
            print(f'[LOG] Created {question_obj}')

            questions_answers = [q_a for q_a in self.ANSWERS if q_a["question_id"]==question_obj.id]
            for question_answer in questions_answers:
                ans_obj, created = Answer.objects.get_or_create(
                    question=question_obj,
                    **{k:v for k,v in question_answer.items() if k != "question_id"}
                )
                print(f'[LOG] Created {ans_obj}')

        