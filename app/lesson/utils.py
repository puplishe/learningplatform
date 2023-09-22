from django.http import JsonResponse, Http404
from users.models import UserProfle
from .models import LessonView
def calculate_and_record_lesson_view(user, lesson, start_time, end_time):
    # Check if the user has purchased the product associated with the lesson
    user_profile = UserProfle.objects.get(user=user)
    has_purchased = user_profile.product_access.filter(pk=lesson.product_id).exists()

    if not has_purchased:
        return JsonResponse({"message": "You have not purchased this product."}, status=403)

    # Calculate view status
    lesson_duration = lesson.duration_seconds

    if lesson_duration > 0 and start_time is not None and end_time is not None:
        viewed_duration = (end_time - start_time).total_seconds()
        percentage_viewed = (viewed_duration / lesson_duration) * 100

        if percentage_viewed >= 80:
            status = True
        else:
            status = False
    else:
        # Handle the case where lesson_duration is zero or negative
        status = False

    # Create a LessonView object and set the calculated status
    lesson_view = LessonView(user=user, lesson=lesson, start_time=start_time, end_time=end_time, status=status)
    lesson_view.save()

    return JsonResponse({"message": "Lesson view recorded."})