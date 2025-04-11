from django.urls import path
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as token_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    # path('login/', views.UserLoginView.as_view()),
    # path('login/', token_view.obtain_auth_token)
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),
]
router = routers.SimpleRouter()
router.register("user", views.UserViewset)
urlpatterns += router.urls
