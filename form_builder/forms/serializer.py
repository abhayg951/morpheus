from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'options', 'order', 'is_required']

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    
    class Meta:
        model = Form
        fields = '__all__'
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        form = Form.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(form=form, **question_data)
        return form

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Response
        fields = '__all__'
    
    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        user_response = Response.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(response=user_response, **answer_data)
        return user_response