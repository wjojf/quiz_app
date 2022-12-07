from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Quiz, Question, Answer
User = get_user_model()


class Command(BaseCommand):
    TEST_QUIZ = {
        "title": "Test Quiz",
        "QUESTIONS": [
            {
                "prompt": "What is OOP?",
                "ANSWERS": [
                     {
                        "text": "Programming Concept",
                        "correct": True,
                    }, 
                    {
                        "text": "Or Or Poop",
                    }, 
                    {
                        "question_id": 1,
                        "text": "Other",
                    }
                ]
            },
            {
                "prompt": "How do you reverse a list in Python?",
                "ANSWERS": [
                    {
                        "text": "list.Reversed()",
                    }, 
                    {
                        "text": "list[::-1]",
                        "correct":True,
                    }, 
                    {
                        "text": "list.UpSideDown()",
                    }, 
                ],
            }, 
            {
                "prompt": "What is Python?",
                "ANSWERS": [
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
                ],
            },
        ],
    }

    def handle(self, *args, **options):
        try:
            ADMIN_USER = User.objects.get(username="admin")
        except Exception:
            print("Cannot find the Admin user")
            return 
        
        quiz_obj, created = Quiz.objects.get_or_create(
            author = ADMIN_USER,
            title=self.TEST_QUIZ["title"]
        )
        
        if created:
            print(f'[LOG] -> created {quiz_obj}')
            quiz_obj.save()


        for  question_dict in self.TEST_QUIZ["QUESTIONS"]:
            question_obj, created = Question.objects.get_or_create(
                quiz=quiz_obj,
                prompt=question_dict["prompt"]
            )
            
            if created:
                print(f'[LOG] -> created {question_obj}')
                question_obj.save()
            
            for answer_dict in question_dict["ANSWERS"]:
                answer_obj,created = Answer.objects.get_or_create(
                    question=question_obj,
                    **answer_dict
                )
                
                if created:
                    print(f'[LOG] -> created {answer_obj}')
                    answer_obj.save()
        
        