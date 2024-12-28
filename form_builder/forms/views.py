from collections import Counter
from .models import *
from .serializer import *
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response as restResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permission import IsAdminUser

# Here class based views are used

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        form = self.get_object()
        responses = Response.objects.filter(form=form)
        total_responses = responses.count()
        analytics = {
            "total_responses": total_responses, "questions": []
        }
        
        for question in form.questions.all():
            question_data = {"id": question.id, "text": question.text}
            
            if question.type == Question.TEXT:
                answers = Answer.objects.filter(question=question).values_list('text_answer', flat=True)
                word_counts = Counter(word for answer in answers for word in answer.split() if len(word) >= 5)
                top_words = word_counts.most_common(5)
                question_data["analytics"] = {"word_count": top_words}
            
            elif question.type in [Question.DROPDOWN, Question.CHECKBOX]:
                answers = Answer.objects.filter(question=question).values_list('selected_options', flat=True)
                options_count = Counter(tuple(sorted(options)) for options in answers)
                top_options = options_count.most_common(5)
                question_data["analytics"] = {"option_count": top_options}
            
            analytics["questions"].append(question_data)
        
        return restResponse(analytics)

class ResponseCreateView(generics.CreateAPIView):
    serializer_class = ResponseSerializer


# Authentication views

class CustomAuthToken(ObtainAuthToken):
    """
    Returns a token for the authentication Admin user
    """
    
    def post(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        user = serializers.validated_data['user']
        if not user.is_staff:
            return restResponse({"error": "Only admin users can log in"}, status=403)
        token, created = Token.objects.get_or_create(user=user)
        return restResponse({'token': token.key, 'user_id': user.pk, 'username': user.username})
        return super().post(request, *args, **kwargs)


class AdminFormViewSet(viewsets.ModelViewSet):
    """
    Handles form creation and management for Admins
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated , IsAdminUser]