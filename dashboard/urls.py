from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    # Subject section

    path(
        "admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
    path(
        "subjects/",
        views.subject_list,
        name="subject_list",
    ),

    path(
        "subjects/add/",
        views.add_subject,
        name="add_subject",
    ),

    path(
        "subjects/<int:subject_id>/edit/",
        views.edit_subject,
        name="edit_subject",
    ),

    path(
        "subjects/<int:subject_id>/delete/",
        views.delete_subject,
        name="delete_subject",
    ),

    # Questions section

    path(
        "subjects/<int:subject_id>/questions/",
        views.question_list,
        name="question_list",
    ),

    path(
        "subjects/<int:subject_id>/questions/add/",
        views.add_question,
        name="add_question",
    ),

    path(
        "questions/<int:question_id>/edit/",
        views.edit_question,
        name="edit_question",
    ),

    path(
        "questions/<int:question_id>/delete/",
        views.delete_question,
        name="delete_question",
    ),

    # users response
    path(
        "submissions/",
        views.submission_list,
        name="submission_list",
    ),

    path(
        "submissions/<int:exam_id>/",
        views.view_submission,
        name="view_submission",
    ),
    path(
        "submissions/<int:exam_id>/delete/",
        views.delete_submission,
        name="delete_submission",
    ),
]