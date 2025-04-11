from rest_framework import serializers
from . import models
from django.utils.text import slugify
from .custom_relational_fields import EmailAndUsernameFields


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        # fields = '__all__'
        exclude = ['id', 'creation']  # show all fields except id


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # from user model return any thing on __str__

    # user = serializers.SlugRelatedField(read_only=True,
    #                                     slug_field='email')  # from user model show any thing in slug field
    # user = EmailAndUsernameFields(read_only=True)

    class Meta:
        model = models.Question
        exclude = ['created']
        extra_kwargs = {
            'user': {'read_only': True},
            'slug': {'read_only': True}
        }

    answers = serializers.SerializerMethodField(method_name="all_answers")

    def all_answers(self, obj):
        # obj => all questions
        result = obj.question.all()
        return AnswerSerializer(instance=result, many=True).data

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.get("title", '')
        if 'slug' in self.initial_data:
            raise serializers.ValidationError({"slug": "You cannot send this field."})
        validated_data['slug'] = slugify(title)
        return models.Question.objects.create(user=user, **validated_data)


class AnswerSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    question = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Answer
        exclude = ['id', 'created']

    def create(self, validated_data):
        request = self.context['request']
        question = self.context['question']
        if 'user' in self.initial_data:
            # print("=" * 90, self.initial_data) # initial_data => all data send from client
            raise serializers.ValidationError({"user": "You cannot send this field."})
        if 'question' in self.initial_data:
            raise serializers.ValidationError({"question": "You cannot send this field."})
        return models.Answer.objects.create(user=request.user, question=question, **validated_data)
