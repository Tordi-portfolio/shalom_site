from django.conf import settings
from django.db import models

class Subject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(
        default=30,
        help_text="Duration in minutes"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Question(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    marks = models.PositiveIntegerField(default=5)

    order = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.subject.title} - Question {self.order}"


class ExamSession(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    started_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    completed = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.user} - {self.subject}"


class StudentAnswer(models.Model):

    exam = models.ForeignKey(
        ExamSession,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    answer = models.TextField(blank=True)

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    feedback = models.TextField(
        blank=True
    )

    class Meta:
        unique_together = ("exam", "question")

    def __str__(self):
        return f"{self.exam.user.username} - Question {self.question.order}"