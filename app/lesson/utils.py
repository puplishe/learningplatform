from .models import LessonView


def view_count_time(duration: int, lesson_view: LessonView):
    if lesson_view:
        lesson_duration_seconds = duration
        if lesson_duration_seconds:
            if lesson_view.start_time is not None and lesson_view.end_time is not None:
                viewing_time_seconds = (lesson_view.end_time - lesson_view.start_time).total_seconds()
                if lesson_view.time_watched is not None:
                    lesson_view.time_watched += viewing_time_seconds
                    if lesson_view.time_watched >= 0.8 * lesson_duration_seconds:
                        lesson_view.status = True
                else:
                    lesson_view.time_watched = viewing_time_seconds
                    if lesson_view.time_watched <= 0.8 * lesson_duration_seconds:
                        lesson_view.status = False
                    else:
                        lesson_view.status = True

    return lesson_view
