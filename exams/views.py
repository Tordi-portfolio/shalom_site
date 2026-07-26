from datetime import timedelta
from urllib import request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .models import Subject, ExamSession, StudentAnswer, Question
from django.shortcuts import render


@login_required
def start_exam(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        is_active=True
    )

    # Prevent user from taking a completed exam again
    already_completed = ExamSession.objects.filter(
        user=request.user,
        subject=subject,
        completed=True
    ).exists()

    if already_completed:
        messages.warning(
            request,
            "You have already completed this examination."
        )
        return redirect("dashboard")

    now = timezone.now()

    # Check for an active (unfinished) exam
    active_exam = ExamSession.objects.filter(
        user=request.user,
        subject=subject,
        completed=False
    ).first()

    if active_exam:

        # Continue the exam if time has not expired
        if now < active_exam.expires_at:
            return redirect("question_page", active_exam.id, 1)

        # Time expired
        # Delete answers
        StudentAnswer.objects.filter(
            exam=active_exam
        ).delete()

        # Delete exam session
        active_exam.delete()

    # Create a brand new exam session
    exam = ExamSession.objects.create(
        user=request.user,
        subject=subject,
        expires_at=now + timedelta(hours=24)
    )

    return redirect("question_page", exam.id, 1)

@login_required
def exam_page(request, exam_id):

    exam = get_object_or_404(

        ExamSession,

        id=exam_id,

        user=request.user

    )

    questions = exam.subject.questions.all()

    context = {

        "exam": exam,

        "questions": questions,

    }

    return render(request, "exams/exam.html", context)


@login_required
def question_page(request, exam_id, number):

    exam = get_object_or_404(
        ExamSession,
        id=exam_id,
        user=request.user,
        completed=False
    )

    # Check if exam has expired
    if timezone.now() >= exam.expires_at:

        exam.answers.all().delete()
        exam.delete()

        messages.error(
            request,
            "Your examination has expired. Please start again."
        )

        return redirect("dashboard")

    questions = list(
        exam.subject.questions.order_by("order")
    )

    total = len(questions)

    if number < 1 or number > total:
        return redirect("question_page", exam.id, 1)

    question = questions[number - 1]

    answer, created = StudentAnswer.objects.get_or_create(
        exam=exam,
        question=question
    )

    if request.method == "POST":

        # Save text answer
        if question.allow_text:
            answer.answer = request.POST.get("answer", "")

        # Save uploaded image
        if question.allow_image:

            image = request.FILES.get("image")

            if image:
                answer.uploaded_image = image

            elif question.image_required and not answer.uploaded_image:

                messages.error(
                    request,
                    "This question requires an image."
                )

                return redirect(
                    "question_page",
                    exam.id,
                    number
                )

        answer.save()

        if number == total:
            return redirect("submit_exam", exam.id)

        return redirect(
            "question_page",
            exam.id,
            number + 1
        )

    return render(
        request,
        "exams/question.html",
        {
            "exam": exam,
            "question": question,
            "answer": answer,
            "number": number,
            "total": total,
        }
    )


@login_required
def submit_exam(request, exam_id):

    exam = get_object_or_404(
        ExamSession,
        id=exam_id,
        user=request.user
    )

    exam.completed = True
    exam.submitted_at = timezone.now()
    exam.save()

    messages.success(request, "Exam submitted successfully.")

    return redirect("dashboard")