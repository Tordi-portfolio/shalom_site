from django import forms
from exams.models import Subject, Question


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "title",
            "description",
            "duration",
            "is_active",
        ]


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question

        fields = [
            "question",
            "marks",
            "order",
        ]