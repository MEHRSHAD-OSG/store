from rest_framework import serializers
from django.contrib.auth.models import User


def validate_email(value):
    """
        this method when use have many validation on one field
    """
    email = User.objects.filter(email=value).exists()
    if email:
        raise serializers.ValidationError({"email": "This email already exists"})


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'email': {'validators': [validate_email], 'required': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})

        return data

    def validate_username(self, value):
        if value.lower() == 'admin':
            raise serializers.ValidationError("username can't be 'admin'")
        return value  # always must be return value

    def create(self, validated_data):
        # hashed password
        validated_data.pop('confirm_password')  # Remove confirm_password before saving user
        user = User(username=validated_data['username'], email=validated_data['email'],
                    first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError("Both username and password are required")
        return data


class UserViewsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
