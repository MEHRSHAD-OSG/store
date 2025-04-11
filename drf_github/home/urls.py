from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'home'
urlpatterns = [
    path('', views.HomeAllViews.as_view(), name='home'),
    path('questions/', views.QuestionListView.as_view(), name='question'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question'),
    path('question/update/<int:pk>/', views.QuestionUpdateView.as_view(), name='question'),
    path('question/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='question_pk'),
    path('answers/<int:pk>/', views.AnswerViewset.as_view({'post': 'create'}), name='answer-create'),
]
router = routers.SimpleRouter()
router.register("answer", views.AnswerViewset)
urlpatterns += router.urls
