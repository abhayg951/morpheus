from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Form(models.Model):
    '''Store form details'''
    title = models.CharField(max_length=150, help_text='Title of the form')
    description = models.TextField(blank=True, null=True, help_text="Description of the form (Optional)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time the form was created")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms", help_text="Admin of the form")
    
    def __str__(self):
        return self.title

class Question(models.Model):
    '''Store details of each question, linked to a specific form'''
    
    TEXT = 'text'
    DROPDOWN = 'dropdown'
    CHECKBOX = 'checkbox'
    
    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (DROPDOWN, 'Dropdown'),
        (CHECKBOX, 'Checkbox')
    ]
    
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions", help_text="Question for the form")
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, help_text="Type of question")
    text = models.TextField(help_text="Text of the question")
    order = models.PositiveIntegerField(help_text="Order of the question in the form")
    options = models.JSONField(blank=True, null=True, help_text="Options for dropdown or checkbox questions")
    is_required = models.BooleanField(default=True, help_text="Question is required or not")
    
    def __str__(self):
        return self.text
    
    def clean(self):
        if self.type in [self.DROPDOWN, self.CHECKBOX] and not self.options:
            raise ValidationError("Options are required for dropdown and checkbox questions")
        if self.type == self.TEXT and self.options:
            raise ValidationError("Options are not allowed for text questions")

class Response(models.Model):
    '''store user responses for a form'''
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses", help_text="Form for which the response is")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Date and time the response was submitted")
    
    def __str__(self):
        return f"{self.form.title} - {self.submitted_at}"

class Answer(models.Model):
    '''Link specific answer to questions in a response'''
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers", help_text="Response for which the answer is")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", help_text="Question for which the answer is")
    text_answer = models.TextField(blank=True, null=True, help_text="Text answer for the question")
    selected_options = models.JSONField(blank=True, null=True, help_text="Selected options for dropdown or checkbox questions")
    
    def __str__(self):
        return f"{self.question.text} - {self.text_answer}"
    
    def clean(self):
        if self.question.type == Question.text and not self.text_answer:
            raise ValidationError("Answer should be in text for text questions")
        if self.question.type in [Question.DROPDOWN, Question.CHECKBOX] and not self.selected_options:
            raise ValidationError("Answer should be selected for dropdown or checkbox questions")