# region import libraries
from rest_framework.views import APIView
from django.contrib.auth.models import User

from drf_learn_2025.settings import SIMPLE_JWT
from . import serializers, models
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
# from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import Token, RefreshToken


# endregion

class UserRegisterView(APIView):
    serializer_class = serializers.UserRegisterSerializer

    # def get(self, request):
    #     user = User.objects.all()
    #     ser_data = serializers.UserRegisterSerializer(instance=user, many=True)
    #     return Response(
    #         data={"data": ser_data.data, "user": request.user.username if request.user.is_authenticated else None})

    def post(self, request):
        ser_data = serializers.UserRegisterSerializer(data=request.data)  # Use correct serializer import
        if ser_data.is_valid():
            ser_data.save()  # Call serializer's save() method, which hashes the password
            return Response(data={'user registered with this info': ser_data.data})
        return Response(data=ser_data.errors)


# class UserLoginView(APIView):
#     def get(self, request):
#         return Response(data={"user": request.user.username})
#
#     def post(self, request):
#         serializer = serializers.UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(request=request, username=username, password=password)
#             if user is not None:
#                 login(request, user)  # Log the user into the session and update sessions
#                 Token.objects.get_or_create(user=user)
#                 return Response(
#                     {'data': serializer.data},
#                     status=status.HTTP_200_OK
#                 )
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserViewsetSerializer

    def list(self, request):
        ser_data_instance = self.serializer_class(instance=self.queryset, many=True).data
        return Response(data=ser_data_instance)

    def retrieve(self, request, pk=None):
        ser_data_instance = self.serializer_class(instance=get_object_or_404(self.queryset, pk=pk))
        return Response(ser_data_instance.data)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({"Permission denied": "You're not the owner"})
        ser_data_instance = self.serializer_class(instance=user, data=request.data,
                                                  partial=True)
        if ser_data_instance.is_valid():
            ser_data_instance.save()
            return Response(ser_data_instance.data)
        return Response(ser_data_instance.errors)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({"Permission denied": "You're not the owner"})
        user.is_active = False
        user.save()
        return Response({"Message": "User inactivated succesfuly"})


class UserLoginView(APIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        ser_data = serializers.UserLoginSerializer(data=request.data)
        if ser_data.is_valid():
            username = ser_data.validated_data['username']
            password = ser_data.validated_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user:
                token = RefreshToken.for_user(user)
                return Response({"data": ser_data.data, "refresh": str(token), "access": str(token.access_token)})
            return Response({"error": "Invalid username or password"})
        return Response(ser_data.errors)


class RefreshTokenView(APIView):
    def post(self, request):

        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and refresh the token
        token = RefreshToken(refresh_token)
        new_access_token = str(token.access_token)

        # If ROTATE_REFRESH_TOKENS is True, generate a new refresh token
        new_refresh_token = str(token) if SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS") else None

        response_data = {
            "message": "Token refreshed successfully",
            "access": new_access_token,
        }
        if new_refresh_token:
            response_data["refresh"] = new_refresh_token

        return Response(response_data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
        just send token to this class
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "توکن با موفقیت باطل شد"})
        return Response({"error": "توکن ارائه نشده است"}, status=400)
