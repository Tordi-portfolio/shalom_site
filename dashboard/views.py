from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from exams.models import ExamSession, Subject
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SubjectForm
from exams.models import Subject, Question
from .forms import QuestionForm
from exams.models import Subject, ExamSession

@login_required
def dashboard(request):

    subjects = Subject.objects.filter(is_active=True)

    completed_subjects = ExamSession.objects.filter(
        user=request.user,
        completed=True
    ).values_list("subject_id", flat=True)

    context = {
        "subjects": subjects,
        "completed_subjects": completed_subjects,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


@staff_member_required
def admin_dashboard(request):

    context = {
        "subjects": Subject.objects.count(),
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context,
    )


@staff_member_required
def subject_list(request):

    subjects = Subject.objects.all()

    return render(

        request,

        "dashboard/subject_list.html",

        {

            "subjects": subjects

        }

    )


@staff_member_required
def add_subject(request):

    if request.method == "POST":

        form = SubjectForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("subject_list")

    else:

        form = SubjectForm()

    return render(

        request,

        "dashboard/subject_form.html",

        {

            "form": form,

            "title": "Add Subject",

        }

    )


@login_required
def edit_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == "POST":

        form = SubjectForm(
            request.POST,
            instance=subject
        )

        if form.is_valid():

            form.save()

            return redirect("subject_list")

    else:

        form = SubjectForm(instance=subject)

    return render(
        request,
        "dashboard/subject_form.html",
        {
            "form": form,
            "title": "Edit Subject",
        },
    )


@login_required
def delete_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    subject.delete()

    return redirect("subject_list")


# Question section

@login_required
def question_list(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    questions = Question.objects.filter(
        subject=subject
    ).order_by("order")

    return render(
        request,
        "dashboard/question_list.html",
        {
            "subject": subject,
            "questions": questions,
        },
    )


@login_required
def add_question(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.save(commit=False)

            question.subject = subject

            question.save()

            return redirect(
                "question_list",
                subject.id
            )

    else:

        form = QuestionForm()

    return render(
        request,
        "dashboard/question_form.html",
        {
            "form": form,
            "subject": subject,
            "title": "Add Question",
        },
    )


@login_required
def edit_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            instance=question
        )

        if form.is_valid():

            form.save()

            return redirect(
                "question_list",
                question.subject.id
            )

    else:

        form = QuestionForm(
            instance=question
        )

    return render(
        request,
        "dashboard/question_form.html",
        {
            "form": form,
            "subject": question.subject,
            "title": "Edit Question",
        },
    )


@login_required
def delete_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    subject_id = question.subject.id

    question.delete()

    return redirect(
        "question_list",
        subject_id
    )

# users response
@login_required
def submission_list(request):

    exams = ExamSession.objects.filter(
        completed=True
    ).select_related(
        "user",
        "subject"
    )

    return render(
        request,
        "dashboard/submission_list.html",
        {
            "exams": exams,
        },
    )


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def view_submission(request, exam_id):

    exam = get_object_or_404(
        ExamSession,
        id=exam_id
    )

    answers = exam.answers.select_related("question")

    if request.method == "POST":

        total = 0

        for answer in answers:

            score = request.POST.get(
                f"score_{answer.id}",
                0
            )

            feedback = request.POST.get(
                f"feedback_{answer.id}",
                ""
            )

            answer.score = score or 0
            answer.feedback = feedback
            answer.save()

            total += float(answer.score)

        exam.score = total
        exam.save()

        messages.success(
            request,
            "Scores saved successfully."
        )

        return redirect(
            "view_submission",
            exam.id
        )

    return render(
        request,
        "dashboard/view_submission.html",
        {
            "exam": exam,
            "answers": answers
        }
    )


from django.contrib import messages

@login_required
def delete_submission(request, exam_id):

    exam = get_object_or_404(
        ExamSession,
        id=exam_id
    )

    student_name = exam.user.username
    subject_name = exam.subject.title

    exam.delete()

    messages.success(
        request,
        f"{student_name}'s submission for '{subject_name}' has been deleted successfully."
    )

    return redirect("submission_list")