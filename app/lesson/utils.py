from django.http import JsonResponse, Http404
from users.models import UserProfle
from .models import LessonView


def view_count_time(lesson, lesson_view: LessonView):
    if lesson_view:
        lesson_duration_seconds = lesson.duration_seconds
        if lesson_duration_seconds:
            if lesson_view.start_time is not None and lesson_view.end_time is not None:
                viewing_time_seconds = (lesson_view.end_time - lesson_view.start_time).total_seconds()
                if viewing_time_seconds >= 0.8 * lesson_duration_seconds:
                    status = 'Completed'
                elif lesson_view.time_watched is not None:
                    lesson_view.time_watched += viewing_time_seconds
                else:
                    status = 'Not Completed'
                    lesson_view.time_watched = viewing_time_seconds
            else:
                status = 'Not Completed'
        else:
            status = 'Not Completed'
        viewing_time = int(viewing_time_seconds) if 'viewing_time_seconds' in locals() else 0
    else:
        status = 'Not Completed'
        viewing_time = 0
    data = {
        'status': status,
        'viewing_time': viewing_time,
    }

    return data
