# Create your urls here - possible pages and views
from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("sphere/", views.sphere, name="sphere"),
    path("api/questions/", views.QuestionListCreate.as_view(), name="question-list"),
    path("api/questions/<int:pk>/", views.QuestionDetail.as_view(), name="question-detail"),
    path("api/choices/", views.ChoiceListCreate.as_view(), name="choice-list"),
    path("api/choices/<int:pk>/", views.ChoiceDetail.as_view(), name="choice-detail"),
]
