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

    order = models.PositiveIntegerField(default=1)

    marks = models.PositiveIntegerField(default=10)

    # New fields
    allow_text = models.BooleanField(default=True)

    allow_image = models.BooleanField(default=False)

    image_required = models.BooleanField(default=False)

    def __str__(self):
        return self.question[:50]
    

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

    uploaded_image = models.ImageField(
        upload_to="student_answers/",
        blank=True,
        null=True
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    feedback = models.TextField(blank=True)