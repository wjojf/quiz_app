def generate_quiz_index(sender, instance, *args, **kwargs):

    # if we modify current value 
    # in case of deleting previous question - do nothing
    if instance.quiz_index > 1:
        return 

    instance_quiz = instance.quiz
    quiz_indexes = sender.objects.filter(
        quiz=instance_quiz
    ).order_by('quiz_index').values_list('quiz_index')

    if not quiz_indexes:
        return # default value will be set
    
    max_index = quiz_indexes.last()[0]
    instance.quiz_index = max_index + 1


def move_quiz_indexes(sender, instance, *args, **kwargs):
    curr_quiz_index = instance.quiz_index
    next_questions = sender.objects.filter(
        quiz=instance.quiz,
        quiz_index__gt=curr_quiz_index
    ).order_by('quiz_index')

    for next_question in next_questions:
        next_question.quiz_index -= 1 # i + 1 becomes i 
        next_question.save()

