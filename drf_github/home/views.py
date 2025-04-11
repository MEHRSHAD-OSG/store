from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


# Create your views here.
class HomeAllViews(APIView):
    # def get(self, req):
    #     # req.query_params['name']for get query params (after ? in urls like ?name=Mehrshad)
    #     name = req.query_params.get('name', "Ali")
    #     return Response({'name': name})
    permission_classes = [IsAuthenticated]

    def get(self, request):
        person = models.Person.objects.all()
        ser_data = serializers.PersonSerializer(instance=person, many=True)
        return Response(data=ser_data.data)


class QuestionListView(APIView):
    serializer_class = serializers.QuestionSerializer

    def get(self, request):
        question_instance = models.Question.objects.all()
        ser_data = self.serializer_class(instance=question_instance, many=True).data
        return Response(ser_data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.QuestionSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data, context={'request': request})
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = serializers.QuestionSerializer

    def put(self, request, pk):
        question = models.Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)  # for check custom object perm
        ser_data = self.serializer_class(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = serializers.QuestionSerializer

    def delete(self, request, pk):
        question = models.Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        question.delete()
        return Response("deleted succesfully")


class AnswerViewset(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

    def list(self, request):
        ser_data_instance = self.serializer_class(instance=self.queryset, many=True)
        return Response(ser_data_instance.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        ser_data_instance = self.serializer_class(instance=get_object_or_404(self.queryset, pk=pk)).data
        return Response(ser_data_instance, status=status.HTTP_200_OK)

    def create(self, request, pk):
        question = get_object_or_404(models.Question.objects.all(), question=pk)
        ser_data_instance = self.serializer_class(data=request.data, context={'request': request, "question": question})
        if ser_data_instance.is_valid():
            ser_data_instance.save()
            return Response(ser_data_instance.data, status=status.HTTP_201_CREATED)
        return Response(ser_data_instance.errors)

    def update(self, request, pk=None):
        answer = get_object_or_404(self.queryset, pk=pk)
        ser_data_instance = self.serializer_class(instance=answer, data=request.data)

        if answer.user != request.user:
            return Response({"Permission denied": "This answer is not yours"})
        if ser_data_instance.is_valid():
            ser_data_instance.save()
            return Response(ser_data_instance.data, status=status.HTTP_201_CREATED)
        return Response(ser_data_instance.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        answer = get_object_or_404(self.queryset, pk=pk)
        ser_data_instance = self.serializer_class(instance=answer, data=request.data)
        if answer.user != request.user:
            return Response({"Permission denied": "This answer is not yours"})

        if ser_data_instance.is_valid():
            ser_data_instance.save()
            return Response(ser_data_instance.data, status=status.HTTP_201_CREATED)
        return Response(ser_data_instance.errors, status=status.HTTP_400_BAD_REQUEST)
