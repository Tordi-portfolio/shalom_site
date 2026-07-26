from django.urls import path
from . import views

urlpatterns = [

    path(
        "start/<int:subject_id>/",
        views.start_exam,
        name="start_exam"
    ),

    path(
        "<int:exam_id>/question/<int:number>/",
        views.question_page,
        name="question_page"
    ),

    path(
        "<int:exam_id>/submit/",
        views.submit_exam,
        name="submit_exam"
    ),
]